# Codex adapter

## Required path

Read the available subagent tool contracts at runtime. Create one recorder with
[the assignment](recorder.md) and concrete script/directory/report paths. Retain its
ID. For a running recorder, use the host's message mechanism; for an idle/completed
recorder, use its continuation/follow-up mechanism. A message-only tool may not
start an idle turn. Wait for a receipt before claiming the report was reflected.
Do not substitute a new user-visible chat for a subagent.

If the host provides no continuation, explicitly replace the recorder from the
saved state. If subagents are disabled, state that prerequisite. Run the loopback
server using the host's long-running command facility; open the printed URL using
its browser facility. On resume confirm both server and recorder rather than
assuming either survived the previous turn or application restart.

## Optional automatic observations

Codex supports `SubagentStart` and `SubagentStop` hooks. Add command handlers to a
reviewed project/user hook configuration only when hook setup is in scope. Each
handler runs the absolute dashboard.py path with `--directory` pointing at this
session's directory and `hook` as the command. Quote both filesystem paths for the
host shell. Merge with existing handlers; never replace unrelated settings.
Register only these two events. The runtime checks their session ID and emits `{}`.

Codex requires review/trust for non-managed hooks. Skill installation alone does
not make them trusted. If unavailable or not trusted, keep the main-agent report
path and label automatic lifecycle observation as unavailable. Never bypass trust
to make a dashboard appear supported. Do not attach recorders to hook events: that
would create a recursive agent-start/update loop.

## Evidence boundary

CLI, desktop and cloud may expose different process and subagent facilities.
Test the exact host and version; do not infer desktop support from CLI results.
No uninterrupted agent lifetime across restarts is promised. The durable record,
not a retained model context, is the recovery source.

Official sources consulted 2026-09-27:
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Hooks](https://learn.chatgpt.com/docs/hooks)
