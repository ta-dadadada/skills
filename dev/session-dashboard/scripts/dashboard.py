#!/usr/bin/env python3
"""A local, read-only session dashboard with a durable report inbox."""
from __future__ import annotations

import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from urllib.parse import urlsplit

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TODO_STATES = {"pending", "in_progress", "done", "blocked", "cancelled"}
AGENT_STATES = {"working", "waiting", "reported", "failed", "stopped"}
SESSION_STATES = {"active", "paused", "completed", "interrupted"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()),
            f"Expected fields: {names}")


def strings(value, names):
    for name in names.split():
        require(isinstance(value[name], str), f"{name} must be text")


def records(value, name):
    require(isinstance(value, list), f"{name} must be a list")
    ids = set()
    for item in value:
        require(isinstance(item, dict) and isinstance(item.get("id"), str)
                and item["id"].strip() and item["id"] not in ids,
                f"{name} requires unique, nonempty IDs")
        ids.add(item["id"])
    return ids


def validate(snapshot):
    require(isinstance(snapshot, dict), "Snapshot must be an object")
    fields({k: v for k, v in snapshot.items() if k not in {"metrics", "session_context"}},
           "goal completion_conditions current_work status summary phases requests agents")
    if "session_context" in snapshot:
        context = snapshot["session_context"]
        fields(context, "started_at cwd")
        require(context["cwd"] is None or (isinstance(context["cwd"], str)
                and context["cwd"].strip()), "cwd must be null or nonempty text")
        started = context["started_at"]
        if started is not None:
            require(isinstance(started, str), "started_at must be null or ISO 8601 text")
            try:
                parsed = datetime.fromisoformat(started)
            except ValueError:
                raise ValueError("started_at must be ISO 8601 with timezone") from None
            require(parsed.tzinfo is not None, "started_at needs timezone")
    if "metrics" in snapshot:
        metrics = snapshot["metrics"]
        fields(metrics, "models total_tokens scope source reported_at")
        strings(metrics, "scope source reported_at")
        require(all(metrics[k].strip() for k in ("scope", "source", "reported_at")),
                "Metrics need scope, source and observation time")
        require(isinstance(metrics["models"], list)
                and all(isinstance(x, str) and x.strip() for x in metrics["models"]),
                "Models must be a list of observed names")
        tokens = metrics["total_tokens"]
        require(tokens is None or (type(tokens) is int and tokens >= 0),
                "total_tokens must be null or a nonnegative integer")
    strings(snapshot, "goal current_work status summary")
    require(snapshot["goal"].strip(), "goal must not be empty")
    require(snapshot["status"] in SESSION_STATES, "Invalid session status")
    conditions = snapshot["completion_conditions"]
    require(isinstance(conditions, list) and conditions
            and all(isinstance(x, str) and x.strip() for x in conditions),
            "completion_conditions must contain text")
    records(snapshot["phases"], "phases")
    todos = set()
    for phase in snapshot["phases"]:
        fields(phase, "id title todos")
        strings(phase, "id title")
        ids = records(phase["todos"], "todos")
        require(not todos.intersection(ids), "TODO IDs must be unique across phases")
        todos.update(ids)
        for todo in phase["todos"]:
            fields(todo, "id title status owner result")
            strings(todo, "id title status owner result")
            require(todo["status"] in TODO_STATES, "Invalid TODO status")
            require(todo["status"] != "done" or todo["result"].strip(), "Done TODO needs result")
    records(snapshot["requests"], "requests")
    for request in snapshot["requests"]:
        fields(request, "id kind title detail status blocks resolution")
        strings(request, "id kind title detail status resolution")
        require(request["kind"] in {"decision", "review"}, "Invalid request kind")
        require(request["status"] in {"open", "resolved"}, "Invalid request status")
        require(isinstance(request["blocks"], list)
                and all(isinstance(x, str) and x in todos for x in request["blocks"]),
                "Request blocks must reference current TODO IDs")
        require(request["status"] != "resolved" or request["resolution"].strip(),
                "Resolved request needs resolution")
    records(snapshot["agents"], "agents")
    for agent in snapshot["agents"]:
        fields(agent, "id assignment status latest_report result review reported_at")
        strings(agent, "id assignment status latest_report result review reported_at")
        require(agent["status"] in AGENT_STATES, "Invalid agent status")
        require(agent["review"] in {"pending", "accepted", "changes_requested"}, "Invalid review")
        require(agent["reported_at"].strip(), "Agent report needs timestamp")
    if snapshot["status"] == "completed":
        require(snapshot["summary"].strip(), "Completed session needs summary")
        require(all(t["status"] in {"done", "cancelled"} for p in snapshot["phases"] for t in p["todos"]),
                "Completed session has unfinished TODOs")
        require(all(r["status"] == "resolved" for r in snapshot["requests"]),
                "Completed session has open requests")


def plan(snapshot):
    return [snapshot["goal"], snapshot["completion_conditions"],
            [[p["id"], p["title"], [[t["id"], t["title"], t["owner"],
              t["status"] == "cancelled"] for t in p["todos"]]] for p in snapshot["phases"]]]


class Store:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.db = self.directory / "session.sqlite3"

    @contextlib.contextmanager
    def transaction(self):
        require(self.db.is_file(), "Session is not initialized")
        connection = sqlite3.connect(self.db, timeout=15)
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def init(self, session_id, snapshot):
        validate(snapshot)
        require(isinstance(session_id, str) and session_id.strip(), "Session ID is required")
        self.directory.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.db, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
        state = {"session_id": session_id, "revision": 0, "snapshot": snapshot,
                 "received_at": now(), "applied_at": now(), "runtime_agents": {},
                 "finished_at": None if snapshot["status"] == "active" else now(),
                 "history": [{"at": now(), "reason": "Session initialized", "revision": 0}]}
        with sqlite3.connect(self.db) as c:
            c.execute("CREATE TABLE state (id INTEGER PRIMARY KEY CHECK(id=1), body TEXT NOT NULL)")
            c.execute("INSERT INTO state VALUES (1, ?)", (encoded(state),))
            c.execute("CREATE TABLE reports (id TEXT PRIMARY KEY, body TEXT NOT NULL, applied INTEGER NOT NULL DEFAULT 0)")
        self.export()

    @staticmethod
    def read(c):
        return json.loads(c.execute("SELECT body FROM state WHERE id=1").fetchone()[0])

    @staticmethod
    def write(c, state):
        c.execute("UPDATE state SET body=? WHERE id=1", (encoded(state),))

    def state(self):
        with self.transaction() as c:
            state = self.read(c)
            state["pending_reports"] = [r[0] for r in c.execute("SELECT id FROM reports WHERE applied=0 ORDER BY rowid")]
            return state

    def submit(self, report):
        fields(report, "id expected_revision reason snapshot")
        strings(report, "id reason")
        require(report["id"].strip(), "Report ID must not be empty")
        require(type(report["expected_revision"]) is int and report["expected_revision"] >= 0,
                "expected_revision must be a nonnegative integer")
        validate(report["snapshot"])
        with self.transaction() as c:
            old = c.execute("SELECT body FROM reports WHERE id=?", (report["id"],)).fetchone()
            if old:
                require(old[0] == encoded(report), "Report ID already has different content")
            else:
                state = self.read(c)
                c.execute("INSERT INTO reports(id, body) VALUES (?, ?)", (report["id"], encoded(report)))
                state["received_at"] = now()
                self.write(c, state)
        self.export()
        return report["id"]

    def apply(self, report_id):
        with self.transaction() as c:
            row = c.execute("SELECT body, applied FROM reports WHERE id=?", (report_id,)).fetchone()
            require(row is not None, "Unknown report ID")
            report, applied = json.loads(row[0]), row[1]
            state = self.read(c)
            require(applied != 2, "Report was withdrawn")
            if not applied:
                require(report["expected_revision"] == state["revision"],
                        "Stale report: main agent must reconcile against current state")
                changed = plan(state["snapshot"]) != plan(report["snapshot"])
                require(not changed or report["reason"].strip(), "Plan changes require a reason")
                if report["snapshot"]["status"] == "active":
                    state["finished_at"] = None
                elif state["snapshot"]["status"] == "active":
                    state["finished_at"] = now()
                else:
                    state.setdefault("finished_at", state["applied_at"])
                state["revision"] += 1
                state["snapshot"] = report["snapshot"]
                state["applied_at"] = now()
                state["history"].append({"at": now(), "revision": state["revision"],
                                         "reason": report["reason"] or "Progress updated"})
                self.write(c, state)
                c.execute("UPDATE reports SET applied=1 WHERE id=?", (report_id,))
            revision = state["revision"]
        self.export()
        return revision

    def withdraw(self, report_id, reason):
        require(reason.strip(), "Withdrawal requires reason")
        with self.transaction() as c:
            row = c.execute("SELECT applied FROM reports WHERE id=?", (report_id,)).fetchone()
            require(row is not None and row[0] != 1, "Cannot withdraw unknown/applied report")
            if row[0] == 0:
                state = self.read(c)
                state["history"].append({"at": now(), "revision": state["revision"],
                                         "reason": f"Withdrawn {report_id}: {reason}"})
                self.write(c, state)
                c.execute("UPDATE reports SET applied=2 WHERE id=?", (report_id,))
        self.export()

    def hook(self, event):
        require(isinstance(event, dict), "Hook input must be an object")
        with self.transaction() as c:
            state = self.read(c)
            if event.get("session_id") != state["session_id"]:
                return
            kind = event.get("hook_event_name")
            if kind not in {"SubagentStart", "SubagentStop"}:
                return
            agent_id = event.get("agent_id")
            require(isinstance(agent_id, str) and agent_id.strip(), "Hook needs agent_id")
            agent_type = event.get("agent_type", "")
            require(isinstance(agent_type, str), "agent_type must be text")
            state["runtime_agents"][agent_id] = {"event": kind, "type": agent_type, "at": now()}
            self.write(c, state)
        self.export()

    def export(self):
        with self.transaction() as c:
            state = self.read(c)
            state["pending_reports"] = [r[0] for r in c.execute("SELECT id FROM reports WHERE applied=0 ORDER BY rowid")]
            atomic(self.directory / "state.json", encoded(state) + "\n")
            atomic(self.directory / "report.html", page(state))


def atomic(path, content):
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".dashboard-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def esc(value):
    return html.escape(str(value), quote=True)


LABELS = {"pending": "未着手 / 未確認", "in_progress": "作業中", "done": "完了", "blocked": "待機",
          "cancelled": "取りやめ", "active": "進行中", "paused": "一時停止", "completed": "完了",
          "interrupted": "中断", "working": "作業中", "waiting": "待機", "reported": "報告済み",
          "failed": "問題あり", "stopped": "停止", "open": "返答待ち", "resolved": "解決済み",
          "accepted": "確認・反映済み", "changes_requested": "修正依頼", "decision": "判断", "review": "レビュー"}


def badge(value):
    return f'<span class="badge status-{esc(value)}">{esc(LABELS.get(value, value))}</span>'


def elapsed_text(state, observed_at=None):
    snapshot = state["snapshot"]
    start = datetime.fromisoformat(state["history"][0]["at"])
    end = (observed_at or now()) if snapshot["status"] == "active" else (
        state.get("finished_at") or state["applied_at"])
    seconds = max(0, int((datetime.fromisoformat(end) - start).total_seconds()))
    hours, remaining = divmod(seconds, 3600)
    minutes, seconds = divmod(remaining, 60)
    elapsed = f"{hours}時間 {minutes}分 {seconds}秒" if hours else f"{minutes}分 {seconds}秒"
    return elapsed


def usage_widgets(state, observed_at=None):
    elapsed = elapsed_text(state, observed_at)
    metrics = state["snapshot"].get("metrics")
    total = metrics["total_tokens"] if metrics else None
    tokens = f"{total:,}" if total is not None else "未取得"
    models = " / ".join(metrics["models"]) if metrics and metrics["models"] else "未取得"
    note = (f'範囲：{metrics["scope"]}\n出典：{metrics["source"]}\n観測：{metrics["reported_at"]}'
            if metrics else "実行環境からの報告が届いた場合に表示します。")
    return ('<section class="usage"><h2>実行状況</h2><dl class="widgets">'
            f'<div><dt>経過時間</dt><dd id="elapsed-time">{esc(elapsed)}</dd>'
            '<p class="meta">ダッシュボード起動から・待機時間を含む</p></div>'
            f'<div><dt>使用トークン</dt><dd>{tokens}</dd></div>'
            f'<div><dt>実行モデル</dt><dd>{esc(models)}</dd></div></dl>'
            f'<p class="meta">{esc(note)}</p></section>')


def overview(state):
    s = state["snapshot"]
    todos = [t for p in s["phases"] for t in p["todos"]]
    return {
        "total": len(todos), "done": sum(t["status"] == "done" for t in todos),
        "running": sum(t["status"] == "in_progress" for t in todos),
        "cancelled": sum(t["status"] == "cancelled" for t in todos),
        "attention": sum(r["status"] == "open" for r in s["requests"]),
        "failed": sum(a["status"] == "failed" for a in s["agents"]),
        "unverified": sum(a["review"] == "pending" and (a["status"] == "reported" or bool(a["result"].strip()))
                          for a in s["agents"]) + len(state.get("pending_reports", [])),
    }


def disclosure(key, title, content):
    return f'<details id="{esc(key)}"><summary>{esc(title)}</summary>{content}</details>'


def body(state):
    s = state["snapshot"]
    counts = overview(state)
    context = s.get("session_context", {})
    parts = [f'<header><div class="session-line"><span class="eyebrow">SESSION / STATUS</span>{badge(s["status"])}</div>'
             f'<h1>{esc(s["goal"])}</h1><p class="current"><span class="meta">NOW</span> {esc(s["current_work"]) or "現在の作業は未報告"}</p>'
             f'<p class="meta">セッション開始：{esc(context.get("started_at") or "未取得")} · 最終反映：{esc(state["applied_at"])}</p></header>',
             '<nav class="overview" aria-label="状況サマリー">']
    for key, label, target, tone in [("done", "完了 / 全TODO", "plan", ""),
                                   ("attention", "Attention · 対応待ち", "attention", "attention"),
                                   ("running", "Running · 作業中", "plan", "running"),
                                   ("failed", "Failed · 問題あり", "agents", "failed"),
                                   ("unverified", "Unverified · 未確認", "attention", "attention")]:
        number = f'{counts[key]} / {counts["total"]}' if key == "done" else str(counts[key])
        parts.append(f'<a href="#{target}" class="stat {tone if counts[key] else ""}"><span>{label}</span><strong>{number}</strong></a>')
    parts.append('</nav><p class="meta legend">件数は最終報告時点。Attention＝人間への依頼、Running＝TODO、Failed＝エージェント、Unverified＝成果・反映待ち報告。</p>')
    parts.append('<section id="attention"><h2>Attention <span>判断・レビュー / 確認事項</span></h2>')
    attention = []
    resolved = []
    for r in s["requests"]:
        row = (f'<article class="attention-row"><div class="row-heading">{badge(r["kind"])} <h3>{esc(r["title"])}</h3>{badge(r["status"])}</div>'
               f'<p>{esc(r["detail"])}</p><p class="meta">停止中のTODO：{esc(", ".join(r["blocks"])) if r["blocks"] and r["status"] == "open" else "なし"}</p>'
               f'<p>{esc(r["resolution"])}</p></article>')
        (attention if r["status"] == "open" else resolved).append(row)
    for phase in s["phases"]:
        for t in phase["todos"]:
            if t["status"] == "blocked":
                attention.append(f'<p class="attention-row">{badge("blocked")} {esc(t["title"])} · 担当 {esc(t["owner"])} — {esc(t["result"])}</p>')
    for a in s["agents"]:
        if a["status"] == "failed" or a["review"] == "changes_requested" or (a["review"] == "pending" and (a["status"] == "reported" or a["result"].strip())):
            label = "failed" if a["status"] == "failed" else a["review"]
            attention.append(f'<p class="attention-row">{badge(label)} <strong>{esc(a["id"])}</strong> · {esc(a["assignment"])} — {esc(a["latest_report"])}</p>')
    if state.get("pending_reports"):
        attention.append(f'<p class="attention-row">反映待ちの報告：{esc(", ".join(state["pending_reports"]))}</p>')
    parts.extend(attention or ['<p class="empty">報告された対応待ち・問題・未確認成果はありません。</p>'])
    if counts["attention"]:
        parts.append('<p class="meta">返答は元のチャットでお願いします。</p>')
    if s["summary"]:
        parts.append(f'<p class="summary-note">作業のまとめ・残作業・未確認事項：{esc(s["summary"])}</p>')
    parts.append('</section><div class="columns"><section id="plan"><h2>作業計画 <span>フェーズ / TODO</span></h2>')
    rank = {"blocked": 0, "in_progress": 1, "pending": 2, "done": 3, "cancelled": 4}
    for phase in s["phases"]:
        done = sum(t["status"] == "done" for t in phase["todos"])
        total = len(phase["todos"])
        parts.append(f'<article class="phase"><div class="row-heading"><h3>{esc(phase["title"])}</h3><span class="meta">{done} / {total} 完了</span></div>'
                     f'<progress value="{done}" max="{total or 1}" aria-label="{esc(phase["title"])}のTODO完了数"></progress>')
        active, complete = [], []
        for t in sorted(phase["todos"], key=lambda t: rank[t["status"]]):
            row = (f'<li data-todo-status="{esc(t["status"])}"><div class="todo-line">{badge(t["status"])} <strong>{esc(t["title"])}</strong> <span class="owner">担当 {esc(t["owner"])}</span></div>'
                   f'<p class="meta">{esc(t["id"])}</p><p>{esc(t["result"])}</p></li>')
            (complete if t["status"] in {"done", "cancelled"} else active).append(row)
        parts.append('<ul class="todos">' + ''.join(active) + '</ul>')
        if complete:
            parts.append(disclosure('phase-' + phase['id'], f'完了・取りやめ {len(complete)}件', '<ul class="todos">' + ''.join(complete) + '</ul>'))
        parts.append('</article>')
    if not s["phases"]:
        parts.append('<p class="empty">作業計画はまだ報告されていません。</p>')
    parts.append(f'<p class="meta">取りやめ {counts["cancelled"]}件（完了数には含めません）</p></section><section id="agents"><h2>エージェント <span>報告された状態</span></h2>')
    quiet = []
    for a in sorted(s["agents"], key=lambda a: ({"failed": 0, "working": 1, "waiting": 2, "reported": 3, "stopped": 4}[a["status"]])):
        row = (f'<article class="agent-row"><div class="row-heading">{badge(a["status"])}<h3>{esc(a["id"])}</h3></div>'
               f'<p>{esc(a["assignment"])}</p><p class="agent-report">{esc(a["latest_report"])}</p><p>{esc(a["result"])}</p>'
               f'<p class="meta">成果の確認：{badge(a["review"])} · 報告時刻：{esc(a["reported_at"])}</p></article>')
        if a["review"] == "accepted" and a["status"] in {"reported", "stopped"}:
            quiet.append(row)
        else:
            parts.append(row)
    if not s["agents"]:
        parts.append('<p class="empty">担当状況の報告はまだありません。</p>')
    if quiet:
        parts.append(disclosure('accepted-agents', f'確認済みエージェント {len(quiet)}件', ''.join(quiet)))
    parts.append('</section></div><footer>')
    parts.append(disclosure('session-details', 'セッション詳細・実行状況',
        '<dl class="session-info">' + ''.join(f'<div><dt>{label}</dt><dd>{esc(value)}</dd></div>' for label, value in [
            ('セッションID', state['session_id']), ('セッション開始', context.get('started_at') or '未取得'),
            ('CWD', context.get('cwd') or '未取得'), ('ダッシュボード起動', state['history'][0]['at']),
            ('最終報告受信', state['received_at']), ('更新番号', state['revision'])]) + '</dl>' + usage_widgets(state)))
    parts.append(disclosure('conditions', '完了条件', '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in s['completion_conditions']) + '</ul>'))
    if resolved:
        parts.append(disclosure('resolved-requests', f'解決済みの判断・レビュー {len(resolved)}件', ''.join(resolved)))
    if state['runtime_agents']:
        observations = '<p class="meta">最後に観測した開始・応答終了です。TODOの完了を意味しません。</p><ul>'
        for aid, observed in state['runtime_agents'].items():
            label = '開始を観測' if observed['event'] == 'SubagentStart' else '応答終了を観測'
            observations += f'<li>{esc(aid)} · {esc(observed["type"])} · {label}<p class="meta">{esc(observed["at"])}</p></li>'
        parts.append(disclosure('runtime-observations', '実行環境からの観測', observations + '</ul>'))
    history = '<ol>' + ''.join(f'<li><p>{esc(e["reason"])}</p><p class="meta">{esc(e["at"])} · 更新番号 {e["revision"]}</p></li>' for e in reversed(state['history'])) + '</ol>'
    parts.append(disclosure('history', f'変更・進捗履歴 {len(state["history"])}件', history))
    parts.append('</footer>')
    return ''.join(parts)


def page(state):
    template = (ASSETS / "dashboard.html").read_text(encoding="utf-8")
    return template.replace("<!--CONTENT-->", body(state))


def serve(store, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.headers.get("Host") != f"127.0.0.1:{self.server.server_port}":
                self.send_error(403)
                return
            path = urlsplit(self.path).path
            if path not in {"/", "/view.json"}:
                self.send_error(404)
                return
            state = store.state()
            content = body(state)
            payload = (encoded({"html": content, "elapsed": elapsed_text(state),
                                "version": hashlib.sha256(encoded(state).encode()).hexdigest()})
                       if path == "/view.json" else page(state)).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8" if path.endswith("json") else "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"http://127.0.0.1:{server.server_port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, help="Durable directory for one session")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--session-id", required=True)
    init.add_argument("--input", required=True, help="Initial snapshot JSON")
    submit = sub.add_parser("submit")
    submit.add_argument("--input", required=True, help="Report JSON; '-' reads stdin")
    apply = sub.add_parser("apply")
    apply.add_argument("--report", required=True)
    withdraw = sub.add_parser("withdraw")
    withdraw.add_argument("--report", required=True)
    withdraw.add_argument("--reason", required=True)
    sub.add_parser("status")
    sub.add_parser("export")
    sub.add_parser("hook", help="Read lifecycle event JSON from stdin")
    server = sub.add_parser("serve")
    server.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    store = Store(args.directory)
    try:
        if args.command in {"init", "submit"}:
            data = json.load(sys.stdin) if args.input == "-" else json.loads(Path(args.input).read_text(encoding="utf-8"))
            if args.command == "init":
                store.init(args.session_id, data)
            else:
                print(store.submit(data))
        elif args.command == "apply":
            print(store.apply(args.report))
        elif args.command == "withdraw":
            store.withdraw(args.report, args.reason)
        elif args.command == "status":
            print(encoded(store.state()))
        elif args.command == "export":
            store.export()
        elif args.command == "hook":
            store.hook(json.load(sys.stdin))
            print("{}")
        elif args.command == "serve":
            store.state()
            serve(store, args.port)
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        print(f"dashboard: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
