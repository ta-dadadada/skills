#!/usr/bin/env python3
"""HQ ledger CLI and read-only loopback dashboard for an adjutant session.

Every mutating command runs in one short SQLite transaction, appends one event,
rewrites <hq>/ledger.md atomically and prints a one-line JSON receipt. Errors
print {"ok": false, ...} and exit non-zero. HQ folder: --hq > $HQ_DIR > ~/hq.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys

ASSET = Path(__file__).resolve().parent.parent / "assets" / "dashboard.html"
DB_NAME = "ledger.sqlite3"
MD_NAME = "ledger.md"
TASK_STATUSES = ("queued", "active", "waiting-user", "blocked", "done", "dropped")
SESSION_STATES = ("starting", "working", "idle", "waiting-user", "blocked", "done", "archived")
EDGE_KINDS = ("depends_on", "spawned_from", "related")
WAIT_KINDS = ("approval", "decision", "review", "launch", "criteria")
NEED_KINDS = ("approval", "decision", "review")
ARTIFACT_KINDS = ("branch", "pr", "doc", "file", "url", "other")
REPORT_STATES = ("working", "waiting-user", "blocked", "done")
FINAL_TASK = ("done", "dropped")
LIVE_SESSION = ("starting", "working", "idle", "waiting-user", "blocked")
LIVE_SQL = "(" + ",".join(f"'{s}'" for s in LIVE_SESSION) + ")"
SUMMARY_LIMIT = 400
MD_EVENTS = 30
MD_FINISHED = 50
API_EVENTS = 200
API_RESOLVED_WAITS = 50
SCHEMA_VERSION = "2"  # 2: waits.source (report | manual)
MD_MARK_RE = re.compile(rb"<!-- hq-ledger revision (\d+) -->")
LANG_RE = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{1,8})*$")

SCHEMA = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE tasks (id TEXT PRIMARY KEY, num INTEGER NOT NULL, title TEXT NOT NULL,
  goal TEXT NOT NULL DEFAULT '', target TEXT NOT NULL, deliverable TEXT NOT NULL,
  done_criteria TEXT NOT NULL, authority TEXT NOT NULL DEFAULT '', status TEXT NOT NULL,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE sessions (id TEXT PRIMARY KEY, task_id TEXT, name TEXT NOT NULL DEFAULT '',
  title TEXT NOT NULL DEFAULT '', cwd TEXT NOT NULL DEFAULT '', branch TEXT NOT NULL DEFAULT '',
  state TEXT NOT NULL, summary TEXT NOT NULL DEFAULT '', reported_at TEXT,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE INDEX sessions_task ON sessions(task_id);
CREATE TABLE edges (from_task TEXT NOT NULL, kind TEXT NOT NULL, to_task TEXT NOT NULL,
  created_at TEXT NOT NULL, PRIMARY KEY (from_task, kind, to_task));
CREATE TABLE waits (id TEXT PRIMARY KEY, num INTEGER NOT NULL, kind TEXT NOT NULL, task_id TEXT,
  session_id TEXT, summary TEXT NOT NULL, status TEXT NOT NULL, resolution TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL, resolved_at TEXT, source TEXT NOT NULL DEFAULT 'manual');
CREATE INDEX waits_open ON waits(status, session_id);
CREATE TABLE artifacts (id TEXT PRIMARY KEY, num INTEGER NOT NULL, task_id TEXT NOT NULL,
  kind TEXT NOT NULL, label TEXT NOT NULL, ref TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE INDEX artifacts_ref ON artifacts(task_id, ref);
CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, type TEXT NOT NULL,
  task_id TEXT, session_id TEXT, text TEXT NOT NULL);
"""


class HQError(Exception):
    """A user-facing error reported as {"ok": false}."""


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def emit(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def one_line(text, limit=None):
    flat = " ".join(str(text or "").split())
    if limit and len(flat) > limit:
        flat = flat[: limit - 1] + "…"
    return flat


def text_param(p, key, required=False):
    value = p.get(key)
    if value is None:
        if required:
            raise HQError(f"missing {key}")
        return None
    if not isinstance(value, str):
        raise HQError(f"{key} must be text")
    value = value.strip()
    if required and not value:
        raise HQError(f"{key} must not be empty")
    return value


def enum_param(p, key, allowed, required=False, default=None):
    value = text_param(p, key, required)
    if value is None:
        return default
    if value not in allowed:
        raise HQError(f"invalid {key} '{value}'; expected one of: {', '.join(allowed)}")
    return value


# ---------------------------------------------------------------- storage

class Ledger:
    def __init__(self, hq):
        self.dir = Path(os.path.abspath(os.path.expanduser(hq)))
        self.db = self.dir / DB_NAME
        self.md = self.dir / MD_NAME

    def exists(self):
        return self.db.is_file()

    def connect(self):
        if not self.exists():
            raise HQError(f"no ledger at {self.dir}; run init")
        c = sqlite3.connect(self.db, timeout=10, isolation_level=None)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA synchronous=NORMAL")
        return c

    def init(self, lang):
        if self.exists():
            c = self.connect()
            try:
                current = get_meta(c, "lang")
            finally:
                c.close()
            receipt = {"ok": True, "created": False, "hq": str(self.dir), "lang": current}
            if lang and lang != current:
                receipt["note"] = "existing ledger kept; use the lang command to change the language"
            return receipt
        lang = check_lang(lang or "en")
        self.dir.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.db, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
        c = sqlite3.connect(self.db, isolation_level=None)
        try:
            c.execute("PRAGMA journal_mode=WAL")
            c.execute("BEGIN IMMEDIATE")
            for statement in SCHEMA.split(";"):
                if statement.strip():
                    c.execute(statement)
            ts = now()
            for key, value in (("schema", SCHEMA_VERSION), ("lang", lang), ("revision", "1"), ("created_at", ts),
                               ("next_T", "1"), ("next_W", "1"), ("next_A", "1")):
                c.execute("INSERT INTO meta VALUES (?, ?)", (key, value))
            add_event(c, "init", f"ledger created (lang {lang})")
            c.execute("COMMIT")
        except BaseException:
            if c.in_transaction:
                c.execute("ROLLBACK")
            c.close()
            self.db.unlink(missing_ok=True)
            raise
        c.close()
        receipt = {"ok": True, "created": True, "hq": str(self.dir), "lang": lang}
        self.refresh_md_or_warn([receipt])
        return receipt

    def mutate(self, ops):
        """Run (name, function, params) ops in ONE transaction; all-or-nothing."""
        c = self.connect()
        try:
            c.execute("BEGIN IMMEDIATE")
            if get_meta(c, "schema") != SCHEMA_VERSION:
                migrate(c)
            results = []
            for index, (name, fn, params) in enumerate(ops):
                try:
                    results.append(fn(c, params))
                except HQError as exc:
                    if len(ops) > 1:
                        raise HQError(f"op {index} ({name}): {exc}") from None
                    raise
            set_meta(c, "revision", str(int(get_meta(c, "revision")) + 1))
            c.execute("COMMIT")
        except BaseException:
            if c.in_transaction:
                c.execute("ROLLBACK")
            raise
        finally:
            c.close()
        self.refresh_md_or_warn(results)   # only committed state reaches ledger.md
        return results

    def refresh_md(self, force=False):
        """Rewrite ledger.md from a committed snapshot; returns False if a newer file was kept.

        Writers are serialized with a lock file and read the snapshot after taking
        the lock, so a later writer always renders state at least as new. The
        revision marker on the first line is a second guard (and the only one
        where flock is unavailable): an older snapshot never replaces a newer file.
        """
        try:
            import fcntl
        except ImportError:  # pragma: no cover - non-POSIX
            fcntl = None
        lock = os.open(self.dir / f".{MD_NAME}.lock", os.O_CREAT | os.O_RDWR, 0o600)
        try:
            if fcntl:
                fcntl.flock(lock, fcntl.LOCK_EX)
            revision, content = self.read(lambda c: (int(get_meta(c, "revision", "0")), render_md(c, self.dir)))
            if not force:
                try:
                    with open(self.md, "rb") as fh:
                        mark = MD_MARK_RE.match(fh.read(64))
                except FileNotFoundError:
                    mark = None
                if mark and int(mark.group(1)) > revision:
                    return False
            temp = self.dir / f".{MD_NAME}.{os.getpid()}.tmp"
            fd = os.open(temp, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
            try:
                os.write(fd, content.encode("utf-8"))
            finally:
                os.close(fd)
            os.replace(temp, self.md)
            return True
        finally:
            os.close(lock)  # also releases the flock

    def refresh_md_or_warn(self, receipts):
        try:
            self.refresh_md()
        except (OSError, sqlite3.Error) as exc:
            for receipt in receipts:
                receipt.setdefault("warnings", []).append(f"ledger.md not rewritten: {exc}")

    def read(self, fn):
        c = self.connect()
        try:
            c.execute("BEGIN")
            return fn(c)
        finally:
            if c.in_transaction:
                c.execute("ROLLBACK")
            c.close()


def get_meta(c, key, default=None):
    row = c.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row[0] if row else default


def set_meta(c, key, value):
    c.execute("INSERT INTO meta VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
              (key, value))


def migrate(c):
    """Upgrade an older ledger inside the caller's write transaction."""
    if get_meta(c, "schema", "1") == "1":
        # Origin of existing waits: those recorded by `wait add` left a wait.add event that
        # starts with their id; the rest of the approval/decision/review waits with a session
        # can only have come from `report`.
        c.execute("ALTER TABLE waits ADD COLUMN source TEXT NOT NULL DEFAULT 'manual'")
        c.execute("UPDATE waits SET source='report' WHERE kind IN ('approval','decision','review')"
                  " AND session_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM events e WHERE e.type='wait.add'"
                  " AND (e.text = waits.id OR e.text LIKE waits.id || ' %'))")
    set_meta(c, "schema", SCHEMA_VERSION)


def next_id(c, prefix):
    n = int(get_meta(c, f"next_{prefix}", "1"))
    set_meta(c, f"next_{prefix}", str(n + 1))
    return f"{prefix}{n}", n


def add_event(c, kind, text, task=None, session=None):
    cur = c.execute("INSERT INTO events (ts, type, task_id, session_id, text) VALUES (?, ?, ?, ?, ?)",
                    (now(), kind, task, session, one_line(text, 500)))
    return cur.lastrowid


def check_lang(code):
    code = (code or "").strip()
    if not LANG_RE.match(code):
        raise HQError(f"invalid language code '{code}'; use a BCP 47 tag such as en or ja")
    return code


def need_task(c, task_id):
    row = c.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if row is None:
        raise HQError(f"unknown task {task_id}")
    return row


def need_session(c, session_id):
    row = c.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
    if row is None:
        raise HQError(f"unknown session {session_id}")
    return row


# ---------------------------------------------------------------- mutations
# Each op takes (connection, params) and returns its receipt. CLI subcommands and
# `apply` share them; params keys mirror the CLI flag names in snake_case.

TASK_FIELDS = (("title", "title"), ("goal", "goal"), ("target", "target"),
               ("deliverable", "deliverable"), ("done", "done_criteria"), ("authority", "authority"))


def op_task_add(c, p):
    values = {col: text_param(p, key, key in ("title", "target", "deliverable", "done")) or ""
              for key, col in TASK_FIELDS}
    status = enum_param(p, "status", TASK_STATUSES, default="queued")
    task_id, num = next_id(c, "T")
    ts = now()
    c.execute("INSERT INTO tasks (id, num, title, goal, target, deliverable, done_criteria, authority,"
              " status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (task_id, num, values["title"], values["goal"], values["target"], values["deliverable"],
               values["done_criteria"], values["authority"], status, ts, ts))
    add_event(c, "task.add", f"{task_id} [{status}] {values['title']} ({values['target']})", task_id)
    return {"ok": True, "id": task_id, "status": status}


def op_task_update(c, p):
    task_id = text_param(p, "id", True)
    row = need_task(c, task_id)
    changes = {}
    for key, col in TASK_FIELDS:
        value = text_param(p, key)
        if value is not None and value != row[col]:
            if key in ("title", "target", "deliverable", "done") and not value:
                raise HQError(f"{key} must not be empty")
            changes[col] = value
    status = enum_param(p, "status", TASK_STATUSES)
    if status is not None and status != row["status"]:
        changes["status"] = status
    if changes:
        changes["updated_at"] = now()
        c.execute(f"UPDATE tasks SET {', '.join(f'{k}=?' for k in changes)} WHERE id=?",
                  (*changes.values(), task_id))
    changed = [k for k in changes if k != "updated_at"]
    detail = f"status {row['status']}→{status}" if "status" in changes else ""
    others = [k for k in changed if k != "status"]
    text = " ".join(x for x in (detail, ("updated " + ", ".join(others)) if others else "") if x)
    receipt = {"ok": True, "id": task_id, "status": changes.get("status", row["status"]), "changed": changed}
    if status in FINAL_TASK:
        # Closing a task closes what hangs off it: its open waits and its live sessions.
        waits = [r[0] for r in c.execute("SELECT id FROM waits WHERE status='open' AND task_id=? ORDER BY num",
                                         (task_id,))]
        for wait_id in waits:
            resolve_wait(c, wait_id, f"task closed: {status}")
        sessions = [r[0] for r in c.execute(f"SELECT id FROM sessions WHERE task_id=? AND state IN {LIVE_SQL}"
                                            " ORDER BY created_at, id", (task_id,))]
        if sessions:
            c.execute(f"UPDATE sessions SET state='done', updated_at=? WHERE task_id=? AND state IN {LIVE_SQL}",
                      (now(), task_id))
        receipt.update(waits_resolved=waits, sessions_closed=sessions)
        if waits or sessions:
            text += f"; resolved {', '.join(waits) or '-'}; closed sessions {', '.join(sessions) or '-'}"
    add_event(c, "task.update", f"{task_id} {text.strip('; ') or 'no change'}", task_id)
    return receipt


def upsert_session(c, sid, task_id, p, state_default="starting"):
    """Insert or update a session; returns (created, state)."""
    fields = {k: text_param(p, k) for k in ("name", "title", "cwd", "branch")}
    state = enum_param(p, "state", SESSION_STATES)
    summary = text_param(p, "summary")
    ts = now()
    row = c.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
    if row is None:
        state = state or state_default
        c.execute("INSERT INTO sessions (id, task_id, name, title, cwd, branch, state, summary,"
                  " reported_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (sid, task_id, fields["name"] or "", fields["title"] or "", fields["cwd"] or "",
                   fields["branch"] or "", state, (summary or "")[:SUMMARY_LIMIT],
                   ts if summary else None, ts, ts))
        return True, state
    changes = {k: v for k, v in fields.items() if v is not None}
    if task_id is not None:
        changes["task_id"] = task_id
    if state is not None:
        changes["state"] = state
    if summary is not None:
        changes["summary"] = summary[:SUMMARY_LIMIT]
        changes["reported_at"] = ts
    changes["updated_at"] = ts
    c.execute(f"UPDATE sessions SET {', '.join(f'{k}=?' for k in changes)} WHERE id=?",
              (*changes.values(), sid))
    return False, state or row["state"]


def op_session_upsert(c, p):
    sid = text_param(p, "id", True)
    task_id = text_param(p, "task", True)
    need_task(c, task_id)
    created, state = upsert_session(c, sid, task_id, p)
    add_event(c, "session.upsert", f"{sid} {'created' if created else 'updated'} [{state}] for {task_id}",
              task_id, sid)
    return {"ok": True, "id": sid, "task": task_id, "state": state, "created": created}


def edge_params(c, p):
    src = text_param(p, "from", True)
    kind = enum_param(p, "kind", EDGE_KINDS, True)
    dst = text_param(p, "to", True)
    need_task(c, src)
    need_task(c, dst)
    if src == dst:
        raise HQError("an edge needs two different tasks")
    return src, kind, dst


def op_edge_add(c, p):
    src, kind, dst = edge_params(c, p)
    cur = c.execute("INSERT OR IGNORE INTO edges VALUES (?, ?, ?, ?)", (src, kind, dst, now()))
    created = cur.rowcount == 1
    add_event(c, "edge.add", f"{src} {kind} {dst}{'' if created else ' (already present)'}", src)
    return {"ok": True, "edge": [src, kind, dst], "created": created}


def op_edge_remove(c, p):
    src, kind, dst = edge_params(c, p)
    cur = c.execute("DELETE FROM edges WHERE from_task=? AND kind=? AND to_task=?", (src, kind, dst))
    if cur.rowcount == 0:
        raise HQError(f"no edge {src} {kind} {dst}")
    add_event(c, "edge.remove", f"{src} {kind} {dst} removed", src)
    return {"ok": True, "edge": [src, kind, dst], "removed": True}


def insert_wait(c, kind, summary, task_id, session_id, source="manual"):
    wait_id, num = next_id(c, "W")
    c.execute("INSERT INTO waits (id, num, kind, task_id, session_id, summary, status, created_at, source)"
              " VALUES (?, ?, ?, ?, ?, ?, 'open', ?, ?)",
              (wait_id, num, kind, task_id, session_id, summary, now(), source))
    return wait_id


def resolve_wait(c, wait_id, resolution):
    c.execute("UPDATE waits SET status='resolved', resolution=?, resolved_at=? WHERE id=?",
              (resolution, now(), wait_id))


def op_wait_add(c, p):
    kind = enum_param(p, "kind", WAIT_KINDS, True)
    summary = text_param(p, "summary", True)
    task_id = text_param(p, "task") or None
    session_id = text_param(p, "session") or None
    if task_id:
        need_task(c, task_id)
    if session_id:
        need_session(c, session_id)
    existing = c.execute("SELECT id FROM waits WHERE status='open' AND kind=? AND summary=?"
                         " AND task_id IS ? AND session_id IS ?",
                         (kind, summary, task_id, session_id)).fetchone()
    if existing:
        add_event(c, "wait.add", f"{existing[0]} [{kind}] already open", task_id, session_id)
        return {"ok": True, "id": existing[0], "kind": kind, "created": False}
    wait_id = insert_wait(c, kind, summary, task_id, session_id)
    add_event(c, "wait.add", f"{wait_id} [{kind}] {summary}", task_id, session_id)
    return {"ok": True, "id": wait_id, "kind": kind, "created": True}


def op_wait_resolve(c, p):
    wait_id = text_param(p, "id", True)
    resolution = text_param(p, "resolution") or "resolved"
    row = c.execute("SELECT * FROM waits WHERE id=?", (wait_id,)).fetchone()
    if row is None:
        raise HQError(f"unknown wait {wait_id}")
    if row["status"] == "resolved":
        add_event(c, "wait.resolve", f"{wait_id} already resolved; kept: {row['resolution']}",
                  row["task_id"], row["session_id"])
        return {"ok": True, "id": wait_id, "status": "resolved", "already_resolved": True,
                "resolution": row["resolution"]}
    resolve_wait(c, wait_id, resolution)
    add_event(c, "wait.resolve", f"{wait_id} [{row['kind']}] {resolution}", row["task_id"], row["session_id"])
    return {"ok": True, "id": wait_id, "status": "resolved", "kind": row["kind"], "task": row["task_id"],
            "session": row["session_id"]}


def insert_artifact(c, task_id, kind, label, ref):
    """Add an artifact unless the task already has one with this ref; returns (id, created)."""
    existing = c.execute("SELECT id FROM artifacts WHERE task_id=? AND ref=?", (task_id, ref)).fetchone()
    if existing:
        return existing[0], False
    art_id, num = next_id(c, "A")
    c.execute("INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?, ?)", (art_id, num, task_id, kind, label, ref, now()))
    return art_id, True


def op_artifact_add(c, p):
    task_id = text_param(p, "task", True)
    need_task(c, task_id)
    kind = enum_param(p, "kind", ARTIFACT_KINDS, True)
    label = text_param(p, "label", True)
    ref = text_param(p, "ref", True)
    art_id, created = insert_artifact(c, task_id, kind, label, ref)
    add_event(c, "artifact.add", f"{art_id} [{kind}] {label}{'' if created else ' (already recorded)'}", task_id)
    return {"ok": True, "id": art_id, "created": created}


def op_note(c, p):
    text = text_param(p, "text", True)
    task_id = text_param(p, "task") or None
    session_id = text_param(p, "session") or None
    if task_id:
        need_task(c, task_id)
    if session_id:
        need_session(c, session_id)
    event_id = add_event(c, "note", text, task_id, session_id)
    return {"ok": True, "event": event_id}


def op_lang(c, p):
    code = check_lang(text_param(p, "code", True))
    set_meta(c, "lang", code)
    add_event(c, "lang", f"language set to {code}")
    return {"ok": True, "lang": code}


def op_launch(c, p):
    task_id = text_param(p, "id", True)
    sid = text_param(p, "session", True)
    task = need_task(c, task_id)
    if task["status"] in FINAL_TASK:
        raise HQError(f"{task_id} is {task['status']}; set it back with task update {task_id} --status queued"
                      " before launching")
    created, _ = upsert_session(c, sid, task_id, {**{k: p.get(k) for k in ("name", "title", "cwd", "branch")},
                                                  "state": "starting"})
    resolved = [r[0] for r in c.execute(
        "SELECT id FROM waits WHERE status='open' AND task_id=? AND kind IN ('criteria','launch') ORDER BY num",
        (task_id,))]
    for wait_id in resolved:
        resolve_wait(c, wait_id, f"launched as {sid}")
    pending = c.execute("SELECT 1 FROM waits WHERE status='open' AND task_id=?"
                        " AND kind IN ('approval','decision','review') LIMIT 1", (task_id,)).fetchone()
    status = "waiting-user" if pending else "active"
    if task["status"] != status:
        c.execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?", (status, now(), task_id))
    add_event(c, "launch", f"{task_id} launched as {sid}" + (f" ({p.get('name')})" if p.get("name") else ""),
              task_id, sid)
    return {"ok": True, "task": task_id, "session": sid, "state": "starting", "task_status": status,
            "created": created, "waits_resolved": resolved}


# ---------------------------------------------------------------- report parsing

STATUS_RE = re.compile(r"\bHQ\s+T(\d+)\s+(working|waiting-user|blocked|done)\s*:", re.I)
NEEDS_RE = re.compile(r"\bNeeds\s*:")
ARTS_RE = re.compile(r"\bArtifacts\s*:")
# List markers a writer may put before an item: "1)", "1.", "(a)", "-", "*", "•", "・", "①".
LIST = r"(?:[-*•・]|\(?\d{1,2}[.)]|\(?[a-z][.)]|[①-⑳])"
KIND = r"(?:approval|decision|review)\s*:"
NEED_SPLIT_RE = re.compile(rf"(?:[;；,，、\n]\s*|\s+(?={LIST}\s*{KIND}))(?=(?:{LIST}\s*)?{KIND})", re.I)
NEED_ITEM_RE = re.compile(rf"\s*(?:{LIST}\s*)?(approval|decision|review)\s*:\s*(.*)$", re.I | re.S)
LIST_PREFIX_RE = re.compile(rf"^\s*{LIST}\s+")
# Items split on ", " / "; " (punctuation followed by whitespace), on 、 ， ；, or on line breaks,
# so a URL such as https://x.y/a,b stays one token.
ART_SPLIT_RE = re.compile(r"\s*(?:[,;](?=\s)|[、，；\n])\s*")
ART_KEY_RE = re.compile(r"(PR|branch|doc)\b[\s:]*(.*)$", re.I | re.S)
URL_RE = re.compile(r"https?://[^\s<>\"'（）「」、]+", re.I)
NONE_WORDS = ("none", "なし", "無し")
TRAIL = " \t.。;；,，、*`"


def normalize(text):
    return text.replace("　", " ").replace(" ", " ").replace("：", ":").replace("\r\n", "\n")


def clean(text):
    return (text or "").strip(" \t*`").rstrip(TRAIL).strip()


def segment(region, start, stop):
    """Text of a Needs/Artifacts segment: the rest of its line, or, when that is empty,
    the following non-blank lines (a list written under the keyword)."""
    value = region[start:stop]
    if value.strip() or stop < len(region) and region[stop] != "\n":
        return value
    lines = []
    for line in region[stop + 1:].split("\n"):
        if not line.strip() or NEEDS_RE.search(line) or ARTS_RE.search(line):
            break
        lines.append(line.strip())
    return "\n".join(lines)


def parse_report(text):
    """Return the parsed HQ status line with its Needs/Artifacts, or None if there is none.

    Needs: and Artifacts: may sit on the status line or anywhere after it (blank
    lines allowed) up to the next "HQ T<n>" status line.
    """
    t = normalize(text)
    m = STATUS_RE.search(t)
    if not m:
        return None
    nxt = STATUS_RE.search(t, m.end())
    region = t[m.end(): nxt.start() if nxt else len(t)]
    first_end = region.find("\n")
    first_end = len(region) if first_end < 0 else first_end
    marks = sorted((mm.start(), mm.end(), name) for name, rx in (("needs", NEEDS_RE), ("artifacts", ARTS_RE))
                   for mm in [rx.search(region)] if mm)
    segs = {}
    for i, (_, seg_start, name) in enumerate(marks):
        line_end = region.find("\n", seg_start)
        line_end = len(region) if line_end < 0 else line_end
        stop = min(line_end, marks[i + 1][0]) if i + 1 < len(marks) else line_end
        segs[name] = clean(segment(region, seg_start, stop))
    inline = [mk[0] for mk in marks if mk[0] < first_end]
    result = clean(region[: inline[0] if inline else first_end])
    line = region[:first_end]
    return {"task": f"T{int(m.group(1))}", "state": m.group(2).lower(), "result": result,
            "needs": segs.get("needs"), "artifacts": segs.get("artifacts"),
            "line": one_line(f"HQ T{int(m.group(1))} {m.group(2).lower()}: {line.strip()}", 300)}


def is_none(text):
    return clean(LIST_PREFIX_RE.sub("", text or "")).casefold() in NONE_WORDS


def parse_needs(text, fallback):
    """None-word → []; known kinds → [(kind, summary)]; anything else → None."""
    if is_none(text):
        return []
    items = []
    for part in NEED_SPLIT_RE.split(text):
        m = NEED_ITEM_RE.match(part)
        if m:
            items.append((m.group(1).lower(), clean(m.group(2)) or fallback or m.group(1).lower()))
    return items or None


def parse_artifacts(text):
    if not text or is_none(text):
        return []
    found = []
    for raw in ART_SPLIT_RE.split(text):
        item = clean(LIST_PREFIX_RE.sub("", raw))
        if not item or item.casefold() in NONE_WORDS:
            continue
        url = URL_RE.search(item)
        url = url.group(0).rstrip(".,;:)]。") if url else None
        key = ART_KEY_RE.match(item)
        word = key.group(1).lower() if key else ""
        rest = clean(key.group(2)) if key else ""
        if word == "pr" or (url and "/pull/" in url):
            found.append(("pr", item, url or rest or item))
        elif word == "branch":
            found.append(("branch", item, (rest.split() or [item])[0]))
        elif word == "doc":
            found.append(("doc", item, url or rest or item))
        elif url:
            found.append(("url", item, url))
        else:
            found.append(("other", item, item))
    return found


def same_summary(a, b):
    return " ".join(a.split()).casefold() == " ".join(b.split()).casefold()


def op_report(c, p):
    sid = text_param(p, "session", True)
    raw = p.get("text")
    if not isinstance(raw, str) or not raw.strip():
        raise HQError("report text is empty; pass --text or pipe the note on stdin")
    explicit = text_param(p, "task") or None
    if explicit:
        need_task(c, explicit)
    session = c.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
    parsed = parse_report(raw)
    warnings = []
    # Task precedence: explicit --task > the session's existing mapping > the report line.
    # A report never silently moves a session to another task.
    mapped = session["task_id"] if session else None
    line_task = parsed["task"] if parsed else None
    line_known = bool(line_task and c.execute("SELECT 1 FROM tasks WHERE id=?", (line_task,)).fetchone())
    task_id = explicit or mapped or (line_task if line_known else None)
    if explicit and mapped and explicit != mapped:
        warnings.append(f"session {sid} moved from {mapped} to {explicit} by --task")
    if parsed and line_task != task_id:
        if task_id:
            warnings.append(f"report line names {line_task}{'' if line_known else ' (unknown)'} but session {sid}"
                            f" belongs to {task_id}; recorded under {task_id}")
        else:
            warnings.append(f"report line names unknown task {line_task}; recorded as unparsed")
            parsed = None
    summary = raw.strip()[:SUMMARY_LIMIT]
    ts = now()
    if session is None:
        state = parsed["state"] if parsed else "idle"
        c.execute("INSERT INTO sessions (id, task_id, state, summary, reported_at, created_at, updated_at)"
                  " VALUES (?, ?, ?, ?, ?, ?, ?)", (sid, task_id, state, summary, ts, ts, ts))
        warnings.append(f"session {sid} was not in the ledger; created" + ("" if task_id else " without a task"))
    else:
        state = parsed["state"] if parsed else session["state"]
        c.execute("UPDATE sessions SET task_id=?, state=?, summary=?, reported_at=?, updated_at=? WHERE id=?",
                  (task_id, state, summary, ts, ts, sid))
    opened, resolved, added = [], [], []
    if parsed:
        needs = None
        if parsed["needs"] is None:
            warnings.append("no Needs: segment; open waits left unchanged")
        else:
            needs = parse_needs(parsed["needs"], parsed["result"])
            if needs is None:
                warnings.append(f"Needs not understood ({one_line(parsed['needs'], 80)}); open waits left unchanged")
        if needs is not None:
            open_rows = c.execute("SELECT id, kind, summary, source FROM waits WHERE status='open'"
                                  " AND session_id=? AND kind IN ('approval','decision','review') ORDER BY num",
                                  (sid,)).fetchall()
            kept = set()
            for kind, text in needs:
                match = next((r for r in open_rows if r["kind"] == kind and same_summary(r["summary"], text)
                              and r["id"] not in kept), None)
                if match:
                    kept.add(match["id"])
                    continue
                wait_id = insert_wait(c, kind, text, task_id, sid, source="report")
                kept.add(wait_id)
                opened.append({"id": wait_id, "kind": kind, "summary": text})
            for r in open_rows:   # waits recorded with `wait add` are never superseded by a report
                if r["id"] not in kept and r["source"] == "report":
                    resolve_wait(c, r["id"], "superseded by report")
                    resolved.append(r["id"])
        if parsed["artifacts"] is not None:
            items = parse_artifacts(parsed["artifacts"])
            if items and not task_id:
                warnings.append("artifacts not recorded: session has no task")
            elif items:
                for kind, label, ref in items:
                    art_id, created = insert_artifact(c, task_id, kind, label, ref)
                    if created:
                        added.append(art_id)
        if task_id:
            task = need_task(c, task_id)
            if task["status"] not in FINAL_TASK:
                pending = c.execute("SELECT 1 FROM waits WHERE status='open' AND task_id=?"
                                    " AND kind IN ('approval','decision','review') LIMIT 1", (task_id,)).fetchone()
                if pending or (needs is None and parsed["state"] == "waiting-user"):
                    status = "waiting-user"
                elif parsed["state"] == "blocked":
                    status = "blocked"
                else:
                    status = "active"
                if status != task["status"]:
                    c.execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?", (status, ts, task_id))
    text = parsed["line"] if parsed else "unparsed report: " + one_line(raw, 160)
    add_event(c, "report", text, task_id, sid)
    receipt = {"ok": True, "task": task_id, "session": sid, "state": state, "parsed": parsed is not None,
               "waits_opened": opened, "waits_resolved": resolved, "artifacts_added": added}
    if warnings:
        receipt["warnings"] = warnings
    return receipt


# op name → (function, required keys, optional keys)
OPS = {
    "task.add": (op_task_add, {"title", "target", "deliverable", "done"}, {"goal", "authority", "status"}),
    "task.update": (op_task_update, {"id"}, {"title", "goal", "target", "deliverable", "done", "authority",
                                             "status"}),
    "session.upsert": (op_session_upsert, {"id", "task"}, {"name", "title", "cwd", "branch", "state", "summary"}),
    "edge.add": (op_edge_add, {"from", "kind", "to"}, set()),
    "edge.remove": (op_edge_remove, {"from", "kind", "to"}, set()),
    "wait.add": (op_wait_add, {"kind", "summary"}, {"task", "session"}),
    "wait.resolve": (op_wait_resolve, {"id"}, {"resolution"}),
    "artifact.add": (op_artifact_add, {"task", "kind", "label", "ref"}, set()),
    "note": (op_note, {"text"}, {"task", "session"}),
    "report": (op_report, {"session", "text"}, {"task"}),
    "launch": (op_launch, {"id", "session"}, {"name", "cwd", "branch", "title"}),
    "lang": (op_lang, {"code"}, set()),
}


def batch_ops(data):
    if not isinstance(data, list) or not data:
        raise HQError("apply expects a non-empty JSON array of op objects")
    ops = []
    for index, item in enumerate(data):
        if not isinstance(item, dict) or not isinstance(item.get("op"), str):
            raise HQError(f"op {index}: expected an object with an \"op\" name")
        name = item["op"]
        if name not in OPS:
            raise HQError(f"op {index}: unknown op '{name}'; expected one of: {', '.join(OPS)}")
        fn, required, optional = OPS[name]
        params = {k: v for k, v in item.items() if k != "op"}
        unknown = set(params) - required - optional
        if unknown:
            raise HQError(f"op {index} ({name}): unknown keys: {', '.join(sorted(unknown))}")
        missing = required - set(params)
        if missing:
            raise HQError(f"op {index} ({name}): missing keys: {', '.join(sorted(missing))}")
        bad = [k for k, v in params.items() if v is not None and not isinstance(v, str)]
        if bad:
            raise HQError(f"op {index} ({name}): values must be strings: {', '.join(sorted(bad))}")
        ops.append((name, fn, params))
    return ops


# ---------------------------------------------------------------- reading

def rows(c, sql, args=()):
    return [dict(r) for r in c.execute(sql, args)]


def snapshot(c, events_limit=API_EVENTS):
    events_total = c.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    return {
        "revision": int(get_meta(c, "revision", "0")),
        "lang": get_meta(c, "lang", "en"),
        "generated_at": now(),
        "server_url": get_meta(c, "server_url"),
        "tasks": rows(c, "SELECT * FROM tasks ORDER BY num"),
        "sessions": rows(c, "SELECT * FROM sessions ORDER BY created_at, id"),
        "edges": rows(c, "SELECT from_task AS 'from', kind, to_task AS 'to' FROM edges ORDER BY created_at"),
        "waits": rows(c, "SELECT * FROM waits WHERE status='open' ORDER BY num")
        + rows(c, "SELECT * FROM waits WHERE status='resolved' ORDER BY resolved_at DESC, num DESC LIMIT ?",
               (API_RESOLVED_WAITS,)),
        "artifacts": rows(c, "SELECT * FROM artifacts ORDER BY num"),
        "events": rows(c, "SELECT * FROM events ORDER BY id DESC LIMIT ?", (events_limit,)),
        "events_total": events_total,
    }


def status_data(c):
    open_waits = rows(c, "SELECT id, kind, task_id, session_id, summary, created_at FROM waits"
                         " WHERE status='open' ORDER BY num")
    counts = {s: 0 for s in TASK_STATUSES}
    for r in c.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status"):
        counts[r[0]] = r[1]
    live = rows(c, "SELECT * FROM tasks WHERE status NOT IN ('done','dropped') ORDER BY num")
    for task in live:
        task["sessions"] = rows(c, "SELECT id, name, state, branch, cwd, summary, reported_at FROM sessions"
                                   " WHERE task_id=? ORDER BY created_at", (task["id"],))
        task["artifacts"] = rows(c, "SELECT id, kind, label, ref FROM artifacts WHERE task_id=? ORDER BY num",
                                 (task["id"],))
        task["edges_out"] = rows(c, "SELECT kind, to_task AS 'to' FROM edges WHERE from_task=?", (task["id"],))
        task["edges_in"] = rows(c, "SELECT from_task AS 'from', kind FROM edges WHERE to_task=?", (task["id"],))
    active_sessions = c.execute("SELECT COUNT(*) FROM sessions WHERE state IN"
                                " ('starting','working','idle','waiting-user','blocked')").fetchone()[0]
    return {
        "ok": True, "lang": get_meta(c, "lang", "en"), "revision": int(get_meta(c, "revision", "0")),
        "server_url": get_meta(c, "server_url"), "counts": counts, "active_sessions": active_sessions,
        "open_waits": open_waits, "tasks": live,
        "finished_tasks": rows(c, "SELECT id, title, status, target FROM tasks WHERE status IN ('done','dropped')"
                                  " ORDER BY num"),
    }


def probe_server(url, revision):
    """Return True when an hq.py server answers /api/state at url."""
    m = re.match(r"http://127\.0\.0\.1:(\d+)/", url or "")
    if not m:
        return False
    import socket
    port = int(m.group(1))
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.5) as sock:
            sock.settimeout(1.0)
            sock.sendall(f"GET /api/state?since={revision} HTTP/1.0\r\nHost: 127.0.0.1:{port}\r\n\r\n".encode())
            data = b""
            while len(data) < 4096:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                data += chunk
    except OSError:
        return False
    return data.startswith(b"HTTP/1.") and b" 200 " in data[:20] and b'"revision"' in data


def status_text(data, hq):
    counts = ", ".join(f"{k} {v}" for k, v in data["counts"].items() if v) or "no tasks"
    server = data.get("server_url") or "never started"
    if data.get("server_url"):
        server += " (up)" if data.get("server_alive") else " (down: restart serve)"
    out = [f"HQ {hq} · lang {data['lang']} · revision {data['revision']} · dashboard {server}",
           f"Tasks: {counts} · active sessions {data['active_sessions']}",
           f"Open waits ({len(data['open_waits'])}):"]
    for w in data["open_waits"]:
        where = " ".join(x for x in (w["task_id"], w["session_id"]) if x)
        out.append(f"  {w['id']} [{w['kind']}] {where}: {one_line(w['summary'], 200)}")
    if not data["open_waits"]:
        out.append("  none")
    out.append("Tasks not done:")
    for t in data["tasks"]:
        out.append(f"  {t['id']} [{t['status']}] {t['title']} · target {t['target']}")
        for label, key in (("goal", "goal"), ("deliverable", "deliverable"), ("done when", "done_criteria"),
                           ("authority", "authority")):
            if t[key]:
                out.append(f"    {label}: {one_line(t[key])}")
        edges = [f"{e['kind']} {e['to']}" for e in t["edges_out"]] + \
                [f"{e['from']} {e['kind']} this" for e in t["edges_in"]]
        if edges:
            out.append(f"    edges: {'; '.join(edges)}")
        for s in t["sessions"]:
            name = f" ({s['name']})" if s["name"] else ""
            out.append(f"    session {s['id']}{name} [{s['state']}] reported {s['reported_at'] or '-'}: "
                       f"{one_line(s['summary'], 160) or '-'}")
        for a in t["artifacts"]:
            out.append(f"    artifact {a['id']} [{a['kind']}] {a['ref']}")
    if not data["tasks"]:
        out.append("  none")
    if data["finished_tasks"]:
        out.append("Finished: " + ", ".join(f"{t['id']} [{t['status']}]" for t in data["finished_tasks"]))
    return "\n".join(out)


# ---------------------------------------------------------------- ledger.md

def md_field(label, value):
    lines = [ln.rstrip() for ln in str(value).strip().splitlines() if ln.strip()] or ["-"]
    return [f"- {label}: {lines[0]}"] + [f"  {ln}" for ln in lines[1:]]


def render_md(c, hq_dir):
    revision = get_meta(c, "revision", "0")
    out = [f"<!-- hq-ledger revision {revision} -->", "# HQ ledger", "",
           "Auto-generated by hq.py after every change; do not edit. State of record: ledger.sqlite3.", "",
           f"- HQ folder: {hq_dir}", f"- Language: {get_meta(c, 'lang', 'en')}",
           f"- Revision: {revision} · written {now()}"]
    if get_meta(c, "server_url"):
        out.append(f"- Dashboard: {get_meta(c, 'server_url')} (last started {get_meta(c, 'server_started_at')})")
    waits = rows(c, "SELECT * FROM waits WHERE status='open' ORDER BY num")
    out += ["", f"## Waiting for you ({len(waits)})", ""]
    for w in waits:
        where = " · ".join(x for x in (w["task_id"], w["session_id"] and f"session {w['session_id']}") if x)
        out.append(f"- {w['id']} [{w['kind']}] {where} · {w['created_at']}: {one_line(w['summary'])}")
    if not waits:
        out.append("- none")
    tasks = rows(c, "SELECT * FROM tasks WHERE status NOT IN ('done','dropped') ORDER BY num")
    out += ["", f"## Tasks not done ({len(tasks)})"]
    for t in tasks:
        out += ["", f"### {t['id']} [{t['status']}] {one_line(t['title'])}", ""]
        out += md_field("Target", t["target"]) + md_field("Goal", t["goal"] or "-")
        out += md_field("Deliverable", t["deliverable"]) + md_field("Done when", t["done_criteria"])
        out += md_field("Authority", t["authority"] or "-")
        edges = [f"{e['kind']} {e['to_task']}" for e in
                 rows(c, "SELECT kind, to_task FROM edges WHERE from_task=?", (t["id"],))]
        edges += [f"{e['from_task']} {e['kind']} this" for e in
                  rows(c, "SELECT from_task, kind FROM edges WHERE to_task=?", (t["id"],))]
        out.append(f"- Edges: {'; '.join(edges) or '-'}")
        sessions = rows(c, "SELECT * FROM sessions WHERE task_id=? ORDER BY created_at", (t["id"],))
        out.append("- Sessions:" + ("" if sessions else " -"))
        for s in sessions:
            extra = " · ".join(x for x in (s["name"], s["branch"] and f"branch {s['branch']}",
                                            s["cwd"] and f"cwd {s['cwd']}") if x)
            out.append(f"  - {s['id']} [{s['state']}]{' ' + extra if extra else ''} · reported "
                       f"{s['reported_at'] or '-'}: {one_line(s['summary']) or '-'}")
        arts = rows(c, "SELECT * FROM artifacts WHERE task_id=? ORDER BY num", (t["id"],))
        out.append("- Artifacts:" + ("" if arts else " -"))
        for a in arts:
            out.append(f"  - {a['id']} [{a['kind']}] {one_line(a['label'])} → {a['ref']}")
    finished = rows(c, "SELECT id, title, status, target, updated_at FROM tasks WHERE status IN ('done','dropped')"
                       " ORDER BY updated_at DESC LIMIT ?", (MD_FINISHED,))
    total_finished = c.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('done','dropped')").fetchone()[0]
    out += ["", f"## Finished tasks ({total_finished})", ""]
    for t in finished:
        out.append(f"- {t['id']} [{t['status']}] {one_line(t['title'])} · {t['target']} · {t['updated_at']}")
    if not finished:
        out.append("- none")
    events = rows(c, "SELECT * FROM events ORDER BY id DESC LIMIT ?", (MD_EVENTS,))
    out += ["", f"## Recent events (latest {len(events)})", ""]
    for e in events:
        where = " ".join(x for x in (e["task_id"], e["session_id"]) if x)
        out.append(f"- {e['ts']} {e['type']}{' ' + where if where else ''}: {e['text']}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- server

INITIAL_SLOT = '<script id="hq-initial" type="application/json">null</script>'


def render_page(template, state):
    """Embed the current state so labels and data render before the first poll.

    The JSON sits in a non-executable script element; '<', '>' and '&' are
    escaped so ledger text can never close the element or form markup.
    """
    lang = state.get("lang") or "en"
    if not LANG_RE.match(lang):
        lang = "en"
    data = (json.dumps(state, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026"))
    page = template.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    return page.replace(INITIAL_SLOT, INITIAL_SLOT.replace(">null<", f">{data}<"), 1)


def serve(ledger, port):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from urllib.parse import parse_qs, urlsplit

    if not ledger.exists():
        raise HQError(f"no ledger at {ledger.dir}; run init")
    if port is None:
        port = int(ledger.read(lambda c: get_meta(c, "server_port", "0")))

    class Handler(BaseHTTPRequestHandler):
        server_version = "hq-dashboard"
        sys_version = ""

        def send(self, code, body, ctype, extra=()):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; "
                             "style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; "
                             "base-uri 'none'; form-action 'none'")
            for key, value in extra:
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(body)

        def send_json(self, code, obj):
            self.send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

        def do_GET(self):
            allowed = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in allowed:
                self.send_json(403, {"ok": False, "error": "forbidden host"})
                return
            parts = urlsplit(self.path)
            try:
                if parts.path == "/":
                    self.send(200, render_page(ASSET.read_text(encoding="utf-8"), ledger.read(snapshot)).encode("utf-8"),
                              "text/html; charset=utf-8")
                elif parts.path == "/api/state":
                    since = parse_qs(parts.query).get("since", [""])[0]

                    def load(c):
                        revision = int(get_meta(c, "revision", "0"))
                        if since == str(revision):
                            return {"revision": revision, "unchanged": True}
                        return snapshot(c)
                    self.send_json(200, ledger.read(load))
                else:
                    self.send_json(404, {"ok": False, "error": "not found"})
            except (HQError, sqlite3.Error, OSError) as exc:
                self.send_json(500, {"ok": False, "error": str(exc)})

        def reject(self):
            self.send(405, b'{"ok":false,"error":"read-only dashboard: only GET is allowed"}',
                      "application/json; charset=utf-8", (("Allow", "GET"),))

        do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = do_TRACE = do_CONNECT = reject

        def log_message(self, *args):
            pass

    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError as exc:
        raise HQError(f"cannot listen on 127.0.0.1:{port}: {exc}") from None
    url = f"http://127.0.0.1:{server.server_port}/"
    print(url, flush=True)
    try:
        c = ledger.connect()
        try:
            c.execute("BEGIN IMMEDIATE")
            set_meta(c, "server_url", url)
            set_meta(c, "server_port", str(server.server_port))
            set_meta(c, "server_started_at", now())
            c.execute("COMMIT")
        finally:
            if c.in_transaction:
                c.execute("ROLLBACK")
            c.close()
        ledger.refresh_md()
    except (sqlite3.Error, OSError) as exc:
        print(f"hq.py: could not record the server URL: {exc}", file=sys.stderr, flush=True)
    import signal
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


# ---------------------------------------------------------------- CLI

class Parser(argparse.ArgumentParser):
    def error(self, message):
        emit({"ok": False, "error": f"{self.prog}: {message}"})
        sys.exit(2)


def build_parser():
    common = Parser(add_help=False)
    common.add_argument("--hq", default=argparse.SUPPRESS,
                        help="HQ folder (default: $HQ_DIR, else ~/hq)")
    parser = Parser(prog="hq.py", description=__doc__, parents=[common],
                    formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    def cmd(container, name, help_text):
        return container.add_parser(name, parents=[common], help=help_text, description=help_text)

    p = cmd(sub, "init", "create the ledger if absent; never overwrites")
    p.add_argument("--lang", help="HQ language code for a new ledger (default en)")
    p = cmd(sub, "lang", "set the HQ language (BCP 47 code, e.g. ja)")
    p.add_argument("code")
    p = cmd(sub, "serve", "serve the read-only dashboard on 127.0.0.1 (foreground)")
    p.add_argument("--port", type=int, help="port (default: the last used port, else a free one)")
    p = cmd(sub, "status", "compact summary: open waits, tasks not done with sessions, counts")
    p.add_argument("--json", action="store_true")
    cmd(sub, "export", "rewrite ledger.md now (it is also rewritten after every change)")

    p = cmd(sub, "report", "record a session's turn-end note verbatim (text from --text or stdin)")
    p.add_argument("--session", required=True)
    p.add_argument("--task")
    p.add_argument("--text")
    p = cmd(sub, "launch", "record a started session: task active, session starting, criteria/launch waits resolved")
    p.add_argument("id")
    p.add_argument("--session", required=True)
    for flag in ("--name", "--cwd", "--branch", "--title"):
        p.add_argument(flag)

    task = cmd(sub, "task", "add or update a task")
    task_sub = task.add_subparsers(dest="action", required=True, metavar="ACTION")
    p = cmd(task_sub, "add", "add a task (id assigned: T1, T2, ...)")
    for flag in ("--title", "--target", "--deliverable", "--done"):
        p.add_argument(flag, required=True)
    p.add_argument("--goal")
    p.add_argument("--authority")
    p.add_argument("--status", choices=TASK_STATUSES)
    p = cmd(task_sub, "update", "update task fields")
    p.add_argument("id")
    for flag in ("--title", "--goal", "--target", "--deliverable", "--done", "--authority"):
        p.add_argument(flag)
    p.add_argument("--status", choices=TASK_STATUSES)

    session = cmd(sub, "session", "create or update a session")
    session_sub = session.add_subparsers(dest="action", required=True, metavar="ACTION")
    p = cmd(session_sub, "upsert", "create or update a session by host id")
    p.add_argument("id", metavar="SID")
    p.add_argument("--task", required=True)
    for flag in ("--name", "--title", "--cwd", "--branch", "--summary"):
        p.add_argument(flag)
    p.add_argument("--state", choices=SESSION_STATES)

    edge = cmd(sub, "edge", "add or remove a task relationship")
    edge_sub = edge.add_subparsers(dest="action", required=True, metavar="ACTION")
    for action in ("add", "remove"):
        p = cmd(edge_sub, action, f"{action} FROM KIND TO (FROM depends_on TO = TO blocks FROM)")
        p.add_argument("src", metavar="FROM")
        p.add_argument("kind", choices=EDGE_KINDS, metavar="KIND")
        p.add_argument("dst", metavar="TO")

    wait = cmd(sub, "wait", "add or resolve a waiting-for-you item")
    wait_sub = wait.add_subparsers(dest="action", required=True, metavar="ACTION")
    p = cmd(wait_sub, "add", "open a wait item (id assigned: W1, W2, ...)")
    p.add_argument("--kind", required=True, choices=WAIT_KINDS)
    p.add_argument("--summary", required=True)
    p.add_argument("--task")
    p.add_argument("--session")
    p = cmd(wait_sub, "resolve", "resolve a wait item")
    p.add_argument("id", metavar="WID")
    p.add_argument("--resolution")

    artifact = cmd(sub, "artifact", "record an artifact")
    artifact_sub = artifact.add_subparsers(dest="action", required=True, metavar="ACTION")
    p = cmd(artifact_sub, "add", "add an artifact (id assigned: A1, A2, ...; deduplicated by ref per task)")
    p.add_argument("--task", required=True)
    p.add_argument("--kind", required=True, choices=ARTIFACT_KINDS)
    p.add_argument("--label", required=True)
    p.add_argument("--ref", required=True)

    p = cmd(sub, "note", "append a free-text event")
    p.add_argument("--text", required=True)
    p.add_argument("--task")
    p.add_argument("--session")

    p = cmd(sub, "apply", "apply a JSON array of ops in one all-or-nothing transaction")
    p.add_argument("--file", help="JSON file (default: stdin)")
    return parser


def read_stdin():
    if sys.stdin is None or sys.stdin.isatty():
        raise HQError("no input: pass --text/--file or pipe it on stdin")
    return sys.stdin.buffer.read().decode("utf-8", "replace")


def params_from(args, mapping):
    return {key: getattr(args, attr) for key, attr in mapping.items() if getattr(args, attr, None) is not None}


def run(args):
    hq = getattr(args, "hq", None) or os.environ.get("HQ_DIR") or "~/hq"
    ledger = Ledger(hq)
    command = args.command
    if command == "init":
        if args.lang is not None:
            check_lang(args.lang)
        return ledger.init(args.lang)
    if command == "serve":
        serve(ledger, args.port)
        return None
    if command == "status":
        data = ledger.read(status_data)
        data["server_alive"] = probe_server(data.get("server_url"), data["revision"])
        if args.json:
            return data
        sys.stdout.write(status_text(data, ledger.dir) + "\n")
        return None
    if command == "export":
        ledger.refresh_md(force=True)
        return {"ok": True, "path": str(ledger.md)}
    if command == "apply":
        raw = Path(args.file).read_text(encoding="utf-8") if args.file else read_stdin()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise HQError(f"invalid JSON: {exc}") from None
        return {"ok": True, "results": ledger.mutate(batch_ops(data))}
    if command == "report":
        params = params_from(args, {"session": "session", "task": "task"})
        params["text"] = args.text if args.text is not None else read_stdin()
        name = "report"
    elif command == "launch":
        params = params_from(args, {k: k for k in ("id", "session", "name", "cwd", "branch", "title")})
        name = "launch"
    elif command == "lang":
        params, name = {"code": args.code}, "lang"
    elif command == "note":
        params, name = params_from(args, {"text": "text", "task": "task", "session": "session"}), "note"
    elif command == "task":
        keys = ("title", "goal", "target", "deliverable", "done", "authority", "status")
        params = params_from(args, {k: k for k in keys + ("id",)})
        name = f"task.{args.action}"
    elif command == "session":
        keys = ("id", "task", "name", "title", "cwd", "branch", "state", "summary")
        params, name = params_from(args, {k: k for k in keys}), "session.upsert"
    elif command == "edge":
        params, name = {"from": args.src, "kind": args.kind, "to": args.dst}, f"edge.{args.action}"
    elif command == "wait":
        keys = ("id", "kind", "summary", "task", "session", "resolution")
        params, name = params_from(args, {k: k for k in keys}), f"wait.{args.action}"
    elif command == "artifact":
        params, name = params_from(args, {k: k for k in ("task", "kind", "label", "ref")}), "artifact.add"
    else:  # pragma: no cover - argparse rejects unknown commands
        raise HQError(f"unknown command {command}")
    return ledger.mutate([(name, OPS[name][0], params)])[0]


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    args = build_parser().parse_args(argv)
    try:
        receipt = run(args)
    except HQError as exc:
        emit({"ok": False, "error": str(exc)})
        return 1
    except (sqlite3.Error, OSError) as exc:
        emit({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
        return 1
    if receipt is not None:
        emit(receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
