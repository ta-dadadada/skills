import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('install_rules', PACKAGE / 'scripts/install_rules.py')
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / 'project with spaces'
        self.root.mkdir()
        self.spec = installer.catalog()['software-design']
        self.rule = self.root / '.claude/rules/ta-dadadada-software-design.md'
        self.state = self.root / '.claude' / self.spec.state
        self.source = b'# Design\nKeep related behaviour together.\n'

    def plan(self):
        return installer.assess(self.root, self.source, self.spec)

    def apply(self, plan=None):
        return installer.apply(self.root, self.source, (plan or self.plan())['plan_id'], self.spec)

    def install(self):
        self.assertEqual('install', self.plan()['action'])
        self.apply()

    def assert_error(self, code, callback):
        with self.assertRaises(installer.InstallError) as caught:
            callback()
        self.assertEqual(code, caught.exception.code)

    def test_plan_is_read_only_and_install_is_repeatable(self):
        plan = self.plan()
        self.assertFalse((self.root / '.claude').exists())
        self.assertEqual(plan['plan_id'], self.plan()['plan_id'])
        self.assertIn('+Keep related behaviour', plan['diff'])
        self.apply(plan)
        self.assertEqual(self.source, self.rule.read_bytes())
        before = (self.rule.stat().st_mtime_ns, self.state.read_bytes(), self.state.stat().st_mtime_ns)
        self.assertEqual('unchanged', self.apply()['result'])
        self.assertEqual(before, (self.rule.stat().st_mtime_ns, self.state.read_bytes(), self.state.stat().st_mtime_ns))

    def test_update_preserves_mode_and_unrelated_files(self):
        self.install()
        self.rule.chmod(0o640)
        other = self.rule.parent / 'team.md'
        other.write_text('Team rule')
        self.source += b'Hide details.\n'
        self.assertEqual('update', self.plan()['action'])
        self.apply()
        self.assertEqual(self.source, self.rule.read_bytes())
        self.assertEqual(0o640, self.rule.stat().st_mode & 0o777)
        self.assertEqual('Team rule', other.read_text())

    def test_local_edit_conflicts_and_is_preserved(self):
        self.install()
        self.rule.write_bytes(b'Local custom rule\n')
        before = self.state.read_bytes()
        self.assertEqual('conflict', self.plan()['action'])
        self.assert_error('conflict', self.apply)
        self.assertEqual(b'Local custom rule\n', self.rule.read_bytes())
        self.assertEqual(before, self.state.read_bytes())

    def test_personal_rule_survives_install_and_uninstall(self):
        self.rule.parent.mkdir(parents=True)
        personal = self.rule.with_name('software-design.md')
        personal.write_text('Project conventions')
        self.install()
        self.uninstall()
        self.assertEqual('Project conventions', personal.read_text())

    def test_legacy_install_retains_state_and_rule(self):
        self.install()
        record = json.loads(self.state.read_bytes())
        self.state.write_bytes(installer.encoded({**record, 'schema': 1}))
        self.rule.rename(self.rule.with_name('software-design.md'))
        self.assert_error('legacy_install', self.uninstall_plan)
        self.assertTrue(self.state.exists())

    def test_personal_rule_does_not_block_recovery_or_cleanup(self):
        self.rule.parent.mkdir(parents=True)
        personal = self.rule.with_name('software-design.md')
        personal.write_text('Personal')
        self.install()
        record = json.loads(self.state.read_bytes())
        self.rule.unlink()
        self.assertEqual('cleanup', self.uninstall_plan()['action'])
        self.state.write_bytes(installer.encoded({**record, 'installed_sha256': None,
                                                 'pending_sha256': installer.digest(self.source)}))
        self.assertEqual('recover', self.plan()['action'])
        self.apply()
        self.assertEqual(self.source, self.rule.read_bytes())
        self.assertEqual('Personal', personal.read_text())

    def test_diff_marks_missing_newlines_on_both_sides(self):
        self.rule.parent.mkdir(parents=True)
        self.rule.write_bytes(b'old')
        self.source = b'new'
        self.assertEqual(self.plan()['diff'].splitlines()[-4:],
                         ['-old', r'\ No newline at end of file',
                          '+new', r'\ No newline at end of file'])

    def test_unmanaged_different_conflicts(self):
        self.rule.parent.mkdir(parents=True)
        self.rule.write_text('Existing rule')
        self.assert_error('conflict', self.apply)
        self.assertFalse(self.state.exists())

    def test_unmanaged_equal_not_adopted(self):
        self.rule.parent.mkdir(parents=True)
        self.rule.write_bytes(self.source)
        self.assertEqual('unchanged', self.apply()['result'])
        self.assertFalse(self.state.exists())
        self.source += b'New\n'
        self.assertEqual('conflict', self.plan()['action'])

    def test_removed_managed_rule_conflicts(self):
        self.install()
        self.rule.unlink()
        self.assertEqual('conflict', self.plan()['action'])
        self.assert_error('conflict', self.apply)
        self.assertFalse(self.rule.exists())

    def test_stale_target_source_and_state(self):
        self.install()
        original = self.source
        for change in ('target', 'source', 'state'):
            with self.subTest(change=change):
                self.rule.write_bytes(original)
                self.state.write_bytes(installer.encoded({'schema': 1, 'installed_sha256': installer.digest(original), 'pending_sha256': None}))
                self.source = original + b'New\n'
                plan = self.plan()
                if change == 'target':
                    self.rule.write_text('Local edit')
                elif change == 'source':
                    self.source += b'More\n'
                else:
                    self.state.write_bytes(self.state.read_bytes() + b' ')
                self.assert_error('stale_plan', lambda: self.apply(plan))

    def test_plan_is_bound_to_root(self):
        plan = self.plan()
        other = self.base / 'other'
        other.mkdir()
        self.assert_error('stale_plan', lambda: installer.apply(other, self.source, plan['plan_id'], self.spec))
        self.assertFalse((other / '.claude').exists())

    def test_invalid_state_fails_closed(self):
        self.state.parent.mkdir()
        for value in (b'broken', b'[]', b'{"schema": 2}', installer.encoded({'schema': 1, 'installed_sha256': 'invalid', 'pending_sha256': None})):
            self.state.write_bytes(value)
            self.assert_error('invalid_state', self.plan)
        self.assertFalse(self.rule.exists())

    def test_symlink_paths_refused(self):
        outside = self.base / 'outside'
        outside.mkdir()
        for relative in ('.claude', '.claude/rules', '.claude/rules/ta-dadadada-software-design.md', '.claude/' + self.spec.state):
            with self.subTest(path=relative):
                claude = self.root / '.claude'
                if claude.is_symlink():
                    claude.unlink()
                elif claude.exists():
                    shutil.rmtree(claude)
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(outside)
                self.assert_error('unsafe_path', self.plan)
        self.assertEqual([], list(outside.iterdir()))

    def test_symlink_lock_refused_without_writing_target(self):
        claude = self.root / '.claude'
        claude.mkdir()
        outside = self.base / 'external'
        outside.write_text('Keep')
        (claude / self.spec.lock).symlink_to(outside)
        with self.assertRaises(OSError):
            self.apply()
        self.assertFalse(self.rule.exists())
        self.assertFalse(self.state.exists())
        self.assertEqual('Keep', outside.read_text())

    def test_special_file_refused_without_blocking(self):
        self.rule.parent.mkdir(parents=True)
        os.mkfifo(self.rule)
        self.assert_error('unsafe_path', self.plan)

    def test_binary_file_conflicts(self):
        self.rule.parent.mkdir(parents=True)
        self.rule.write_bytes(b'\xff\x00')
        self.assertEqual('conflict', self.plan()['action'])
        self.assert_error('conflict', self.apply)

    def test_lock_serializes_installers(self):
        import fcntl
        self.state.parent.mkdir()
        with (self.state.parent / self.spec.lock).open('w') as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            self.assert_error('busy', self.apply)
        self.assertFalse(self.rule.exists())
        self.apply()

    def test_recheck_after_acquiring_lock(self):
        original = installer.assess
        calls = 0
        def altered(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                self.rule.parent.mkdir(parents=True, exist_ok=True)
                self.rule.write_text('Concurrent rule')
            return original(*args)
        plan = self.plan()
        with patch.object(installer, 'assess', side_effect=altered):
            self.assert_error('stale_plan', lambda: self.apply(plan))
        self.assertEqual('Concurrent rule', self.rule.read_text())
        self.assertFalse(self.state.exists())

    def test_interrupted_writes_recover_before_and_after_rule(self):
        original = installer.atomic_write
        for fail_at in (2, 3):
            with self.subTest(fail_at=fail_at):
                if (self.root / '.claude').exists():
                    shutil.rmtree(self.root / '.claude')
                calls = 0
                def failing(*args, **kwargs):
                    nonlocal calls
                    calls += 1
                    if calls == fail_at:
                        raise OSError('Injected interruption')
                    return original(*args, **kwargs)
                with patch.object(installer, 'atomic_write', side_effect=failing):
                    with self.assertRaises(OSError):
                        self.apply()
                self.assertEqual('recover', self.plan()['action'])
                self.apply()
                self.assertEqual(self.source, self.rule.read_bytes())
                self.assertIsNone(json.loads(self.state.read_bytes())['pending_sha256'])

    def test_interrupted_update_recovers_old_content(self):
        self.install()
        old = self.source
        self.source += b'New\n'
        record = {'schema': 1, 'installed_sha256': installer.digest(old), 'pending_sha256': installer.digest(self.source)}
        self.state.write_bytes(installer.encoded(record))
        self.assertEqual('recover', self.plan()['action'])
        self.apply()
        self.assertEqual(self.source, self.rule.read_bytes())

    def test_pending_different_bundle_or_local_change_conflicts(self):
        self.install()
        self.state.write_bytes(installer.encoded({'schema': 1, 'installed_sha256': installer.digest(self.source), 'pending_sha256': installer.digest(b'Other')}))
        self.assertEqual('conflict', self.plan()['action'])
        self.source = b'Other'
        self.rule.write_text('Manual edits')
        self.assertEqual('conflict', self.plan()['action'])

    def test_failed_replace_preserves_original_and_cleans_temp(self):
        self.install()
        fd = os.open(self.rule.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            with patch.object(installer.os, 'replace', side_effect=OSError('Cannot replace')):
                with self.assertRaises(OSError):
                    installer.atomic_write(fd, self.spec.filename, b'New')
        finally:
            os.close(fd)
        self.assertEqual(self.source, self.rule.read_bytes())
        self.assertEqual([self.rule.name], [p.name for p in self.rule.parent.iterdir()])

    def test_cli_standalone_package_project_and_user_scope(self):
        bundle = self.base / 'standalone bundle'
        shutil.copytree(PACKAGE / 'scripts', bundle / 'scripts')
        shutil.copytree(PACKAGE / 'assets', bundle / 'assets')
        script = bundle / 'scripts/install_rules.py'
        def cli(*args):
            return subprocess.run([sys.executable, str(script), *args], cwd=self.base,
                                  capture_output=True, text=True)
        plan = cli('plan', '--project', str(self.root), '--rule', 'software-design')
        self.assertEqual(0, plan.returncode, plan.stderr)
        result = json.loads(plan.stdout)
        self.assertEqual(str(self.rule), result['destination'])
        applied = cli('apply', '--project', str(self.root), '--rule', 'software-design', '--plan-id', result['plan_id'])
        self.assertEqual(0, applied.returncode, applied.stderr)
        again = cli('plan', '--project', str(self.root), '--rule', 'software-design')
        self.assertEqual('unchanged', json.loads(again.stdout)['action'])
        self.rule.write_text('Conflict')
        conflict = cli('plan', '--project', str(self.root), '--rule', 'software-design')
        self.assertEqual(2, conflict.returncode)
        self.assertEqual('conflict', json.loads(conflict.stdout)['action'])
        bad = cli('apply', '--project', str(self.root), '--rule', 'software-design')
        self.assertEqual(2, bad.returncode)
        self.assertIn('--plan-id', bad.stderr)

    def test_cli_io_errors_are_json(self):
        with patch.object(installer, 'ASSETS', self.base / 'missing'), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, installer.main(['plan', '--project', str(self.root), '--rule', 'software-design']))
        self.assertEqual('io_error', json.loads(output.getvalue())['code'])

    def uninstall_plan(self):
        return installer.assess(self.root, self.source, self.spec, 'uninstall')

    def uninstall(self, plan=None):
        return installer.apply(self.root, self.source, (plan or self.uninstall_plan())['plan_id'], self.spec, 'uninstall')

    def test_uninstall_managed_rule_preserves_neighbors(self):
        self.install()
        neighbor = self.rule.parent / 'other.md'
        neighbor.write_text('Keep')
        self.assertEqual('uninstall', self.uninstall_plan()['action'])
        self.assertIn('-Keep related behaviour', self.uninstall_plan()['diff'])
        self.uninstall()
        self.assertFalse(self.rule.exists())
        self.assertFalse(self.state.exists())
        self.assertEqual('Keep', neighbor.read_text())
        self.assertEqual('unchanged', self.uninstall()['result'])
        self.assertTrue((self.state.parent / self.spec.lock).exists())

    def test_uninstall_modified_or_unmanaged_rule_refused(self):
        self.install()
        self.rule.write_text('Local changes')
        self.assert_error('conflict', self.uninstall)
        self.state.unlink()
        self.rule.write_bytes(self.source)
        self.assert_error('conflict', self.uninstall)
        self.assertEqual(self.source, self.rule.read_bytes())

    def test_uninstall_stale_plan_and_operation_switch_refused(self):
        self.install()
        plan = self.uninstall_plan()
        self.assert_error('stale_plan', lambda: self.apply(plan))
        self.rule.write_text('Edited after plan')
        self.assert_error('stale_plan', lambda: self.uninstall(plan))
        self.assertEqual('Edited after plan', self.rule.read_text())

    def test_uninstall_interruption_cleanup(self):
        self.install()
        original = installer.os.unlink
        def interrupt(name, *args, **kwargs):
            if name == self.spec.state:
                raise OSError('Injected interruption after rule removal')
            return original(name, *args, **kwargs)
        with patch.object(installer.os, 'unlink', side_effect=interrupt):
            with self.assertRaises(OSError):
                self.uninstall()
        self.assertFalse(self.rule.exists())
        self.assertTrue(self.state.exists())
        self.assertEqual('cleanup', self.uninstall_plan()['action'])
        self.uninstall()
        self.assertFalse(self.state.exists())

    def test_uninstall_uses_installed_version_not_current_bundle(self):
        self.install()
        self.source += b'Newer bundled version\n'
        self.assertEqual('uninstall', self.uninstall_plan()['action'])
        self.uninstall()
        self.assertFalse(self.rule.exists())

    def test_uninstall_refuses_pending_install(self):
        self.install()
        self.state.write_bytes(installer.encoded({'schema': 1, 'installed_sha256': installer.digest(self.source), 'pending_sha256': installer.digest(self.source + b'New')}))
        self.assert_error('conflict', self.uninstall)
        self.assertEqual(self.source, self.rule.read_bytes())


    def test_user_scope_without_touching_real_home(self):
        with patch.object(installer.Path, 'home', return_value=self.root), contextlib.redirect_stdout(io.StringIO()) as output:
            code = installer.main(['plan', '--user', '--rule', 'software-design'])
        self.assertEqual(0, code)
        self.assertEqual(str(self.rule), json.loads(output.getvalue())['destination'])
        self.assertFalse((self.root / '.claude').exists())

    def test_second_rule_added_by_manifest_only(self):
        assets = self.base / 'assets'
        shutil.copytree(PACKAGE / 'assets', assets)
        manifest = json.loads((assets / 'manifest.json').read_bytes())
        manifest['rules']['writing'] = {'asset': 'writing.md', 'filename': 'writing.md', 'description': 'Writing rules'}
        (assets / 'manifest.json').write_text(json.dumps(manifest))
        (assets / 'writing.md').write_text('Write clearly.\n')
        self.install()
        with patch.object(installer, 'ASSETS', assets):
            specs = installer.catalog()
            second = specs['writing']
            source = (assets / second.asset).read_bytes()
            plan = installer.assess(self.root, source, second)
            installer.apply(self.root, source, plan['plan_id'], second)
            plan = installer.assess(self.root, source, second, 'uninstall')
            installer.apply(self.root, source, plan['plan_id'], second, 'uninstall')
        self.assertFalse((self.rule.parent / 'writing.md').exists())
        self.assertEqual(self.source, self.rule.read_bytes())
        self.assertTrue(self.state.exists())

    def test_manifest_rejects_traversal_duplicate_destinations_and_unknown_fields(self):
        assets = self.base / 'assets'
        assets.mkdir()
        for entry in ({'asset': '../escape.md', 'filename': 'a.md', 'description': ''},
                      {'asset': 'a.md', 'filename': '../a.md', 'description': ''},
                      {'asset': 'a.md', 'filename': 'a.md', 'description': '', 'command': 'bad'}):
            (assets / 'manifest.json').write_text(json.dumps({'schema': 1, 'rules': {'a': entry}}))
            with patch.object(installer, 'ASSETS', assets):
                self.assert_error('invalid_manifest', installer.catalog)
        entry = {'asset': 'a.md', 'filename': 'a.md', 'description': ''}
        (assets / 'manifest.json').write_text(json.dumps({'schema': 1, 'rules': {'a': entry, 'b': entry}}))
        with patch.object(installer, 'ASSETS', assets):
            self.assert_error('invalid_manifest', installer.catalog)


if __name__ == '__main__':
    unittest.main()
