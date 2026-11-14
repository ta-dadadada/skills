# Claude Code and Claude Desktop

Both hosts run commands through the Bash tool. These notes map the skill's portable steps to those tools. If a tool's own description contradicts this file, follow the tool and report the difference.

## Fixed command prefix and allowlisting

- Resolve the script once: `<skill dir>/scripts/hq.py`, followed through any symlink to the canonical directory. Call it as `python3 /abs/path/to/hq-dashboard/scripts/hq.py …` every time, never through `cd` or a relative path.
- Once per HQ, tell the user they can allowlist the prefix as a Bash permission rule, so updates run without prompts. For example, `Bash(python3 /abs/path/to/hq-dashboard/scripts/hq.py:*)` in the project or user settings. Do not edit settings yourself unless the user asks.
- One call per Bash invocation. `&&`, `;`, and pipes from another command can fall outside a prefix rule. A heredoc (`<<'HQ_NOTE'`) feeds stdin without changing the command prefix, so `report` stays covered.
- Use a quoted heredoc delimiter (`'HQ_NOTE'`) so the shell does not expand `$`, backticks, or `\` in the note.

## Running the server

- Start `serve` with the Bash tool's background execution option (`run_in_background: true`), as you would a dev server: `python3 /abs/…/hq.py serve --port 8765`. Keep the returned task id; it is the process handle.
- The URL is the first line of the task's output file. Read only that line, once. On Claude Desktop, open it in the built-in browser pane if available; otherwise give the URL to the user.
- Do not delegate the launch to a subagent, and do not watch the output in a loop. Notifications about the background task finishing are informational. A finish you did not cause means the server stopped, so start it again.
- Stop it by stopping that background task, which sends SIGTERM; `serve` exits 0. Without the handle, stop the process listening on the recorded port.

## Restart after reboot or a new session

- Background processes do not survive the end of the session that started them, an app restart, or a reboot. On resume, `status` reports `dashboard … (down: restart serve)`. Then run `serve` again in the background. Without `--port`, it reuses the recorded port, so a browser tab left open reconnects on its own.
- `(up)` means a server from an earlier session is still answering. Reuse it; you have no handle for it, so stop it by port if needed.

## Sandbox and permissions

- Binding 127.0.0.1 and writing the HQ folder are the only resource needs. If the sandbox refuses the bind or the write, the error names it. Request that exact permission through the host's permission flow. Never change the bind address to get around a restriction.
- A refused server does not block recording: mutating commands work without a running server. Report the display limitation once.
