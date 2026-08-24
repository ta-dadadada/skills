from __future__ import annotations

import dataclasses
import json
import queue
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from local_intake.cli import build_parser, main  # noqa: E402
from local_intake.document import (  # noqa: E402
    FORM_BEGIN,
    FORM_END,
    STATE_MARKER,
    cleanup_document,
    ensure_local_exclude,
    parse_pending_document,
    read_pending_document,
    replace_pending_block,
)
from local_intake.markdown import render_log_entry  # noqa: E402
from local_intake.render import CSS, SCRIPT, render_form  # noqa: E402
from local_intake.server import create_server, serve_document  # noqa: E402
from local_intake.spec import FormSpec, ProtocolError  # noqa: E402
from local_intake.submission import (  # noqa: E402
    OTHER_VALUE,
    Answers,
    SubmissionError,
    normalize_submission,
)


def sample_raw_spec(*, mode: str = "intake", round_number: int = 1) -> dict:
    raw = {
        "version": 1,
        "round": round_number,
        "mode": mode,
        "language": "ja",
        "title": "依頼を整理する",
        "intro": "分かる範囲で回答してください。",
        "context": "既知の条件はローカル完結です。\n回答は依頼書案の作成に使います。",
        "ui": {
            "app_label": "ローカル質問票",
            "round_label": "ラウンド",
            "progress_label": "回答済み",
            "required_label": "必須",
            "optional_label": "任意",
            "other_label": "その他",
            "context_label": "前提",
            "draft_label": "現在の依頼書案",
            "save_label": "回答を保存",
            "saving_label": "保存中…",
            "saved_title": "保存しました",
            "saved_message": "会話へ戻ってください。",
            "validation_message": "強調された質問へ回答してください。",
        },
        "sections": [
            {
                "id": "purpose",
                "title": "目的",
                "description": "何を変えたいか",
                "questions": [
                    {
                        "id": "outcome",
                        "prompt": "完了時に何が変わりますか？",
                        "context": "この回答で依頼の達成目標を固定します。",
                        "help": "観測できる結果を書いてください。",
                        "type": "long_text",
                        "required": True,
                        "placeholder": "結果は…",
                    },
                    {
                        "id": "priority",
                        "prompt": "優先するものは？",
                        "type": "single_choice",
                        "required": True,
                        "options": ["速度", "品質", "不明"],
                        "allow_other": True,
                    },
                    {
                        "id": "constraints",
                        "prompt": "該当する制約は？",
                        "type": "multiple_choice",
                        "required": False,
                        "options": ["予算", "期限"],
                        "allow_other": True,
                    },
                ],
            }
        ],
    }
    if mode == "review":
        raw["draft"] = "# 依頼書案\n\n目的を達成する。"
    return raw


def sample_spec(*, mode: str = "intake", round_number: int = 1) -> FormSpec:
    return FormSpec.parse(sample_raw_spec(mode=mode, round_number=round_number))


def document_text(raw_spec: dict, *, status: str = "collecting", round_number: int = 0) -> str:
    return f"""{STATE_MARKER}
# Local Intake (temporary)

Status: {status}
Round: {round_number}/3

## Working brief

作業中。

## Blocking open questions

- 未回答

## Interview log

{FORM_BEGIN}
{json.dumps(raw_spec, ensure_ascii=False, indent=2)}
{FORM_END}
"""


class LabelTargetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.label_targets: list[str] = []
        self.fieldsets = 0
        self.legends = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        mapping = dict(attrs)
        if mapping.get("id"):
            self.ids.add(mapping["id"] or "")
        if tag == "label" and mapping.get("for"):
            self.label_targets.append(mapping["for"] or "")
        if tag == "fieldset":
            self.fieldsets += 1
        if tag == "legend":
            self.legends += 1


class SpecTests(unittest.TestCase):
    def test_parses_once_into_frozen_typed_model(self) -> None:
        spec = sample_spec()
        self.assertIsInstance(spec, FormSpec)
        self.assertIsInstance(spec.sections, tuple)
        self.assertIsInstance(spec.sections[0].questions, tuple)
        self.assertTrue(spec.sections[0].questions[1].allow_other)
        self.assertFalse(spec.sections[0].questions[0].allow_other)
        self.assertIn("ローカル完結", spec.context)
        self.assertIn("達成目標", spec.sections[0].questions[0].context)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            spec.round = 2  # type: ignore[misc]

    def test_rejects_bool_as_round(self) -> None:
        raw = sample_raw_spec()
        raw["round"] = True
        with self.assertRaisesRegex(ProtocolError, "round must be"):
            FormSpec.parse(raw)

    def test_context_fields_remain_optional_with_stable_defaults(self) -> None:
        raw = sample_raw_spec()
        raw.pop("context")
        raw["ui"].pop("context_label")
        raw["sections"][0]["questions"][0].pop("context")
        spec = FormSpec.parse(raw)
        self.assertEqual(spec.context, "")
        self.assertEqual(spec.ui.context_label, "Context")
        self.assertEqual(spec.sections[0].questions[0].context, "")

    def test_review_requires_complete_draft(self) -> None:
        raw = sample_raw_spec(mode="review", round_number=2)
        raw.pop("draft")
        with self.assertRaisesRegex(ProtocolError, "required for review"):
            FormSpec.parse(raw)

    def test_rejects_duplicate_question_ids_with_context(self) -> None:
        raw = sample_raw_spec()
        raw["sections"][0]["questions"][1]["id"] = "outcome"
        with self.assertRaisesRegex(ProtocolError, "duplicate question id: outcome"):
            FormSpec.parse(raw)


class DocumentTests(unittest.TestCase):
    def test_pure_parser_returns_typed_spec_and_span(self) -> None:
        content = document_text(sample_raw_spec())
        pending = parse_pending_document(content)
        self.assertIsInstance(pending.spec, FormSpec)
        self.assertEqual(content[pending.form_span[0] :].splitlines()[0], FORM_BEGIN)

    def test_file_reader_delegates_to_pure_parser(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            self.assertEqual(read_pending_document(path).spec, sample_spec())

    def test_replaces_form_atomically_with_rendered_log(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            pending = read_pending_document(path)
            answers = Answers(
                {
                    "outcome": "一行目\n二行目 <script>",
                    "priority": "品質",
                    "constraints": ("期限",),
                }
            )
            replace_pending_block(path, pending, render_log_entry(pending.spec, answers))
            updated = path.read_text(encoding="utf-8")
            self.assertIn("> 一行目\n> 二行目 <script>", updated)
            self.assertNotIn(FORM_BEGIN, updated)

    def test_marker_text_inside_answer_is_not_a_protocol_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            pending = read_pending_document(path)
            answers = Answers({"outcome": FORM_BEGIN, "priority": "品質", "constraints": ()})
            replace_pending_block(path, pending, render_log_entry(pending.spec, answers))
            self.assertIn(f"> {FORM_BEGIN}", path.read_text(encoding="utf-8"))


class SubmissionTests(unittest.TestCase):
    def test_normalizes_text_choices_and_other_to_immutable_values(self) -> None:
        payload = {
            "outcome": ["  利用者が迷わない  "],
            "priority": [OTHER_VALUE],
            "priority__other_text": ["安全性"],
            "constraints": ["期限", OTHER_VALUE],
            "constraints__other_text": ["端末内のみ"],
        }
        answers = normalize_submission(sample_spec(), payload)
        self.assertEqual(answers["outcome"], "利用者が迷わない")
        self.assertEqual(answers["priority"], "安全性")
        self.assertEqual(answers["constraints"], ("期限", "端末内のみ"))

    def test_rejects_missing_required_answer(self) -> None:
        with self.assertRaises(SubmissionError) as raised:
            normalize_submission(sample_spec(), {"priority": ["品質"]})
        self.assertEqual(raised.exception.question_ids, ["outcome"])

    def test_rejects_unknown_choice_even_when_optional(self) -> None:
        payload = {"outcome": ["完了"], "priority": ["品質"], "constraints": ["勝手な値"]}
        with self.assertRaisesRegex(SubmissionError, "unknown choice"):
            normalize_submission(sample_spec(), payload)

    def test_rejects_reserved_other_when_disabled(self) -> None:
        raw = sample_raw_spec()
        raw["sections"][0]["questions"][1]["allow_other"] = False
        spec = FormSpec.parse(raw)
        payload = {"outcome": ["完了"], "priority": [OTHER_VALUE]}
        with self.assertRaisesRegex(SubmissionError, "where it is disabled"):
            normalize_submission(spec, payload)

    def test_rejects_unknown_form_field(self) -> None:
        payload = {"outcome": ["完了"], "priority": ["品質"], "stale-question": ["値"]}
        with self.assertRaisesRegex(SubmissionError, "unknown field"):
            normalize_submission(sample_spec(), payload)

    def test_multiline_list_answer_keeps_markdown_nesting(self) -> None:
        answers = Answers({"outcome": "完了", "priority": "品質", "constraints": ("一行目\n二行目",)})
        rendered = render_log_entry(sample_spec(), answers)
        self.assertIn("> - 一行目\n>   二行目", rendered)


class RenderingTests(unittest.TestCase):
    def test_css_and_javascript_are_static_unescaped_sources(self) -> None:
        self.assertIn(":root {", CSS)
        self.assertNotIn("{{", CSS)
        self.assertNotIn("position: sticky; bottom: 16px", CSS)
        self.assertIn("max-width: 22ch", CSS)
        self.assertIn("color: #4f5967", CSS)
        self.assertIn("function answerState(card) {", SCRIPT)
        self.assertNotIn("{{", SCRIPT)

    def test_render_escapes_content_and_keeps_http_out_of_renderer(self) -> None:
        raw = sample_raw_spec()
        raw["sections"][0]["questions"][0]["prompt"] = "<script>alert(1)</script>"
        page = render_form(FormSpec.parse(raw)).decode("utf-8")
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn('action=""', page)
        self.assertNotIn("token", page)

    def test_renders_shared_and_question_context_as_escaped_plain_text(self) -> None:
        raw = sample_raw_spec()
        raw["context"] = "既知: <外部送信なし>\n用途: 回答判断"
        raw["sections"][0]["questions"][0]["context"] = "理由: <目標を固定>"
        page = render_form(FormSpec.parse(raw)).decode("utf-8")
        self.assertIn('class="form-context"', page)
        self.assertIn("既知: &lt;外部送信なし&gt;\n用途: 回答判断", page)
        self.assertIn('id="outcome-context"', page)
        self.assertIn("理由: &lt;目標を固定&gt;", page)
        self.assertIn('aria-describedby="outcome-context outcome-help"', page)
        self.assertNotIn("<外部送信なし>", page)

    def test_choice_groups_use_fieldset_legend_and_valid_label_targets(self) -> None:
        page = render_form(sample_spec()).decode("utf-8")
        parser = LabelTargetParser()
        parser.feed(page)
        self.assertEqual(parser.fieldsets, 2)
        self.assertEqual(parser.legends, 2)
        self.assertTrue(set(parser.label_targets).issubset(parser.ids))

    def test_help_is_described_by_the_control_or_fieldset(self) -> None:
        raw = sample_raw_spec()
        raw["sections"][0]["questions"][1]["help"] = "一つ選びます。"
        page = render_form(FormSpec.parse(raw)).decode("utf-8")
        self.assertIn('aria-describedby="priority-help"', page)
        self.assertIn('id="priority-help"', page)

    def test_validation_copy_flows_through_form_dataset(self) -> None:
        page = render_form(sample_spec()).decode("utf-8")
        self.assertIn('data-validation-message="強調された質問へ回答してください。"', page)
        self.assertIn("form.dataset.validationMessage", SCRIPT)
        self.assertIn("[data-other]:checked", SCRIPT)


def run_server(server) -> threading.Thread:
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    thread.start()
    return thread


class ServerTests(unittest.TestCase):
    def test_get_returns_form_and_unknown_path_is_404(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            server = create_server(path, sample_spec(), "known-token")
            thread = run_server(server)
            host, port = server.server_address
            try:
                with urllib.request.urlopen(f"http://{host}:{port}/known-token", timeout=2) as response:
                    self.assertEqual(response.status, 200)
                with self.assertRaises(urllib.error.HTTPError) as raised:
                    urllib.request.urlopen(f"http://{host}:{port}/wrong", timeout=2)
                self.assertEqual(raised.exception.code, 404)
                raised.exception.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_slow_connection_does_not_block_valid_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            server = create_server(path, sample_spec(), "known-token")
            thread = run_server(server)
            host, port = server.server_address
            slow = socket.create_connection((host, port), timeout=2)
            slow.sendall(b"GET /known-token HTTP/1.1\r\nHost: localhost\r\n")
            try:
                started = time.monotonic()
                with urllib.request.urlopen(f"http://{host}:{port}/known-token", timeout=2) as response:
                    self.assertEqual(response.status, 200)
                self.assertLess(time.monotonic() - started, 1.5)
                self.assertEqual(server.RequestHandlerClass.timeout, 30)
            finally:
                slow.close()
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

    def test_post_writes_once_and_finishes_server(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            urls: queue.Queue[str] = queue.Queue()
            result: list[int] = []
            thread = threading.Thread(
                target=lambda: result.append(serve_document(path, 5, urls.put)),
                daemon=True,
            )
            thread.start()
            url = urls.get(timeout=2)
            body = urllib.parse.urlencode(
                {"outcome": "依頼書が完成する", "priority": "品質", "constraints": ["予算", "期限"]},
                doseq=True,
            ).encode("utf-8")
            request = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            with urllib.request.urlopen(request, timeout=2) as response:
                self.assertEqual(response.status, 200)
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())
            self.assertEqual(result, [0])
            self.assertIn("依頼書が完成する", path.read_text(encoding="utf-8"))


class LifecycleTests(unittest.TestCase):
    def test_registers_any_repo_relative_document_in_git_local_exclude(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            nested = root / "work"
            nested.mkdir()
            path = nested / "intake.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            self.assertEqual(ensure_local_exclude(path), "added")
            self.assertEqual(ensure_local_exclude(path), "present")
            exclude_result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--git-path", "info/exclude"],
                capture_output=True,
                text=True,
                check=True,
            )
            exclude_path = Path(exclude_result.stdout.strip())
            if not exclude_path.is_absolute():
                exclude_path = root / exclude_path
            self.assertIn("/work/intake.md", exclude_path.read_text(encoding="utf-8").splitlines())

    def test_cli_exposes_explicit_git_exclude_opt_out(self) -> None:
        options = build_parser().parse_args(["--document", "intake.md", "--no-git-exclude"])
        self.assertTrue(options.no_git_exclude)

    def test_prepare_excludes_future_document_before_it_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            path = root / ".agent-intake.local.md"
            self.assertFalse(path.exists())
            self.assertEqual(main(["--document", str(path), "--prepare"]), 0)
            self.assertFalse(path.exists())
            exclude_result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--git-path", "info/exclude"],
                capture_output=True,
                text=True,
                check=True,
            )
            exclude_path = Path(exclude_result.stdout.strip())
            if not exclude_path.is_absolute():
                exclude_path = root / exclude_path
            self.assertIn("/.agent-intake.local.md", exclude_path.read_text(encoding="utf-8"))

    def test_cleanup_removes_terminal_owned_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            content = document_text(sample_raw_spec(), status="agreed").split(FORM_BEGIN)[0]
            path.write_text(content, encoding="utf-8")
            cleanup_document(path)
            self.assertFalse(path.exists())

    def test_cleanup_refuses_active_or_pending_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".agent-intake.local.md"
            path.write_text(document_text(sample_raw_spec()), encoding="utf-8")
            with self.assertRaisesRegex(ProtocolError, "pending form"):
                cleanup_document(path)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
