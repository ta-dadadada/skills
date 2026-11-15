# Codex desktop execution

Use the current host shell tool to execute the portable CLI. The Codex app
thread tools collect session reports; the dashboard server only displays the
ledger and does not subscribe to chats or grant permissions.

## Commands and server lifetime

- Resolve `scripts/hq.py` once through the installed skill's symlink. Run one
  command per shell call with the fixed prefix `python3 /abs/path/hq.py` and an
  explicit `--hq` outside the default folder. For stdin reports, use a quoted
  heredoc delimiter absent from the report; preserve its text literally.
- With `exec_command`, start `serve` with a short `yield_time_ms` and keep the
  returned `session_id` if it remains running. Read the first output line for
  its URL. Do not assume shell `&` provides a durable process handle. If this
  host exposes another background facility, follow its documented lifetime.
- Stop an owned interactive process through that handle (for example Ctrl-C
  through `write_stdin` when using a PTY). Verify that it exits. A session id is
  an execution handle, not a Codex chat id. Never stop an unrelated process by
  guessing its port or pid.
- On resume, run `status` once. Reuse a responding server; otherwise start it
  again. Long-running execution may end with the chat or app; persistence is
  not guaranteed. A live server does not imply that the adjutant is monitoring.

## Permissions and reporting

The host controls writable folders and loopback binding. Use a user-selected
writable HQ folder and request only the exact denied resource through the
host's native flow when required. Never change the bind address, edit host
permission settings, or bypass a denial. An approval in another chat cannot
satisfy this chat's tool prompt. Prefix suggestions in the Claude overlay do
not describe Codex settings and must not be copied as Codex configuration.

A denied display launch does not prevent recording when the HQ folder remains
writable. Give the limitation and retain the ledger. Successful mutation
receipts establish that data was committed; they do not establish server
liveness, host permissions, or subordinate completion. At startup, verify the
server once; do not fetch the page after every event.

For chat discovery, authorization, pending launch ids, bounded collection, and
cursor persistence, use
[the adjutant Codex overlay](../../hq-adjutant/references/codex-desktop.md).
