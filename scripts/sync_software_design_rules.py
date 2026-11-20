#!/usr/bin/env python3
"""Generate the design skill reference from the installer asset; --check for CI."""
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'dev/install-agent-rules/assets/software-design.md'
TARGET = ROOT / 'dev/purpose-driven-software-design/references/design-principles.md'
HEADER = '<!-- Generated from install-agent-rules/assets/software-design.md; do not edit. -->\n\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--check-index', action='store_true', help='Compare staged files for pre-commit')
    args = parser.parse_args()
    if args.check_index:
        def staged(path: Path) -> bytes:
            key = ':' + path.relative_to(ROOT).as_posix()
            return subprocess.check_output(['git', 'show', key])
        try:
            matches = HEADER.encode() + staged(SOURCE) == staged(TARGET)
        except subprocess.CalledProcessError:
            matches = False
        if not matches:
            print('Staged design rules differ. Regenerate the reference and stage both files.')
        return int(not matches)
    expected = HEADER.encode() + SOURCE.read_bytes()
    if args.check:
        if not TARGET.is_file() or TARGET.read_bytes() != expected:
            print('Design rules drift: run python3 scripts/sync_software_design_rules.py')
            return 1
        print('Design rules are in sync.')
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_bytes(expected)
        print('Generated design-principles.md.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
