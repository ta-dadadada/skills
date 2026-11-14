---
name: hq-dashboard
description: >-
  Ledger CLI and read-only local browser dashboard for an HQ that commands
  parallel host sessions: tasks, sessions, waiting-for-you items (approval,
  decision, review, launch, criteria), artifacts, a task relationship graph,
  and an event log in one SQLite ledger. Each update is one command with a JSON
  receipt; a session's turn-end note is recorded verbatim with `report`. Use
  when the hq-adjutant skill initializes, resumes, serves, or updates its HQ
  ledger, or when the user explicitly asks for the HQ dashboard. Not for one
  session's own progress (session-dashboard), collecting approvals in the
  browser, or planning and verifying the work itself.
license: MIT
compatibility: >-
  Python 3.11+ standard library only (sqlite3, http.server), a writable HQ
  folder, a local browser, and loopback HTTP on 127.0.0.1. No third-party
  packages or network services. Claude Code / Claude Desktop notes are in
  references/claude-desktop.md.
metadata:
  author: ta-dadadada
---

# HQ Dashboard

The ledger is the HQ's state of record; the dashboard is a read-only window on it. Every routine update is **one** CLI call whose input you already hold verbatim. The CLI parses, assigns ids, appends the event, and rewrites `ledger.md`; its receipt proves the dashboard is current. Updating the dashboard never costs a second call, a re-read, or a page check.

The skill's work is complete when the ledger exists, the dashboard URL is live or its failure is reported, every received session note and user answer has an `"ok":true` receipt, and at shutdown the server is stopped with the ledger intact.

## When to use

- The `hq-adjutant` skill activates, resumes, or updates its HQ.
- The user explicitly asks to open, restart, or update the HQ dashboard.

## When not to use

- Tracking one session's own goal and TODOs: `session-dashboard`.
- Collecting approvals or decisions: the page is read-only; answers happen in the adjutant chat.
- Deciding, planning, or verifying the work: that is the adjutant's job; this skill only records.

## CLI

- The CLI is [scripts/hq.py](scripts/hq.py) in this skill's directory. Resolve its absolute path once. Call it with the same fixed prefix every time, `python3 <abs>/hq.py …`, so the user can allowlist that prefix once. Run each call as its own command; do not chain calls with `&&` or `;`.
- HQ folder: `--hq DIR`, else env `HQ_DIR`, else `~/hq`. `--hq` may appear before or after the command.
- Every command prints one line of JSON. `"ok":true` means the change was committed in one transaction. On error the CLI prints `{"ok":false,"error":…}`, exits non-zero, and changes nothing. Fix the cause named in the error and run the command once more.
- Free text (titles, goals, summaries, wait summaries, resolutions) is written in the HQ language. Commands, flags, enum values, and ids stay English.
- Full command, receipt, `apply`, and `report` parsing reference: [references/cli.md](references/cli.md). Read it when you need a command not shown below, or when a receipt's `warnings` are unclear.

## Workflow

React to session notes and user turns only. Never poll the ledger or the page in an LLM loop.

### 1. Initialize or resume

- Run `init --lang <HQ language>`, using the language the user speaks with you, such as `ja`. It never overwrites an existing ledger.
  - `"created":true`: a new ledger was created.
  - `"created":false`: the existing ledger was kept. Never delete it or re-create it. If its `lang` differs from the HQ language, run `lang <code>`.
- When resuming, run `status`. It lists open waits, every task that is not done with its confirmed fields, sessions, edges, and artifacts, and the dashboard URL with `(up)` or `(down: restart serve)`. Rebuild context from it, not from memory. `status --json` returns the same data as JSON.

**Done when:** an `init` receipt exists, and when resuming, `status` has been read.

### 2. Serve the dashboard

- If `status` says the dashboard is `(up)`, give the user its URL and do not start another server.
- Otherwise start `serve [--port N]` as a background long-running process using the host's background execution, as you would a project dev server. Do not use a subagent or a polling loop. Keep the process handle.
  - Without `--port`, `serve` reuses the last recorded port, so open tabs reconnect on their own. The first stdout line is the URL. Open it, or give it to the user.
  - A `cannot listen` error means the port is busy. Run `status`: if it says `(up)`, a server is already running; otherwise pass another `--port`.
- The server binds 127.0.0.1 only and serves `GET /` and `GET /api/state`. Never bind it elsewhere or proxy it.
- The page fits one screen:
  - a header with counts and a progress bar;
  - a progress map with one swimlane per target, laid out in dependency order;
  - a one-line-per-item waiting-on-you column, where each item opens as a drawer;
  - a pinned detail drawer, where ids, branches, URLs, and operations can be copied.

  It polls every 3 seconds and redraws when the ledger revision changes. A pinned panel and any text selected in it are kept.
- After a reboot or a replaced session, a `(down…)` status means: start `serve` again. The ledger needs no repair.

**Done when:** the user has the URL and the server answers, or the launch failure and its error are reported.

### 3. Record each event with one command

| Event | The one command |
|---|---|
| A session's turn-end note arrives | `report --session <id>` with the note piped verbatim through a quoted heredoc (below) |
| A session was started for a task | `launch T<n> --session <id> [--name N] [--cwd C] [--branch B] [--title T]` |
| The user answers a wait item | `wait resolve W<n> --resolution 'user: "<their exact words>"'` |
| A new task is proposed | `task add --title … --target … --deliverable … --done … [--goal] [--authority] [--status queued]` |
| Criteria or a launch need the user | `wait add --kind criteria\|launch --task T<n> --summary …` |
| A task is closed after checking it | `task update T<n> --status done` (or `dropped`); this also resolves the task's open waits and marks its live sessions done |
| Tasks are related | `edge add T<a> depends_on\|spawned_from\|related T<b>` (`A depends_on B`: B blocks A) |
| An artifact the reports missed | `artifact add --task T<n> --kind branch\|pr\|doc\|file\|url\|other --label … --ref …` |
| A session changes state outside a report (for example archived) | `session upsert <id> --task T<n> --state archived` |
| Anything else worth keeping | `note --text … [--task T<n>] [--session <id>]` |
| A rare multi-op correction | `apply` with a JSON array of ops (one transaction, all-or-nothing) |

```
python3 <abs>/hq.py report --session <id> <<'HQ_NOTE'
<note text exactly as received>
HQ_NOTE
```

- `report` finds the `HQ T<n> <state>: … Needs: … Artifacts: …` line anywhere in the note. It sets the session state and summary, opens a wait for each `Needs` item, and resolves the approval, decision, and review waits that earlier reports of that session opened and this note no longer restates; waits you added with `wait add` stay open. It records artifacts and sets the task to `waiting-user`, `blocked`, or `active`. A session's `done` never completes the task, and a report never moves a session to another task; a mismatch comes back as a warning.
- **The receipt is the proof.** After `"ok":true` do not run `status`, fetch the page or `/api/state`, open the browser, run `export`, or restart the server. The server reads SQLite on every request, the page polls, and `ledger.md` was already rewritten. Build your reply from the receipt alone: `waits_opened`, `waits_resolved`, `artifacts_added`, `state`, `parsed`.
- `"parsed":false` means the note had no usable status line. The summary and an event were still recorded. Ask the session for a report line and treat its state as unknown. Read any `warnings` before replying.
- Record first, verify later. A report is recorded as *reported*. Checking claims is the caller's job, done before telling the user something is done or presenting an approval.

**Done when:** every received note and user answer has an `"ok":true` receipt before the reply that mentions it.

### 4. Shut down

- When the HQ is closed or the user asks, stop the `serve` process through its handle. The ledger and `ledger.md` stay in the HQ folder. `init` and `serve` resume them any time.

**Done when:** the server process has exited and `status` still reads the ledger.

## Red flags

| Rationalization | Reality |
|---|---|
| "Check the page to be sure the update landed" | `"ok":true` is the proof; a check doubles the latency and proves nothing more |
| "Parse the note first, then record the fields" | pipe it verbatim to `report`; the CLI parses |
| "Chain the updates with `&&` to save a prompt" | one command per call keeps the allowlisted prefix; use `apply` for a real batch |
| "The ledger looks wrong, re-init it" | `init` never overwrites; fix it with `task update`, `wait resolve`, or `apply` |
| "Restart the server after each update" | the server reads per request; restart only when `status` says down |
| "The subordinate said done, mark the task done" | the task is done only after the caller's check, via `task update` |
| "Let the user click approve on the page" | the page is read-only; answers belong in the chat |

## Related

- `hq-adjutant`: the orchestrator that drives this CLI.
- `hq-subordinate`: defines the report line that `report` parses.
- `session-dashboard`: one session's own progress dashboard, not cross-session.
- Claude Code and Claude Desktop launch, allowlist, and restart notes: [references/claude-desktop.md](references/claude-desktop.md).
