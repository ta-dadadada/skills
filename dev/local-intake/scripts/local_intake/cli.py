"""ローカル質問フォームのCLI境界。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .document import cleanup_document, ensure_local_exclude
from .server import serve_document
from .spec import ProtocolError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Serve one local-intake browser form.")
    parser.add_argument("--document", required=True, type=Path, help="local-intake Markdown path")
    parser.add_argument("--timeout", type=int, default=1800, help="seconds to wait for one submission")
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--prepare",
        action="store_true",
        help="register the document in Git's local exclude before creating it",
    )
    action.add_argument("--cleanup", action="store_true", help="remove a handed-off terminal document")
    parser.add_argument(
        "--no-git-exclude",
        action="store_true",
        help="leave Git's local exclude file unchanged",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    document = args.document.resolve()
    if args.timeout < 1 or args.timeout > 86400:
        print("local-intake: --timeout must be between 1 and 86400", file=sys.stderr)
        return 1
    try:
        if args.prepare:
            if args.no_git_exclude:
                raise ProtocolError("--prepare cannot be combined with --no-git-exclude")
            exclude_result = ensure_local_exclude(document)
            if exclude_result in {"not-git", "outside-root"}:
                print(f"local-intake: Git local exclude skipped ({exclude_result})", file=sys.stderr)
            return 0
        if args.cleanup:
            cleanup_document(document)
            print(f"Removed {document}")
            return 0
        if not args.no_git_exclude:
            exclude_result = ensure_local_exclude(document)
            if exclude_result in {"not-git", "outside-root"}:
                print(f"local-intake: Git local exclude skipped ({exclude_result})", file=sys.stderr)
        return serve_document(document, args.timeout)
    except ProtocolError as exc:
        print(f"local-intake: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
