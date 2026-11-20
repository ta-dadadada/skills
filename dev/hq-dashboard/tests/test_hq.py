import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
import unittest.mock
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "hq.py"
ASSET = ROOT / "assets" / "dashboard.html"
spec = importlib.util.spec_from_file_location("hq", SCRIPT)
hq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hq)


class LedgerCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name) / "hq"
        self.ledger = hq.Ledger(self.dir)
        self.ledger.init("ja")

    def op(self, op_name, /, **params):
        return self.ledger.mutate([(op_name, hq.OPS[op_name][0], params)])[0]

    def task(self, title="タスク", target="repoA", **extra):
        return self.op("task.add", title=title, target=target, deliverable="PR", done="tests pass", **extra)["id"]

    def report(self, session, text, task=None):
        params = {"session": session, "text": text}
        if task:
            params["task"] = task
        return self.op("report", **params)

    def q(self, sql, args=()):
        return self.ledger.read(lambda c: [dict(r) for r in c.execute(sql, args)])

    def waits(self, status="open"):
        return self.q("SELECT * FROM waits WHERE status=? ORDER BY num", (status,))

    def task_row(self, task_id):
        return self.q("SELECT * FROM tasks WHERE id=?", (task_id,))[0]

    def session_row(self, sid):
        return self.q("SELECT * FROM sessions WHERE id=?", (sid,))[0]

    def revision(self):
        return self.ledger.read(lambda c: int(hq.get_meta(c, "revision")))

    def cli(self, *args, stdin=None, env=None):
        full_env = {k: v for k, v in os.environ.items() if k != "HQ_DIR"}
        full_env.update(env or {})
        proc = subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True,
                              text=True, encoding="utf-8", env=full_env)
        line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "{}"
        return proc.returncode, json.loads(line)


class InitAndLangTest(LedgerCase):
    def test_init_is_idempotent_and_never_overwrites(self):
        tid = self.task()
        again = self.ledger.init("en")
        self.assertEqual((again["ok"], again["created"], again["lang"]), (True, False, "ja"))
        self.assertIn("note", again)
        self.assertEqual(self.task_row(tid)["title"], "タスク")
        code, receipt = self.cli("--hq", str(self.dir), "init")
        self.assertEqual((code, receipt["created"]), (0, False))
        self.assertEqual(self.q("PRAGMA journal_mode")[0]["journal_mode"], "wal")

    def test_lang_command_and_validation(self):
        self.assertEqual(self.op("lang", code="en")["lang"], "en")
        self.assertEqual(self.ledger.read(lambda c: hq.get_meta(c, "lang")), "en")
        with self.assertRaisesRegex(hq.HQError, "invalid language"):
            self.op("lang", code="not a code")
        code, receipt = self.cli("--hq", str(Path(self.temp.name) / "new"), "init", "--lang", "!!")
        self.assertEqual((code, receipt["ok"]), (1, False))
        self.assertFalse((Path(self.temp.name) / "new" / "ledger.sqlite3").exists())

    def test_hq_resolution_order_and_position(self):
        other = Path(self.temp.name) / "env-hq"
        code, receipt = self.cli("init", env={"HQ_DIR": str(other)})
        self.assertEqual((code, receipt["hq"]), (0, str(other)))
        code, receipt = self.cli("init", "--hq", str(self.dir), env={"HQ_DIR": str(other)})
        self.assertEqual(receipt["hq"], str(self.dir))
        home = Path(self.temp.name) / "home"
        code, receipt = self.cli("init", env={"HOME": str(home), "HQ_DIR": ""})
        self.assertEqual(receipt["hq"], str(home / "hq"))

    def test_uninitialized_ledger_is_an_error(self):
        code, receipt = self.cli("--hq", str(Path(self.temp.name) / "missing"), "note", "--text", "x")
        self.assertEqual(code, 1)
        self.assertIn("run init", receipt["error"])


class MutationTest(LedgerCase):
    def test_ids_receipts_and_one_event_per_mutation(self):
        t1, t2 = self.task("一"), self.task("二", status="active")
        self.assertEqual((t1, t2), ("T1", "T2"))
        events = len(self.q("SELECT id FROM events"))
        rev = self.revision()
        r = self.op("task.update", id=t1, status="active", goal="目的")
        self.assertEqual((r["status"], sorted(r["changed"])), ("active", ["goal", "status"]))
        r = self.op("session.upsert", id="local_a", task=t1, name="t1-x", state="working", summary="作業中")
        self.assertEqual((r["created"], r["state"], r["task"]), (True, "working", "T1"))
        self.assertIsNotNone(self.session_row("local_a")["reported_at"])
        r = self.op("session.upsert", id="local_a", task=t1, branch="feat/x")
        self.assertEqual((r["created"], r["state"]), (False, "working"))
        self.assertEqual(self.op("edge.add", **{"from": t2, "kind": "depends_on", "to": t1})["created"], True)
        self.assertEqual(self.op("edge.add", **{"from": t2, "kind": "depends_on", "to": t1})["created"], False)
        w = self.op("wait.add", kind="decision", summary="どちらにするか", task=t1, session="local_a")
        self.assertEqual((w["id"], w["created"]), ("W1", True))
        self.assertEqual(self.op("wait.add", kind="decision", summary="どちらにするか", task=t1,
                                 session="local_a")["created"], False)
        r = self.op("wait.resolve", id="W1", resolution='user: "A"')
        self.assertEqual((r["status"], r["task"]), ("resolved", "T1"))
        again = self.op("wait.resolve", id="W1", resolution="later")
        self.assertEqual((again["already_resolved"], again["resolution"]), (True, 'user: "A"'))
        a = self.op("artifact.add", task=t1, kind="pr", label="PR 1", ref="https://x/pull/1")
        self.assertEqual((a["id"], a["created"]), ("A1", True))
        self.assertEqual(self.op("artifact.add", task=t1, kind="url", label="dup", ref="https://x/pull/1"),
                         {"ok": True, "id": "A1", "created": False})
        self.assertEqual(self.op("note", text="メモ", task=t1)["ok"], True)
        self.assertEqual(self.op("edge.remove", **{"from": t2, "kind": "depends_on", "to": t1})["removed"], True)
        self.assertEqual(len(self.q("SELECT id FROM events")) - events, 13)
        self.assertEqual(self.revision() - rev, 13)

    def test_unknown_ids_and_enum_errors(self):
        t1 = self.task()
        cases = [
            ("task.update", {"id": "T9"}, "unknown task T9"),
            ("task.update", {"id": t1, "status": "finished"}, "invalid status"),
            ("task.add", {"title": "x", "target": "y", "deliverable": "d", "done": "c", "status": "x"}, "invalid"),
            ("session.upsert", {"id": "s", "task": "T9"}, "unknown task"),
            ("session.upsert", {"id": "s", "task": t1, "state": "sleeping"}, "invalid state"),
            ("edge.add", {"from": t1, "kind": "blocks", "to": t1}, "invalid kind"),
            ("edge.add", {"from": t1, "kind": "related", "to": "T9"}, "unknown task"),
            ("edge.add", {"from": t1, "kind": "related", "to": t1}, "two different"),
            ("edge.remove", {"from": t1, "kind": "related", "to": self.task()}, "no edge"),
            ("wait.add", {"kind": "question", "summary": "x"}, "invalid kind"),
            ("wait.add", {"kind": "review", "summary": "x", "session": "nope"}, "unknown session"),
            ("wait.resolve", {"id": "W7"}, "unknown wait"),
            ("artifact.add", {"task": t1, "kind": "zip", "label": "l", "ref": "r"}, "invalid kind"),
            ("note", {"text": "x", "task": "T42"}, "unknown task"),
            ("launch", {"id": "T42", "session": "s"}, "unknown task"),
            ("report", {"session": "s", "text": "x", "task": "T42"}, "unknown task"),
        ]
        rev = self.revision()
        for name, params, message in cases:
            with self.subTest(op=name, params=params):
                with self.assertRaisesRegex(hq.HQError, message):
                    self.op(name, **params)
        self.assertEqual(self.revision(), rev)
        code, receipt = self.cli("--hq", str(self.dir), "wait", "add", "--kind", "bogus", "--summary", "x")
        self.assertNotEqual(code, 0)
        self.assertFalse(receipt["ok"])
        code, receipt = self.cli("--hq", str(self.dir), "task", "update", "T77", "--title", "x")
        self.assertEqual((code, receipt["ok"], receipt["error"]), (1, False, "unknown task T77"))

    def test_apply_is_all_or_nothing(self):
        ops = [{"op": "task.add", "title": "一", "target": "r", "deliverable": "d", "done": "c"},
               {"op": "wait.add", "kind": "criteria", "task": "T1", "summary": "確認"},
               {"op": "edge.add", "from": "T1", "kind": "related", "to": "T5"}]
        code, receipt = self.cli("--hq", str(self.dir), "apply", stdin=json.dumps(ops))
        self.assertEqual(code, 1)
        self.assertIn("op 2 (edge.add)", receipt["error"])
        self.assertEqual(self.q("SELECT id FROM tasks"), [])
        self.assertEqual(self.waits(), [])
        ops[2]["to"] = "T1"
        ops[2]["op"] = "note"
        del ops[2]["from"], ops[2]["kind"], ops[2]["to"]
        ops[2]["text"] = "まとめて登録"
        code, receipt = self.cli("--hq", str(self.dir), "apply", stdin=json.dumps(ops, ensure_ascii=False))
        self.assertEqual(code, 0)
        self.assertEqual([r["ok"] for r in receipt["results"]], [True, True, True])
        self.assertEqual(receipt["results"][0]["id"], "T1")
        for bad, message in (([{"op": "task.add", "title": "x"}], "missing keys"),
                             ([{"op": "note", "text": "x", "extra": 1}], "unknown keys"),
                             ([{"op": "explode"}], "unknown op"), ({"op": "note"}, "array")):
            with self.subTest(bad=bad):
                code, receipt = self.cli("--hq", str(self.dir), "apply", stdin=json.dumps(bad))
                self.assertEqual(code, 1)
                self.assertIn(message, receipt["error"])

    def test_launch_resolves_criteria_and_launch_waits(self):
        t1 = self.task()
        self.op("wait.add", kind="criteria", task=t1, summary="完了条件の確認")
        self.op("wait.add", kind="launch", task=t1, summary="launch T1 in repoA")
        self.op("wait.add", kind="decision", task=t1, summary="別件")
        r = self.op("launch", id=t1, session="local_s", name="t1-a", cwd="/work/a", branch="feat/a", title="T1")
        self.assertEqual((r["task"], r["session"], r["state"], r["waits_resolved"]),
                         ("T1", "local_s", "starting", ["W1", "W2"]))
        # the still-open decision wait keeps the task waiting on the user
        self.assertEqual((r["task_status"], self.task_row(t1)["status"]), ("waiting-user", "waiting-user"))
        self.assertEqual([w["id"] for w in self.waits()], ["W3"])
        s = self.session_row("local_s")
        self.assertEqual((s["name"], s["cwd"], s["branch"], s["state"]), ("t1-a", "/work/a", "feat/a", "starting"))

    def test_ledger_md_is_rewritten_in_order(self):
        t1 = self.task("一番目")
        self.op("launch", id=t1, session="local_a")
        self.report("local_a", "HQ T1 waiting-user: 完了。Needs: approval: git push origin feat/a。Artifacts: none")
        self.op("task.add", title="終わった", target="r", deliverable="d", done="c", status="done")
        md = (self.dir / "ledger.md").read_text(encoding="utf-8")
        order = [md.index(h) for h in ("## Waiting for you (1)", "## Tasks not done (1)", "## Finished tasks (1)",
                                       "## Recent events")]
        self.assertEqual(order, sorted(order))
        self.assertIn("W1 [approval]", md)
        self.assertIn("- Done when: tests pass", md)
        self.assertIn("local_a [waiting-user]", md)
        self.assertEqual(list(self.dir.glob(".ledger.md.*.tmp")), [])


class ReportTest(LedgerCase):
    def setUp(self):
        super().setUp()
        self.t1 = self.task("リトライ")
        self.op("launch", id=self.t1, session="local_a")

    def test_each_needs_kind_opens_a_wait_and_sets_waiting_user(self):
        for kind in ("approval", "decision", "review"):
            with self.subTest(kind=kind):
                r = self.report("local_a", f"HQ T1 waiting-user: 準備完了. Needs: {kind}: {kind} の内容. Artifacts: none.")
                self.assertTrue(r["parsed"])
                self.assertEqual([(w["kind"], w["summary"]) for w in r["waits_opened"]], [(kind, f"{kind} の内容")])
                self.assertEqual(self.task_row("T1")["status"], "waiting-user")
                self.assertEqual(self.session_row("local_a")["state"], "waiting-user")

    def test_needs_none_resolves_and_restated_need_is_not_duplicated(self):
        first = self.report("local_a", "HQ T1 waiting-user: x. Needs: approval: git push origin feat/a; review: 文書. Artifacts: none")
        self.assertEqual([w["kind"] for w in first["waits_opened"]], ["approval", "review"])
        again = self.report("local_a", "HQ T1 waiting-user: x. Needs: approval:  git push origin   feat/a. Artifacts: none")
        self.assertEqual((again["waits_opened"], again["waits_resolved"]), ([], ["W2"]))
        self.assertEqual(self.q("SELECT resolution FROM waits WHERE id='W2'")[0]["resolution"], "superseded by report")
        self.op("wait.add", kind="launch", task="T1", summary="次の起動")
        done = self.report("local_a", "HQ T1 working: 続行中. Needs: none. Artifacts: none")
        self.assertEqual(done["waits_resolved"], ["W1"])
        self.assertEqual([w["kind"] for w in self.waits()], ["launch"])
        self.assertEqual(self.task_row("T1")["status"], "active")

    def test_missing_needs_segment_leaves_waits_open(self):
        self.report("local_a", "HQ T1 waiting-user: x. Needs: approval: push. Artifacts: none")
        r = self.report("local_a", "HQ T1 working: 途中で切れた報告")
        self.assertTrue(r["parsed"])
        self.assertEqual(r["waits_resolved"], [])
        self.assertEqual(len(self.waits()), 1)
        self.assertTrue(any("Needs" in w for w in r["warnings"]))

    def test_blocked_and_done_never_completes_task(self):
        r = self.report("local_a", "HQ T1 blocked: 依存待ち. Needs: none. Artifacts: none")
        self.assertEqual((r["state"], self.task_row("T1")["status"]), ("blocked", "blocked"))
        r = self.report("local_a", "HQ T1 done: 全テスト通過. Needs: none. Artifacts: branch feat/a")
        self.assertEqual(r["state"], "done")
        self.assertEqual(self.session_row("local_a")["state"], "done")
        self.assertEqual(self.task_row("T1")["status"], "active")
        self.op("task.update", id="T1", status="done")
        self.report("local_a", "HQ T1 working: 追加作業. Needs: none. Artifacts: none")
        self.assertEqual(self.task_row("T1")["status"], "done")

    def test_artifact_kinds_and_dedupe(self):
        text = ("HQ T1 waiting-user: 完了. Needs: review: 確認. Artifacts: branch feat/retry, "
                "PR https://github.com/o/r/pull/12, https://github.com/o/r/pull/12, doc /home/u/notes/設計.md, "
                "https://example.com/report, 手順メモ.")
        r = self.report("local_a", text)
        arts = self.q("SELECT kind, ref FROM artifacts ORDER BY num")
        self.assertEqual(arts, [{"kind": "branch", "ref": "feat/retry"},
                                {"kind": "pr", "ref": "https://github.com/o/r/pull/12"},
                                {"kind": "doc", "ref": "/home/u/notes/設計.md"},
                                {"kind": "url", "ref": "https://example.com/report"},
                                {"kind": "other", "ref": "手順メモ"}])
        self.assertEqual(r["artifacts_added"], ["A1", "A2", "A3", "A4", "A5"])
        self.assertEqual(self.report("local_a", text)["artifacts_added"], [])

    def test_japanese_text_with_fullwidth_punctuation(self):
        text = ("報告します。\nHQ　T1　waiting-user：テストは全て通過しました。Needs：approval：git push origin feat/retry"
                "；decision：方式Aか方式Bか。Artifacts：branch feat/retry、PR https://github.com/o/r/pull/3。\n"
                "詳細: pytest 42 passed")
        r = self.report("local_a", text)
        self.assertTrue(r["parsed"])
        self.assertEqual([(w["kind"], w["summary"]) for w in r["waits_opened"]],
                         [("approval", "git push origin feat/retry"), ("decision", "方式Aか方式Bか")])
        self.assertEqual(len(r["artifacts_added"]), 2)
        self.assertEqual(self.session_row("local_a")["summary"], text[:400])

    def test_no_punctuation_and_next_line_segments(self):
        r = self.report("local_a", "HQ T1 waiting-user: 実装済み Needs: review: 差分 Artifacts: branch feat/z")
        self.assertEqual(r["waits_opened"][0]["summary"], "差分")
        self.assertEqual(self.q("SELECT ref FROM artifacts")[0]["ref"], "feat/z")
        r = self.report("local_a", "HQ T1 working: 続行\nNeeds: none\nArtifacts: doc docs/x.md\n詳細")
        self.assertEqual(r["waits_resolved"], ["W1"])
        self.assertEqual(self.q("SELECT ref FROM artifacts ORDER BY num DESC")[0]["ref"], "docs/x.md")

    def test_unparseable_text_is_recorded_not_failed(self):
        rev = self.revision()
        r = self.report("local_a", "途中経過です。まだ報告行はありません。")
        self.assertEqual((r["ok"], r["parsed"], r["task"], r["state"]), (True, False, "T1", "starting"))
        self.assertEqual(self.session_row("local_a")["summary"], "途中経過です。まだ報告行はありません。")
        self.assertEqual(self.revision(), rev + 1)
        self.assertIn("unparsed", self.q("SELECT text FROM events ORDER BY id DESC LIMIT 1")[0]["text"])
        r = self.report("local_a", "HQ T9 working: 番号違い. Needs: none. Artifacts: none")
        self.assertEqual((r["parsed"], r["task"]), (True, "T1"))   # the session's mapping wins
        self.assertTrue(any("T9 (unknown)" in w and "T1" in w for w in r["warnings"]))
        r = self.report("local_orphan", "HQ T9 done: 別HQの報告. Needs: none. Artifacts: none")
        self.assertFalse(r["parsed"])
        self.assertTrue(any("unknown task T9" in w for w in r["warnings"]))

    def test_unknown_session_is_created_and_linked(self):
        r = self.report("local_new", "HQ T1 working: 調査中. Needs: none. Artifacts: none")
        self.assertEqual((r["task"], r["state"]), ("T1", "working"))
        self.assertEqual(self.session_row("local_new")["task_id"], "T1")
        r = self.report("local_other", "no status line", task="T1")
        self.assertEqual((r["task"], r["parsed"]), ("T1", False))
        r = self.report("local_orphan", "no status line")
        self.assertEqual((r["ok"], r["task"]), (True, None))

    def test_cli_report_reads_stdin_and_receipt_shape(self):
        note = "HQ T1 waiting-user: 完了。Needs: approval: git push origin feat/retry。Artifacts: PR https://github.com/o/r/pull/9。"
        code, receipt = self.cli("--hq", str(self.dir), "report", "--session", "local_a", stdin=note)
        self.assertEqual(code, 0)
        self.assertEqual(set(receipt), {"ok", "task", "session", "state", "parsed", "waits_opened",
                                        "waits_resolved", "artifacts_added"})
        self.assertEqual(receipt["waits_opened"], [{"id": "W1", "kind": "approval",
                                                    "summary": "git push origin feat/retry"}])
        code, receipt = self.cli("--hq", str(self.dir), "report", "--session", "local_a", stdin="")
        self.assertEqual((code, receipt["ok"]), (1, False))


class ReviewRegressionTest(LedgerCase):
    """One test per defect found in code review."""

    def setUp(self):
        super().setUp()
        self.t1 = self.task("一")
        self.op("launch", id=self.t1, session="s1")

    def test_1_closing_a_task_resolves_its_waits_and_closes_sessions(self):
        self.report("s1", "HQ T1 waiting-user: 準備完了. Needs: approval: git push. Artifacts: none")
        self.op("wait.add", kind="review", task="T1", summary="手動レビュー")
        self.op("session.upsert", id="s_old", task="T1", state="archived")
        r = self.op("task.update", id="T1", status="done")
        self.assertEqual((r["waits_resolved"], r["sessions_closed"]), (["W1", "W2"], ["s1"]))
        self.assertEqual(self.waits(), [])
        self.assertEqual({w["resolution"] for w in self.waits("resolved")}, {"task closed: done"})
        self.assertEqual(self.session_row("s1")["state"], "done")
        self.assertEqual(self.session_row("s_old")["state"], "archived")
        t2 = self.task("二")
        self.op("launch", id=t2, session="s2")
        self.op("wait.add", kind="decision", task=t2, summary="方針")
        r = self.op("task.update", id=t2, status="dropped")
        self.assertEqual((r["waits_resolved"], r["sessions_closed"]), (["W3"], ["s2"]))
        self.assertEqual(self.waits("resolved")[-1]["resolution"], "task closed: dropped")

    def test_2_needs_and_artifacts_in_later_paragraphs(self):
        r = self.report("s1", "HQ T1 waiting-user: need push.\n\nNeeds: approval: git push\nArtifacts: none")
        self.assertNotIn("warnings", r)
        self.assertEqual([(w["kind"], w["summary"]) for w in r["waits_opened"]], [("approval", "git push")])
        r = self.report("s1", "HQ T1 working: 続行.\n\n詳細\n\nHQ T9 done: other.\nNeeds: none")
        self.assertTrue(any("Needs" in w for w in r["warnings"]))
        self.assertEqual(r["waits_resolved"], [])

    def test_3_launch_refuses_closed_tasks_and_derives_status(self):
        self.op("task.update", id="T1", status="done")
        with self.assertRaisesRegex(hq.HQError, "T1 is done"):
            self.op("launch", id="T1", session="s9")
        t2 = self.task("二")
        self.op("wait.add", kind="approval", task=t2, summary="先に承認")
        r = self.op("launch", id=t2, session="s2")
        self.assertEqual(r["task_status"], "waiting-user")
        self.assertEqual(self.task_row(t2)["status"], "waiting-user")

    def test_4_report_never_moves_a_session_between_tasks(self):
        t2 = self.task("二")
        r = self.report("s1", "HQ T2 waiting-user: 取り違え. Needs: review: x. Artifacts: none")
        self.assertEqual(r["task"], "T1")
        self.assertEqual(self.session_row("s1")["task_id"], "T1")
        self.assertTrue(any("T1" in w and "T2" in w for w in r["warnings"]))
        self.assertEqual(self.task_row(t2)["status"], "queued")
        self.assertEqual(self.task_row("T1")["status"], "waiting-user")
        r = self.report("s1", "HQ T1 working: x. Needs: none. Artifacts: none", task=t2)
        self.assertEqual((r["task"], self.session_row("s1")["task_id"]), ("T2", "T2"))

    def test_5_reports_only_supersede_waits_they_opened(self):
        self.op("wait.add", kind="approval", task="T1", session="s1", summary="手動の承認")
        self.report("s1", "HQ T1 waiting-user: x. Needs: decision: A or B. Artifacts: none")
        r = self.report("s1", "HQ T1 working: x. Needs: none. Artifacts: none")
        self.assertEqual(r["waits_resolved"], ["W2"])
        self.assertEqual([w["id"] for w in self.waits()], ["W1"])
        self.assertEqual(self.q("SELECT id, source FROM waits ORDER BY num"),
                         [{"id": "W1", "source": "manual"}, {"id": "W2", "source": "report"}])

    def test_5_old_ledgers_are_migrated_with_known_origins(self):
        self.op("wait.add", kind="review", task="T1", session="s1", summary="manual")
        self.report("s1", "HQ T1 waiting-user: x. Needs: approval: push. Artifacts: none")
        with sqlite3.connect(self.dir / "ledger.sqlite3") as c:   # rewind to the schema-1 layout
            c.execute("ALTER TABLE waits DROP COLUMN source")
            c.execute("UPDATE meta SET value='1' WHERE key='schema'")
        r = self.report("s1", "HQ T1 working: x. Needs: none. Artifacts: none")
        self.assertEqual(r["waits_resolved"], ["W2"])
        self.assertEqual(self.q("SELECT id, source, status FROM waits ORDER BY num"),
                         [{"id": "W1", "source": "manual", "status": "open"},
                          {"id": "W2", "source": "report", "status": "resolved"}])
        self.assertEqual(self.ledger.read(lambda c: hq.get_meta(c, "schema")), hq.SCHEMA_VERSION)

    def test_6_ledger_md_is_written_after_commit_and_never_regresses(self):
        seen = []
        original = hq.Ledger.refresh_md

        def spy(ledger, force=False):
            with sqlite3.connect(ledger.db) as other:   # a separate connection sees only committed data
                seen.append(int(other.execute("SELECT value FROM meta WHERE key='revision'").fetchone()[0]))
            return original(ledger, force)
        with unittest.mock.patch.object(hq.Ledger, "refresh_md", spy):
            self.op("note", text="after commit")
        self.assertEqual(seen, [self.revision()])
        md = self.dir / "ledger.md"
        self.assertTrue(md.read_text(encoding="utf-8").startswith(f"<!-- hq-ledger revision {self.revision()} -->"))
        md.write_text("<!-- hq-ledger revision 999999 -->\nnewer\n", encoding="utf-8")
        self.op("note", text="older snapshot must not win")
        self.assertIn("newer", md.read_text(encoding="utf-8"))
        code, _ = self.cli("--hq", str(self.dir), "export")
        self.assertEqual(code, 0)
        self.assertNotIn("newer", md.read_text(encoding="utf-8"))

    def test_7_ci_runs_python_tests_when_dashboard_assets_change(self):
        ci = (ROOT.parents[1] / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("dev/hq-dashboard/assets/*)", ci)

    def test_8_artifact_urls_keep_their_commas(self):
        self.report("s1", "HQ T1 working: x. Needs: none. Artifacts: doc docs/a.md, https://x.y/a,b")
        self.assertEqual(self.q("SELECT kind, ref FROM artifacts ORDER BY num"),
                         [{"kind": "doc", "ref": "docs/a.md"}, {"kind": "url", "ref": "https://x.y/a,b"}])

    def test_9_needs_tolerates_list_markers(self):
        for text, expected in (("Needs: 1) approval: push", [("approval", "push")]),
                               ("Needs: - approval: a; ② review: b", [("approval", "a"), ("review", "b")]),
                               ("Needs: 1. approval: x 2. decision: y", [("approval", "x"), ("decision", "y")]),
                               ("Needs:\n• approval: m\n• review: n", [("approval", "m"), ("review", "n")])):
            with self.subTest(text=text):
                r = self.report("s1", f"HQ T1 waiting-user: x.\n{text}\nArtifacts: none")
                self.assertEqual(sorted((w["kind"], w["summary"]) for w in self.waits() if w["session_id"] == "s1"),
                                 sorted(expected), r)


class TimingStatsTest(LedgerCase):
    def at(self, minute, action, *args, **kwargs):
        ts = f"2026-11-20T{minute // 60:02d}:{minute % 60:02d}:00Z"
        with unittest.mock.patch.object(hq, "now", return_value=ts):
            return action(*args, **kwargs)

    def test_completion_uses_transition_and_merges_overlapping_waits(self):
        task = self.at(0, self.task)
        self.at(1, self.task, "Imported completed task", status="done")
        approval = self.at(10, self.op, "wait.add", task=task, kind="approval", summary="approve")["id"]
        review = self.at(25, self.op, "wait.add", task=task, kind="review", summary="review")["id"]
        self.at(40, self.op, "wait.resolve", id=approval)
        self.at(50, self.op, "wait.resolve", id=review)
        self.at(60, self.op, "wait.add", task=task, kind="decision", summary="decide")
        self.at(70, self.op, "task.update", id=task, status="done")
        launch = self.at(80, self.op, "wait.add", task=task, kind="launch", summary="launch")["id"]
        self.at(90, self.op, "wait.resolve", id=launch)
        self.at(100, self.op, "task.update", id=task, title="Edited after completion")

        state = self.ledger.read(lambda c: hq.snapshot(c, events_limit=0))
        self.assertEqual(state["events"], [])
        self.assertEqual(state["timings"]["completion"],
                         {"count": 1, "total_seconds": 4200, "wait_seconds": 3000,
                          "agent_seconds": 0, "agent_tasks": 0})
        self.assertEqual(state["timings"]["resolved_waits"]["decision"],
                         {"count": 1, "median_seconds": 600})
        self.at(120, self.op, "task.update", id=task, status="active")
        self.assertEqual(self.ledger.read(hq.timing_stats)["completion"]["count"], 0)
        self.at(130, self.op, "task.update", id=task, status="done")
        self.assertEqual(self.ledger.read(hq.timing_stats)["completion"],
                         {"count": 1, "total_seconds": 7800, "wait_seconds": 3600,
                          "agent_seconds": 0, "agent_tasks": 0})

    def test_completed_turns_are_clipped_and_waits_take_precedence(self):
        task = self.at(0, self.task)
        for session in ("a", "b"):
            self.at(0, self.op, "session.upsert", id=session, task=task, provider="codex")
        wait = self.at(15, self.op, "wait.add", task=task, kind="approval", summary="approve")["id"]
        self.at(25, self.op, "wait.resolve", id=wait)
        self.at(35, self.op, "task.update", id=task, status="done")
        base = int(hq.datetime(2026, 11, 20, tzinfo=hq.timezone.utc).timestamp())

        def ingest(session, cursor, previous, turn, start, end):
            return self.at(40, self.op, "ingest", session=session, cursor=cursor, after_cursor=previous,
                           turn_id=turn, turn_started_at=str(base + start * 60),
                           turn_completed_at=str(base + end * 60))

        ingest("a", "1", "", "turn-a", -5, 20)
        ingest("a", "2", "1", "turn-a", -5, 50)
        self.assertFalse(ingest("a", "stale", "1", "turn-stale", 0, 35)["accepted"])
        ingest("b", "1", "", "turn-b", 10, 30)
        with self.assertRaisesRegex(hq.HQError, "completion must be"):
            ingest("b", "bad", "1", "turn-bad", 50, 40)
        self.assertEqual(self.session_row("b")["receive_cursor"], "1")
        state = self.ledger.read(hq.snapshot)
        self.assertEqual(state["timings"]["completion"],
                         {"count": 1, "total_seconds": 2100, "wait_seconds": 600,
                          "agent_seconds": 1200, "agent_tasks": 1})
        ingests = [event["text"] for event in state["events"] if event["type"] == "ingest"]
        self.assertEqual(ingests, ["snapshot received; report absent"] * 3)
        ledger_md = self.ledger.md.read_text(encoding="utf-8")
        self.assertIn("snapshot received; report absent", ledger_md)
        self.assertNotIn(hq.TURN_TIMING_MARKER, ledger_md)

    def test_resolved_waits_use_full_history(self):
        for i in range(hq.API_RESOLVED_WAITS + 1):
            wait = self.at(0, self.op, "wait.add", kind="approval", summary=f"request {i}")["id"]
            self.at(i, self.op, "wait.resolve", id=wait)
        state = self.ledger.read(hq.snapshot)
        self.assertEqual(len(state["waits"]), hq.API_RESOLVED_WAITS)
        self.assertEqual(state["timings"]["resolved_waits"]["approval"],
                         {"count": 51, "median_seconds": 1500})


class ServerTest(LedgerCase):
    def start(self):
        proc = subprocess.Popen([sys.executable, str(SCRIPT), "--hq", str(self.dir), "serve", "--port", "0"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: (proc.terminate(), proc.wait(5), proc.stdout.close(), proc.stderr.close()))
        url = proc.stdout.readline().strip()
        self.assertRegex(url, r"^http://127\.0\.0\.1:\d+/$")
        return url

    def test_state_endpoint_page_and_read_only(self):
        self.task()
        url = self.start()
        with urlopen(url + "api/state", timeout=5) as response:
            self.assertEqual(response.headers["Cache-Control"], "no-store")
            state = json.loads(response.read())
        self.assertEqual((state["lang"], len(state["tasks"])), ("ja", 1))
        for key in ("revision", "sessions", "edges", "waits", "artifacts", "events", "events_total", "timings"):
            self.assertIn(key, state)
        with urlopen(f"{url}api/state?since={state['revision']}", timeout=5) as response:
            self.assertEqual(json.loads(response.read()), {"revision": state["revision"], "unchanged": True})
        self.op("note", text="更新")
        with urlopen(f"{url}api/state?since={state['revision']}", timeout=5) as response:
            self.assertEqual(json.loads(response.read())["revision"], state["revision"] + 1)
        with urlopen(url, timeout=5) as response:
            page = response.read().decode()
        self.assertIn('<html lang="ja">', page)
        embedded = re.search(r'<script id="hq-initial" type="application/json">(.*?)</script>', page, re.S)
        self.assertEqual(json.loads(embedded.group(1))["tasks"][0]["title"], "タスク")
        self.assertIn("default-src 'none'", response.headers["Content-Security-Policy"])
        for method in ("POST", "PUT", "DELETE", "PATCH"):
            with self.subTest(method=method):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(Request(url + "api/state", data=b"{}", method=method), timeout=5)
                self.assertEqual(caught.exception.code, 405)
                self.assertEqual(caught.exception.headers["Allow"], "GET")
                caught.exception.close()
        with self.assertRaises(HTTPError) as caught:
            urlopen(url + "nope", timeout=5)
        self.assertEqual(caught.exception.code, 404)
        caught.exception.close()
        with self.assertRaises(HTTPError) as caught:
            urlopen(Request(url + "api/state", headers={"Host": "evil.example"}), timeout=5)
        self.assertEqual(caught.exception.code, 403)
        caught.exception.close()
        status = self.ledger.read(hq.status_data)
        self.assertEqual(status["server_url"], url)
        self.assertTrue(hq.probe_server(url, status["revision"]))

    def test_port_in_use_is_a_json_error(self):
        url = self.start()
        port = url.rsplit(":", 1)[1].strip("/")
        code, receipt = self.cli("--hq", str(self.dir), "serve", "--port", port)
        self.assertEqual((code, receipt["ok"]), (1, False))
        self.assertIn("cannot listen", receipt["error"])


class PageTest(LedgerCase):
    def test_initial_state_is_embedded_without_breaking_out(self):
        hostile = '</script><script>alert(1)</script><!-- & "x"'
        self.task(hostile)
        page = hq.render_page(ASSET.read_text(encoding="utf-8"), self.ledger.read(hq.snapshot))
        self.assertNotIn("<script>alert", page)
        self.assertEqual(page.count("</script>"), ASSET.read_text(encoding="utf-8").count("</script>"))
        embedded = re.search(r'<script id="hq-initial" type="application/json">(.*?)</script>', page, re.S)
        self.assertEqual(json.loads(embedded.group(1))["tasks"][0]["title"], hostile)
        self.assertIn('<html lang="ja">', page)


class AssetAndCliTest(unittest.TestCase):
    def test_asset_never_injects_html(self):
        page = ASSET.read_text(encoding="utf-8")
        for sink in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function"):
            self.assertNotIn(sink, page)
        self.assertNotRegex(page, r"(?i)<(script|link|img)[^>]+(src|href)=[\"']https?:")
        self.assertIn("textContent", page)
        self.assertIn("/api/state", page)
        self.assertIn('<html lang="en">', page)
        self.assertIn('<script id="hq-initial" type="application/json">null</script>', page)
        self.assertNotIn("user-select", page)

    def test_refresh_does_not_rebuild_an_unchanged_or_selected_panel(self):
        # Static check of the guard the browser run verified: polling re-renders skip the pinned
        # detail panel and the waits column when their data signature is unchanged, defer while
        # text is selected inside them, and catch up on selectionchange.
        page = ASSET.read_text(encoding="utf-8")
        for fn, sig, pending, node in (("renderDetail", "detailSig", "detailPending", "box"),
                                       ("renderWaits", "waitsSig", "waitsPending", "list")):
            body = page[page.index(f"function {fn}(force)"):]
            guard = body.index(f"if (!force && sig === {sig}")
            defer = body.index(f"if (!force && selectionInside({node})) {{ {pending} = true; return; }}")
            rebuild = body.index(".replaceChildren(")
            self.assertLess(guard, rebuild)
            self.assertLess(defer, rebuild)
        self.assertIn("addEventListener('selectionchange'", page)
        self.assertIn("navigator.clipboard.writeText", page)

    def test_side_column_toggle_is_accessible_and_storage_optional(self):
        page = ASSET.read_text(encoding="utf-8")
        self.assertRegex(page, r'<button[^>]*id="side-btn"[^>]*aria-controls="side-body"[^>]*aria-expanded="true"')
        self.assertIn('id="side-body"', page)
        # Every storage access is wrapped so the page works when storage is blocked.
        for line in page.splitlines():
            if "localStorage" in line:
                self.assertIn("try {", line)
        for key in ("sideClose", "sideOpen"):
            self.assertEqual(page.count(f"{key}:'"), 2)  # en and ja labels
        self.assertIn("@media (prefers-reduced-motion: reduce) { :root { --slide:0s; } }", page)

    def test_help_and_usage_errors(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        for command in ("report", "launch", "apply", "serve", "status"):
            self.assertIn(command, proc.stdout)
        proc = subprocess.run([sys.executable, str(SCRIPT), "launch"], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(json.loads(proc.stdout)["ok"])

    def test_status_text_and_json(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = hq.Ledger(temp)
            ledger.init("en")
            ledger.mutate([("task.add", hq.op_task_add, {"title": "Fix", "target": "r", "deliverable": "PR",
                                                         "done": "green CI", "authority": "push feat/x"})])
            out = subprocess.run([sys.executable, str(SCRIPT), "--hq", temp, "status"], capture_output=True,
                                 text=True).stdout
            self.assertIn("T1 [queued] Fix", out)
            self.assertIn("authority: push feat/x", out)
            data = json.loads(subprocess.run([sys.executable, str(SCRIPT), "--hq", temp, "status", "--json"],
                                             capture_output=True, text=True).stdout)
            self.assertEqual((data["counts"]["queued"], data["tasks"][0]["done_criteria"]), (1, "green CI"))
            self.assertFalse(data["server_alive"])



class CodexTransportTest(LedgerCase):
    def launch(self):
        tid = self.task()
        self.op("launch", id=tid, session="worker", provider="codex", host_id="local", thread_id="thread")
        return tid

    def ingest(self, cursor, previous, **extra):
        return self.op("ingest", session="worker", cursor=cursor, after_cursor=previous, **extra)

    def test_pending_launch_recovers_without_resolving_wait_early(self):
        tid = self.task()
        wid = self.op("wait.add", kind="launch", task=tid, summary="launch")["id"]
        receipt = self.op("launch", id=tid, session="worker", provider="codex", client_thread_id="queued")
        self.assertTrue(receipt["pending"])
        self.assertEqual(self.task_row(tid)["status"], "queued")
        self.assertEqual(self.session_row("worker")["thread_id"], "")
        self.assertEqual(self.waits()[0]["id"], wid)
        with self.assertRaisesRegex(hq.HQError, "requires thread_id"):
            self.op("launch", id=tid, session="worker")
        self.assertEqual(self.waits()[0]["id"], wid)
        self.assertEqual(self.task_row(tid)["status"], "queued")
        receipt = self.op("launch", id=tid, session="worker", provider="codex", host_id="local", thread_id="ready")
        self.assertEqual(receipt["waits_resolved"], [wid])
        self.assertEqual(self.session_row("worker")["client_thread_id"], "queued")
        self.assertEqual(self.session_row("worker")["thread_id"], "ready")

    def test_repeated_old_and_duplicate_reports_do_not_reopen_waits(self):
        tid = self.launch()
        text = f"HQ {tid} waiting-user: ask. Needs: review: inspect. Artifacts: none"
        first = self.ingest("opaque-z", "", report_id="message-1", text=text)
        wid = first["report"]["waits_opened"][0]["id"]
        self.op("wait.resolve", id=wid, resolution="reviewed")
        self.assertFalse(self.ingest("opaque-z", "")["accepted"])
        duplicate = self.ingest("opaque-a", "opaque-z", report_id="message-1", text=text)
        self.assertTrue(duplicate["report_duplicate"])
        self.assertEqual(duplicate["report"], first["report"])
        self.assertEqual(self.waits(), [])
        self.assertFalse(self.ingest("old", "")["accepted"])
        self.assertFalse(self.ingest("opaque-z", "opaque-a")["accepted"])
        self.assertEqual(self.session_row("worker")["receive_cursor"], "opaque-a")

    def test_native_no_report_snapshot_keeps_report_state_and_waits(self):
        tid = self.launch()
        self.ingest("1", "", report_id="m", text=f"HQ {tid} blocked: wait. Needs: approval: publish. Artifacts: none")
        self.ingest("2", "1", native_status="completed")
        row = self.session_row("worker")
        self.assertEqual((row["native_status"], row["reported_state"], row["state"]), ("completed", "blocked", "blocked"))
        self.assertEqual(len(self.waits()), 1)
        self.assertEqual(self.task_row(tid)["status"], "waiting-user")

    def test_receive_and_report_rollback_together(self):
        tid = self.launch()
        params = dict(session="worker", cursor="x", after_cursor="", report_id="m",
                      text=f"HQ {tid} done: finished. Needs: none. Artifacts: branch test")
        before = self.revision()
        with self.assertRaises(hq.HQError):
            self.ledger.mutate([("ingest", hq.op_ingest, params),
                                ("task.update", hq.op_task_update, {"id": "missing"})])
        self.assertEqual(self.revision(), before)
        self.assertEqual(self.session_row("worker")["receive_cursor"], "")
        self.assertEqual(self.q("SELECT * FROM report_receipts"), [])
        receipt = self.op("ingest", **params)
        self.assertTrue(receipt["accepted"])
        self.assertFalse(receipt["report_duplicate"])
        self.assertEqual(self.task_row(tid)["status"], "active")

    def test_schema_2_migration_preserves_existing_records(self):
        tid = self.launch()
        self.report("worker", f"HQ {tid} working: prior. Needs: approval: approve. Artifacts: none")
        with sqlite3.connect(self.ledger.db) as c:
            for key in hq.TRANSPORT_FIELDS + ("receive_cursor", "reported_state"):
                c.execute(f"ALTER TABLE sessions DROP COLUMN {key}")
            c.execute("DROP TABLE report_receipts")
            c.execute("DROP TABLE received_snapshots")
            c.execute("UPDATE meta SET value='2' WHERE key='schema'")
        self.op("note", text="migrate")
        self.assertEqual(self.session_row("worker")["summary"].split(':')[0], f"HQ {tid} working")
        self.assertEqual(self.session_row("worker")["thread_id"], "")
        self.assertEqual(len(self.waits()), 1)
        self.assertEqual(self.ledger.read(lambda c: hq.get_meta(c, "schema")), "3")

    def test_flattened_final_note_does_not_turn_explanation_into_artifact(self):
        tid = self.launch()
        text = (f"HQ {tid} done: verified behavior. Needs: none. Artifacts: none. "
                f"Additional explanation of HQ {tid} done and command behavior.")
        receipt = self.ingest("final", "", report_id="final-message", text=text)
        self.assertTrue(receipt["report"]["parsed"])
        self.assertEqual(receipt["report"]["artifacts_added"], [])
        self.assertEqual(receipt["report"]["waits_opened"], [])
        self.assertEqual(self.session_row("worker")["reported_state"], "done")
        self.assertEqual(self.task_row(tid)["status"], "active")
        self.ingest("new", "final", report_id="new-message",
                    text=f"HQ {tid} working: resumed. Needs: none. Artifacts: none")
        old = self.ingest("repeat", "new", report_id="final-message", text=text)
        self.assertTrue(old["report_duplicate"])
        self.assertEqual(self.session_row("worker")["reported_state"], "working")

    def test_flattened_nonempty_artifacts_end_at_explicit_marker(self):
        tid = self.launch()
        text = (f"HQ {tid} done: result. Needs: none. Artifacts: branch feature/x; "
                "PR https://example.test/pull/1. EndHQ. More explanation; unrelated prose.")
        receipt = self.ingest("final", "", report_id="message", text=text)
        self.assertEqual(len(receipt["report"]["artifacts_added"]), 2)
        self.assertEqual([a["ref"] for a in self.q("SELECT ref FROM artifacts ORDER BY num")],
                         ["feature/x", "https://example.test/pull/1"])

    def test_ingest_cli_reads_report_from_stdin_only_with_report_id(self):
        tid = self.launch()
        raw = f"HQ {tid} done: result. Needs: none. Artifacts: none. EndHQ."
        code, receipt = self.cli("--hq", str(self.dir), "ingest", "--session", "worker", "--cursor", "a",
                                 "--after-cursor", "", "--report-id", "message", stdin=raw)
        self.assertEqual(code, 0)
        self.assertTrue(receipt["report"]["parsed"])
        args = hq.build_parser().parse_args(["--hq", str(self.dir), "ingest", "--session", "worker",
                                            "--cursor", "b", "--after-cursor", "a"])
        with unittest.mock.patch.object(hq, "read_stdin", side_effect=AssertionError("must not read")):
            self.assertTrue(hq.run(args)["accepted"])
        code, receipt = self.cli("--hq", str(self.dir), "ingest", "--session", "worker", "--cursor", "c",
                                 "--after-cursor", "b", "--report-id", "empty", stdin="")
        self.assertEqual(code, 1)
        self.assertFalse(receipt["ok"])
        self.assertEqual(self.session_row("worker")["receive_cursor"], "b")

    def test_cli_status_recovers_wait_checkpoint_after_restart(self):
        self.launch()
        self.ingest("saved-cursor", "", native_status="active")
        code, status = self.cli("--hq", str(self.dir), "status", "--json")
        self.assertEqual(code, 0)
        session = status["tasks"][0]["sessions"][0]
        self.assertEqual((session["provider"], session["host_id"], session["thread_id"]),
                         ("codex", "local", "thread"))
        self.assertEqual(session["receive_cursor"], "saved-cursor")
        self.assertEqual(status["sessions"][0], session)
        code, receipt = self.cli("--hq", str(self.dir), "ingest", "--session", session["id"],
                                 "--cursor", "next-cursor", "--after-cursor", session["receive_cursor"])
        self.assertEqual(code, 0)
        self.assertTrue(receipt["accepted"])

    def test_schema_2_status_is_readable_before_migration(self):
        self.launch()
        with sqlite3.connect(self.ledger.db) as c:
            for key in hq.TRANSPORT_FIELDS + ("receive_cursor", "reported_state"):
                c.execute(f"ALTER TABLE sessions DROP COLUMN {key}")
            c.execute("DROP TABLE report_receipts")
            c.execute("DROP TABLE received_snapshots")
            c.execute("UPDATE meta SET value='2' WHERE key='schema'")
        code, status = self.cli("--hq", str(self.dir), "status", "--json")
        self.assertEqual(code, 0)
        session = status["tasks"][0]["sessions"][0]
        self.assertEqual(session["thread_id"], "")
        self.assertEqual(session["receive_cursor"], "")
        self.assertEqual(self.ledger.read(lambda c: hq.get_meta(c, "schema")), "2")

    def test_cli_metadata_and_ingest(self):
        tid = self.task()
        code, receipt = self.cli("--hq", str(self.dir), "launch", tid, "--session", "worker",
                                 "--provider", "codex", "--host-id", "local", "--thread-id", "thread")
        self.assertEqual(code, 0)
        code, receipt = self.cli("--hq", str(self.dir), "ingest", "--session", "worker", "--cursor", "one",
                                 "--after-cursor", "", "--native-status", "idle")
        self.assertEqual(code, 0)
        self.assertTrue(receipt["accepted"])
        self.assertEqual(self.session_row("worker")["native_status"], "idle")


if __name__ == "__main__":
    unittest.main()
