#!/usr/bin/env python3
"""Install bundled Claude Code rules; stdout is a single JSON result (Python 3.11+)."""
from __future__ import annotations

import argparse
import contextlib
import difflib
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
LIMIT = 2 * 1024 * 1024


@dataclass(frozen=True)
class RuleSpec:
    rule_id: str
    asset: str
    filename: str
    description: str

    @property
    def state(self) -> str:
        return f'.agent-rules-{self.rule_id}.json'

    @property
    def lock(self) -> str:
        return f'.agent-rules-{self.rule_id}.lock'


class InstallError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def catalog() -> dict[str, RuleSpec]:
    try:
        data = json.loads((ASSETS / 'manifest.json').read_bytes())
        if not isinstance(data, dict) or data.get('schema') != 1 or not isinstance(data.get('rules'), dict):
            raise ValueError('Invalid manifest schema')
        result = {}
        filenames = set()
        for rule_id, entry in data['rules'].items():
            if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', rule_id) or len(rule_id) > 64:
                raise ValueError('Invalid rule ID')
            if not isinstance(entry, dict) or set(entry) != {'asset', 'filename', 'description'}:
                raise ValueError('Invalid manifest entry')
            for field in ('asset', 'filename'):
                if not isinstance(entry[field], str) or not re.fullmatch(r'[a-z0-9][a-z0-9._-]*\.md', entry[field]):
                    raise ValueError('Rule assets and filenames must be simple Markdown filenames')
            if entry['filename'] in filenames or not isinstance(entry['description'], str):
                raise ValueError('Duplicate destination or invalid description')
            filenames.add(entry['filename'])
            result[rule_id] = RuleSpec(rule_id, **entry)
        if not result:
            raise ValueError('Empty rule catalog')
        return result
    except (ValueError, TypeError) as exc:
        raise InstallError('invalid_manifest', str(exc)) from exc


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True) + '\n').encode()


@contextlib.contextmanager
def directory(parent: int, name: str, create: bool = False):
    if create:
        try:
            os.mkdir(name, 0o755, dir_fd=parent)
        except FileExistsError:
            pass
    try:
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
    except FileNotFoundError:
        yield None
        return
    except OSError as exc:
        raise InstallError('unsafe_path', f'Expected a real directory: {name}') from exc
    try:
        yield fd
    finally:
        os.close(fd)


def read_file(parent: int | None, name: str) -> tuple[bytes | None, dict | None]:
    if parent is None:
        return None, None
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    except FileNotFoundError:
        return None, None
    except OSError as exc:
        raise InstallError('unsafe_path', f'Cannot safely read {name}') from exc
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > LIMIT:
            raise InstallError('unsafe_path', f'Expected a regular file <= {LIMIT} bytes: {name}')
        data = stream.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise InstallError('unsafe_path', f'File too large: {name}')
        after = os.fstat(stream.fileno())
        if (info.st_size, info.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise InstallError('changed_during_read', f'File changed while reading: {name}')
        return data, {'sha256': digest(data), 'mode': stat.S_IMODE(info.st_mode),
                      'device': info.st_dev, 'inode': info.st_ino,
                      'mtime_ns': info.st_mtime_ns}


def parse_state(data: bytes | None) -> dict | None:
    if data is None:
        return None
    try:
        record = json.loads(data)
        if not isinstance(record, dict) or set(record) != {'schema', 'installed_sha256', 'pending_sha256'}:
            raise ValueError('Unexpected state fields')
        if type(record['schema']) is not int or record['schema'] not in (1, 2):
            raise ValueError('Unsupported state schema')
        for key in ('installed_sha256', 'pending_sha256'):
            value = record[key]
            if value is not None and (not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value)):
                raise ValueError('Invalid hash')
        if record['installed_sha256'] is None and record['pending_sha256'] is None:
            raise ValueError('Empty state')
        return record
    except (ValueError, UnicodeError) as exc:
        raise InstallError('invalid_state', 'Installation record is invalid; no files changed.') from exc


def assess(root: Path, source: bytes, rule: RuleSpec, operation: str = 'install') -> dict:
    with contextlib.ExitStack() as stack:
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        stack.callback(os.close, root_fd)
        root_stat = os.fstat(root_fd)
        claude_fd = stack.enter_context(directory(root_fd, '.claude'))
        rules_fd = stack.enter_context(directory(claude_fd, 'rules')) if claude_fd is not None else None
        current, file_snapshot = read_file(rules_fd, rule.filename)
        state_bytes, state_snapshot = read_file(claude_fd, rule.state)
        # Pre-release installs used the bare rule ID as the destination.
        record = parse_state(state_bytes)
        if record and record['schema'] == 1 and rule.rule_id == 'software-design' and file_snapshot is None:
            legacy, _ = read_file(rules_fd, 'software-design.md')
            if legacy is not None:
                raise InstallError('legacy_install', 'Use the previous installer to uninstall the old software-design.md first.')
    current_hash = digest(current) if current is not None else None
    wanted = digest(source)
    action, reason = 'conflict', 'Existing file has no matching installation baseline.'
    if record and record['pending_sha256'] is not None:
        if record['pending_sha256'] != wanted:
            reason = 'An interrupted installation belongs to another bundle; resume with that bundle first.'
        elif current_hash in (record['installed_sha256'], wanted):
            action, reason = 'recover', 'Resume the interrupted installation using its recorded hashes.'
        else:
            reason = 'The rule changed after an interrupted installation.'
    elif current_hash == wanted:
        action, reason = 'unchanged', 'Rule already matches; no content or ownership changes.'
    elif current is None:
        if record is None:
            action, reason = 'install', 'No existing rule or installation record.'
        else:
            reason = 'A managed rule was removed locally; do not recreate it automatically.'
    elif record and current_hash == record['installed_sha256']:
        action, reason = 'update', 'Current rule matches the previous installation.'
    elif record:
        reason = 'Managed rule has local edits; no automatic merge or overwrite.'
    if operation == 'uninstall':
        if record and record['pending_sha256'] is not None:
            action, reason = 'conflict', 'Complete the interrupted installation before uninstalling.'
        elif record is None:
            action = 'unchanged' if current is None else 'conflict'
            reason = 'Nothing managed to remove.' if current is None else 'Unmanaged rule; refuse to delete it.'
        elif current is None:
            action, reason = 'cleanup', 'Rule is absent; remove its leftover installation record.'
        elif current_hash == record['installed_sha256']:
            action, reason = 'uninstall', 'Remove the unchanged managed rule and its installation record.'
        else:
            action, reason = 'conflict', 'Managed rule has local edits; refuse to delete it.'
    snapshot = {'operation': operation, 'rule_id': rule.rule_id, 'filename': rule.filename, 'root': str(root), 'root_device': root_stat.st_dev, 'root_inode': root_stat.st_ino,
                'source_sha256': wanted, 'rule': file_snapshot, 'state': state_snapshot}
    try:
        old_text = (current or b'').decode('utf-8')
        new_text = source.decode('utf-8') if operation == 'install' else ''
        lines = difflib.unified_diff(
            old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
            fromfile='installed/' + rule.filename,
            tofile='bundled/' + rule.filename if operation == 'install' else '/dev/null',
        )
        diff = ''.join(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n'
                       for line in lines)
    except UnicodeError:
        action, reason, diff = 'conflict', 'Rule is not UTF-8 text; no overwrite.', None
    return {'schema': 1, 'rule_id': rule.rule_id, 'operation': operation, 'action': action, 'reason': reason,
            'destination': str(root / '.claude' / 'rules' / rule.filename),
            'state_path': str(root / '.claude' / rule.state),
            'source_sha256': wanted, 'plan_id': digest(encoded(snapshot)),
            'diff': diff, 'snapshot': snapshot}


def atomic_write(parent: int, name: str, data: bytes, mode: int = 0o644) -> None:
    temporary = '.agent-rules-' + uuid.uuid4().hex + '.tmp'
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                 mode, dir_fd=parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, name, src_dir_fd=parent, dst_dir_fd=parent)
        os.fsync(parent)
    finally:
        try:
            os.unlink(temporary, dir_fd=parent)
        except FileNotFoundError:
            pass


def apply(root: Path, source: bytes, plan_id: str, rule: RuleSpec, operation: str = 'install') -> dict:
    import fcntl

    initial = assess(root, source, rule, operation)
    if initial['plan_id'] != plan_id:
        raise InstallError('stale_plan', 'Source or destination changed; run plan again.')
    if initial['action'] == 'conflict':
        raise InstallError('conflict', initial['reason'])
    if initial['action'] == 'unchanged':
        return {**initial, 'result': 'unchanged'}
    with contextlib.ExitStack() as stack:
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        stack.callback(os.close, root_fd)
        claude_fd = stack.enter_context(directory(root_fd, '.claude', create=True))
        lock_fd = os.open(rule.lock, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
                          0o600, dir_fd=claude_fd)
        stack.callback(os.close, lock_fd)
        if not stat.S_ISREG(os.fstat(lock_fd).st_mode):
            raise InstallError('unsafe_path', 'Installer lock is not a regular file.')
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise InstallError('busy', 'Another installer is applying; rerun plan when it finishes.') from exc
        latest = assess(root, source, rule, operation)
        if latest['plan_id'] != plan_id:
            raise InstallError('stale_plan', 'Destination changed before applying; run plan again.')
        if operation == 'uninstall':
            rules_fd = stack.enter_context(directory(claude_fd, 'rules'))
            _, observed = read_file(rules_fd, rule.filename)
            if observed != latest['snapshot']['rule']:
                raise InstallError('stale_plan', 'Rule changed before removal; run plan again.')
            if observed is not None:
                # Mark prefix-aware v1 installs before removal so cleanup can resume.
                data, _ = read_file(claude_fd, rule.state)
                record = parse_state(data)
                if record['schema'] == 1:
                    atomic_write(claude_fd, rule.state, encoded({**record, 'schema': 2}), 0o600)
                os.unlink(rule.filename, dir_fd=rules_fd)
                os.fsync(rules_fd)
            os.unlink(rule.state, dir_fd=claude_fd)
            os.fsync(claude_fd)
            return {**latest, 'result': 'removed'}
        rules_fd = stack.enter_context(directory(claude_fd, 'rules', create=True))
        old_state, _ = read_file(claude_fd, rule.state)
        record = parse_state(old_state)
        installed = record['installed_sha256'] if record else None
        pending = {'schema': 2, 'installed_sha256': installed,
                   'pending_sha256': digest(source)}
        atomic_write(claude_fd, rule.state, encoded(pending), 0o600)
        # Recheck the target after recording intent; interrupted writes remain recoverable.
        _, observed = read_file(rules_fd, rule.filename)
        if observed != latest['snapshot']['rule']:
            raise InstallError('stale_plan', 'Rule changed before replacement; pending state retained.')
        mode = observed['mode'] if observed else 0o644
        if observed is None or observed['sha256'] != digest(source):
            atomic_write(rules_fd, rule.filename, source, mode)
        current, _ = read_file(rules_fd, rule.filename)
        if current != source:
            raise InstallError('verification_failed', 'Rule changed during apply; pending state retained.')
        atomic_write(claude_fd, rule.state, encoded({'schema': 2, 'installed_sha256': digest(source),
                                              'pending_sha256': None}), 0o600)
    return {**latest, 'result': 'applied'}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('list', 'plan', 'apply'))
    parser.add_argument('--rule', help='Rule ID from list; required for plan/apply')
    parser.add_argument('--operation', choices=('install', 'uninstall'), default='install')
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--project', type=Path, help='Existing project root; no implicit cwd target')
    scope.add_argument('--user', action='store_true', help='Use ~/.claude/rules for all projects')
    parser.add_argument('--plan-id', help='Exact identifier from plan; required for apply')
    args = parser.parse_args(argv)
    if args.command == 'list':
        if args.rule or args.project or args.user or args.plan_id or args.operation != 'install':
            parser.error('list takes no target or operation options')
    elif not args.rule or (args.project is None and not args.user):
        parser.error('plan/apply require --rule and exactly one of --project or --user')
    if (args.command == 'apply') != (args.plan_id is not None):
        parser.error('--plan-id is required only for apply')
    try:
        if sys.platform not in ('darwin', 'linux'):
            raise InstallError('unsupported_platform', 'This installer supports macOS and Linux.')
        rules = catalog()
        if args.command == 'list':
            print(json.dumps({'schema': 1, 'rules': [vars(rule) for rule in rules.values()]}, indent=2))
            return 0
        if args.rule not in rules:
            raise InstallError('unknown_rule', 'Unknown rule ID; use list.')
        rule = rules[args.rule]
        root = (Path.home() if args.user else args.project.expanduser()).resolve(strict=True)
        if not root.is_dir():
            raise InstallError('invalid_target', 'Target must be an existing directory.')
        source = (ASSETS / rule.asset).read_bytes()
        source.decode('utf-8')
        if not source or len(source) > LIMIT:
            raise InstallError('invalid_source', 'Bundled rule must be nonempty UTF-8 text <= 2 MiB.')
        result = (assess(root, source, rule, args.operation) if args.command == 'plan'
                  else apply(root, source, args.plan_id, rule, args.operation))
        result.pop('snapshot', None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result['action'] == 'conflict' else 0
    except InstallError as exc:
        print(json.dumps({'result': 'error', 'code': exc.code, 'message': str(exc)}, ensure_ascii=False))
        return 2 if exc.code in ('conflict', 'stale_plan', 'busy') else 1
    except (OSError, UnicodeError) as exc:
        print(json.dumps({'result': 'error', 'code': 'io_error', 'message': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
