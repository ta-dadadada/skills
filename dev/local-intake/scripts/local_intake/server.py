"""単発フォームの薄いHTTP層。"""

from __future__ import annotations

import secrets
import sys
import threading
import urllib.parse
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable

from .document import read_pending_document, replace_pending_block
from .markdown import render_log_entry
from .render import render_form, render_message_page
from .spec import FormSpec, ProtocolError
from .submission import SubmissionError, normalize_submission


MAX_BODY_BYTES = 1024 * 1024


@dataclass
class ServerState:
    document: Path
    spec: FormSpec
    token: str
    accepted: threading.Event = field(default_factory=threading.Event)
    completed: threading.Event = field(default_factory=threading.Event)
    write_lock: threading.Lock = field(default_factory=threading.Lock)


class IntakeHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = False

    def __init__(self, address: tuple[str, int], handler: type[BaseHTTPRequestHandler], state: ServerState) -> None:
        self.state = state
        super().__init__(address, handler)


def make_handler(state: ServerState) -> type[BaseHTTPRequestHandler]:
    class IntakeHandler(BaseHTTPRequestHandler):
        server_version = "LocalIntake/1"
        timeout = 30

        def log_message(self, fmt: str, *args: object) -> None:
            sys.stderr.write(f"local-intake: {fmt % args}\n")

        def _send(self, status: int, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
                "form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
            )
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)

        def _path_is_valid(self) -> bool:
            actual = urllib.parse.urlsplit(self.path).path
            expected = f"/{state.token}"
            return secrets.compare_digest(actual, expected)

        def _error(self, status: int, title: str, message: str) -> None:
            self._send(status, render_message_page(title, message, language=state.spec.language))

        def do_GET(self) -> None:
            if not self._path_is_valid():
                self._error(404, "Not found", "Use the exact URL printed by local-intake.")
                return
            self._send(200, render_form(state.spec))

        def do_POST(self) -> None:
            if not self._path_is_valid():
                self._error(404, "Not found", "Use the exact URL printed by local-intake.")
                return
            content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/x-www-form-urlencoded":
                self._error(415, "Unsupported request", "Send the browser form as URL-encoded data.")
                return
            try:
                length = int(self.headers.get("Content-Length", ""))
            except (TypeError, ValueError):
                self._error(411, "Length required", "Reload the form and save the answers again.")
                return
            if length < 0 or length > MAX_BODY_BYTES:
                self._error(413, "Answers are too large", "Shorten the answers and save them again.")
                return
            try:
                body = self.rfile.read(length).decode("utf-8", errors="strict")
                payload = urllib.parse.parse_qs(body, keep_blank_values=True, max_num_fields=1000)
                with state.write_lock:
                    if state.accepted.is_set():
                        self._error(409, "Already saved", "This form has already accepted a response.")
                        return
                    answers = normalize_submission(state.spec, payload)
                    pending = read_pending_document(state.document)
                    if pending.spec != state.spec:
                        raise ProtocolError("pending form changed while the server was running")
                    replace_pending_block(state.document, pending, render_log_entry(state.spec, answers))
                    state.accepted.set()
            except (SubmissionError, ProtocolError, UnicodeError, ValueError) as exc:
                self._error(422, "Answers were not saved", str(exc))
                return

            try:
                self._send(
                    200,
                    render_message_page(
                        state.spec.ui.saved_title,
                        state.spec.ui.saved_message,
                        success=True,
                        language=state.spec.language,
                    ),
                )
            finally:
                state.completed.set()

    return IntakeHandler


def create_server(document: Path, spec: FormSpec, token: str) -> IntakeHTTPServer:
    state = ServerState(document=document, spec=spec, token=token)
    return IntakeHTTPServer(("127.0.0.1", 0), make_handler(state), state)


def serve_document(
    document: Path,
    timeout: int,
    announce: Callable[[str], None] = print,
) -> int:
    """フォームを並行HTTPサーバーで一度だけ配信する。"""

    pending = read_pending_document(document)
    token = secrets.token_urlsafe(24)
    server = create_server(document, pending.spec, token)
    host, port = server.server_address
    announce(f"http://{host}:{port}/{token}")
    worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
    worker.start()
    try:
        server.state.completed.wait(timeout)
        return 0 if server.state.accepted.is_set() else 2
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=2)
