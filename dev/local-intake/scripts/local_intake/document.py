"""一時Markdownの解析、原子的更新、ライフサイクルを扱う。"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .spec import FormSpec, ProtocolError


STATE_MARKER = "<!-- LOCAL-INTAKE:STATE:v1 -->"
FORM_BEGIN = "<!-- LOCAL-INTAKE:FORM:BEGIN -->"
FORM_END = "<!-- LOCAL-INTAKE:FORM:END -->"
TERMINAL_STATUSES = {"agreed", "unresolved"}
STATUS_RE = re.compile(r"^Status:\s*(collecting|reviewing|agreed|unresolved)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class PendingDocument:
    content: str
    spec: FormSpec
    form_span: tuple[int, int]


def _line_marker_matches(content: str, marker: str) -> list[re.Match[str]]:
    return list(re.finditer(rf"^{re.escape(marker)}[ \t]*$", content, re.MULTILINE))


def parse_pending_document(content: str) -> PendingDocument:
    """文字列から未回答フォームを純粋に解析する。"""

    if len(_line_marker_matches(content, STATE_MARKER)) != 1:
        raise ProtocolError("document must contain exactly one state marker")
    begin_markers = _line_marker_matches(content, FORM_BEGIN)
    end_markers = _line_marker_matches(content, FORM_END)
    if len(begin_markers) != 1 or len(end_markers) != 1:
        raise ProtocolError("document must contain exactly one pending form block")
    begin = begin_markers[0]
    end = end_markers[0]
    if begin.end() >= end.start():
        raise ProtocolError("pending form markers are out of order")
    raw_json = content[begin.end() : end.start()].strip()
    try:
        raw_spec = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ProtocolError(f"pending form JSON is invalid: {exc}") from exc
    return PendingDocument(
        content=content,
        spec=FormSpec.parse(raw_spec),
        form_span=(begin.start(), end.end()),
    )


def read_pending_document(document: Path) -> PendingDocument:
    """ファイル境界を読み、純粋な解析関数へ渡す。"""

    try:
        content = document.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProtocolError(f"cannot read document: {exc}") from exc
    return parse_pending_document(content)


def replace_pending_content(pending: PendingDocument, replacement: str) -> str:
    """未回答ブロックを指定文字列へ置き換えた本文を返す。"""

    start, end = pending.form_span
    before = pending.content[:start].rstrip()
    after = pending.content[end:].lstrip("\r\n")
    updated = f"{before}\n\n{replacement.rstrip()}\n"
    if after:
        updated += f"\n{after}"
    return updated


def _atomic_write(document: Path, content: str) -> None:
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=document.parent,
            prefix=f".{document.name}.",
            delete=False,
        ) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temp_name = handle.name
        try:
            os.chmod(temp_name, document.stat().st_mode)
        except OSError:
            pass
        os.replace(temp_name, document)
        temp_name = None
    except OSError as exc:
        raise ProtocolError(f"cannot update document: {exc}") from exc
    finally:
        if temp_name:
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def replace_pending_block(document: Path, pending: PendingDocument, replacement: str) -> None:
    """未回答ブロックを原子的に置き換える。"""

    _atomic_write(document, replace_pending_content(pending, replacement))


def ensure_local_exclude(document: Path) -> str:
    """対象文書をGitローカル除外へ登録し、結果名を返す。"""

    try:
        root_result = subprocess.run(
            ["git", "-C", str(document.parent), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "not-git"
    root = Path(root_result.stdout.strip()).resolve()
    try:
        relative = document.resolve().relative_to(root)
    except ValueError:
        return "outside-root"

    try:
        path_result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--git-path", "info/exclude"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ProtocolError(f"cannot locate Git local exclude: {exc}") from exc
    exclude = Path(path_result.stdout.strip())
    if not exclude.is_absolute():
        exclude = root / exclude
    pattern = f"/{relative.as_posix()}"
    try:
        existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
        if pattern in {line.strip() for line in existing.splitlines()}:
            return "present"
        exclude.parent.mkdir(parents=True, exist_ok=True)
        prefix = existing
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        exclude.write_text(f"{prefix}{pattern}\n", encoding="utf-8")
    except OSError as exc:
        raise ProtocolError(f"cannot update Git local exclude: {exc}") from exc
    return "added"


def cleanup_document(document: Path) -> None:
    """引き渡し済みの終端文書だけを削除する。"""

    try:
        content = document.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProtocolError(f"cannot read document: {exc}") from exc
    if len(_line_marker_matches(content, STATE_MARKER)) != 1:
        raise ProtocolError("cleanup requires exactly one local-intake state marker")
    if _line_marker_matches(content, FORM_BEGIN) or _line_marker_matches(content, FORM_END):
        raise ProtocolError("cleanup refuses a document with a pending form")
    status_match = STATUS_RE.search(content)
    if not status_match or status_match.group(1) not in TERMINAL_STATUSES:
        raise ProtocolError("cleanup requires status agreed or unresolved")
    try:
        document.unlink()
    except OSError as exc:
        raise ProtocolError(f"cannot remove document: {exc}") from exc
