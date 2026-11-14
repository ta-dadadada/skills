# hq.py reference

Call it as `python3 <abs>/hq.py [--hq DIR] <command> …`. HQ folder: `--hq` > `HQ_DIR` > `~/hq`. Output is one line of JSON per call, except `status` without `--json` and `serve`. Errors return `{"ok":false,"error":"…"}` with a non-zero exit, and nothing is changed. Usage errors also return JSON and exit 2.

## Data model

| Record | Id | Fields and enums |
|---|---|---|
| task | `T1, T2, …` | `title, goal, target, deliverable, done_criteria` (flag `--done`), `authority`; `status` ∈ `queued, active, waiting-user, blocked, done, dropped` |
| session | host id | `task_id` (may be null for an unknown session reported without a task), `name, title, cwd, branch`, `state` ∈ `starting, working, idle, waiting-user, blocked, done, archived`, `summary` (≤ 400 chars), `reported_at` |
| edge | `(from, kind, to)` | `kind` ∈ `depends_on, spawned_from, related`. `A depends_on B`: B blocks A. Same-target grouping is derived, not stored |
| wait | `W1, …` | `kind` ∈ `approval, decision, review, launch, criteria`; optional `task_id`, `session_id`; `summary`; `status` ∈ `open, resolved`; `resolution`; `source` ∈ `report, manual` (who opened it; ledgers from schema 1 are migrated on the next write: waits with a `wait.add` event become `manual`, other approval/decision/review waits with a session become `report`) |
| artifact | `A1, …` | `task_id`, `kind` ∈ `branch, pr, doc, file, url, other`, `label`, `ref`; deduplicated by `ref` per task |
| event | integer | `ts, type, task_id, session_id, text`; one per mutating command |

Ids are never reused. Times are ISO-8601 UTC. Ledger metadata holds `lang`, `revision` (incremented once per mutating command), and the last dashboard URL.

## Commands and receipts

| Command | Receipt |
|---|---|
| `init [--lang CODE]` | `{"ok":true,"created":true\|false,"hq":…,"lang":…}`. It never overwrites. If an existing ledger's lang differs, the receipt adds a `note` |
| `lang CODE` | `{"ok":true,"lang":"ja"}` |
| `serve [--port N]` | Prints the URL line first, then runs in the foreground until stopped. A busy port returns an `ok:false` error. Without `--port`, it reuses the last port, else picks a free one |
| `status [--json]` | Text: dashboard URL with `(up)` or `(down…)`, counts, open waits, every task that is not done with its confirmed fields, edges, sessions, and artifacts, then finished task ids. `--json` returns the same data with `server_alive` |
| `export` | `{"ok":true,"path":…/ledger.md}`. Rarely needed, since every mutation rewrites it |
| `task add --title --target --deliverable --done [--goal] [--authority] [--status]` | `{"ok":true,"id":"T3","status":"queued"}` |
| `task update ID [fields…] [--status]` | `{"ok":true,"id":"T3","status":…,"changed":[…]}`. With `--status done` or `dropped`, the same transaction resolves every open wait of the task (`task closed: done` / `task closed: dropped`) and sets its `starting`/`working`/`idle`/`waiting-user`/`blocked` sessions to `done` (archived ones stay); the receipt adds `waits_resolved` and `sessions_closed` |
| `session upsert SID --task ID [--name --title --cwd --branch --state --summary]` | `{"ok":true,"id":SID,"task":…,"state":…,"created":bool}`. A new session defaults to `starting`; `--summary` also sets `reported_at` |
| `edge add FROM KIND TO` | `{"ok":true,"edge":[…],"created":bool}`. A duplicate is a no-op |
| `edge remove FROM KIND TO` | `{"ok":true,"edge":[…],"removed":true}`. A missing edge is an error |
| `wait add --kind K --summary S [--task] [--session]` | `{"ok":true,"id":"W4","kind":…,"created":bool}`. An identical open wait is returned, not duplicated |
| `wait resolve WID [--resolution R]` | `{"ok":true,"id":"W4","status":"resolved","kind":…,"task":…,"session":…}`. An already resolved wait returns `"already_resolved":true` and its earlier `resolution`, unchanged |
| `artifact add --task --kind --label --ref` | `{"ok":true,"id":"A2","created":bool}` |
| `note --text T [--task] [--session]` | `{"ok":true,"event":N}` |
| `launch ID --session SID [--name --cwd --branch --title]` | `{"ok":true,"task":…,"session":…,"state":"starting","task_status":…,"created":bool,"waits_resolved":[…]}`. It resolves the task's open `criteria` and `launch` waits with `launched as SID`; `task_status` is `waiting-user` if approval/decision/review waits stay open, else `active`. A `done` or `dropped` task is refused: set it back with `task update ID --status queued` first |
| `report --session SID [--task ID] [--text T]` | See below |
| `apply [--file F]` | `{"ok":true,"results":[…]}` or one error naming `op N (name)`. All ops run in one transaction |

Unknown task, session, or wait ids are errors. The exceptions: `session upsert` creates the session, and `report` creates an unknown session.

## `report`

The text comes from `--text` or stdin. Pipe the note verbatim. Parsing:

1. Before parsing, full-width spaces and colons (`　`, `：`) are normalized. The first `HQ T<n> <state>:` anywhere in the text is the status line. `<state>` ∈ `working, waiting-user, blocked, done`.
2. `Needs:` and `Artifacts:` (exact capitalisation) are found on the status line, whatever punctuation precedes them (`.`, `。`, `；`, or none), or anywhere after it, blank lines included, up to the next `HQ T<n>` status line. Each value runs to the end of its line; a keyword alone on its line takes the following non-blank lines (a list). Trailing `. 。 ; ；` are stripped.
3. Task, in precedence order: explicit `--task`, then the session's existing task, then the line's `T<n>`. A report never moves a session silently: if the line names another task (or an unknown one), the report is applied to the session's task with a warning naming both ids; `--task` moves it, also with a warning. With no `--task`, no mapping, and an unknown line task, the report counts as unparsed, with a warning.
4. Session: `state` and `reported_at` are set, and `summary` gets the first 400 characters of the text. An unknown session is created and linked to the task.
5. Needs:
   - `none`: resolves the session's open approval, decision, and review waits that a report opened.
   - `approval|decision|review: X`: items may be separated by `;`, `；`, `,`, `、`, or a line break before the next kind, and may carry a list marker (`1)`, `1.`, `(a)`, `-`, `*`, `•`, `・`, `①`). Each opens a wait of that kind with `source` `report`, unless an identical open one exists (same kind, same text after whitespace normalization), whatever its source. The session's other open approval, decision, and review waits that a report opened are resolved with `superseded by report`.
   - Waits recorded with `wait add` (`source` `manual`) are never resolved by a report; resolve them with `wait resolve` or by closing the task.
   - A missing `Needs:` segment, or text that is neither `none` nor a known kind, leaves waits unchanged and adds a warning.
   - `launch` and `criteria` waits are never touched by `report`.
6. Artifacts: items are separated by `, ` or `; ` (punctuation followed by whitespace), by `、`, `，`, `；`, or by line breaks, so a URL containing commas stays one item. List markers before an item are ignored. A leading `PR`, or a URL containing `/pull/`, makes a `pr`. Then `branch X` makes a `branch` (the ref is X's first word), `doc PATH` makes a `doc`, another `http(s)` URL makes a `url`, and anything else is `other`. `none` adds nothing. Items are deduplicated by ref per task.
7. Task status follows these rules. A task that is `done` or `dropped` is never changed. Otherwise the task becomes:
   - `waiting-user` if it has any open approval, decision, or review wait, or if Needs was not understood and the state is `waiting-user`;
   - else `blocked` if the state is `blocked`;
   - else `active`.

   A session's `done` never completes the task.
8. Text with no status line is not an error. It records the summary and an event, leaves the session state unchanged (a new session gets `idle`), and returns `"parsed":false`. Only a missing session id, empty text, or an unknown `--task` is an error.

Receipt:

```json
{"ok":true,"task":"T3","session":"local_x","state":"waiting-user","parsed":true,
 "waits_opened":[{"id":"W4","kind":"approval","summary":"git push origin feat/x"}],
 "waits_resolved":["W2"],"artifacts_added":["A2"]}
```

The receipt adds `"warnings":[…]` only when something needs attention: a created session, a missing or unclear `Needs:`, an unknown task in the line, artifacts without a task, or a `ledger.md` write failure.

## `apply`

A JSON array of objects, from `--file` or stdin. Each object has `"op"` plus keys that mirror the flags in snake_case. Unknown keys, missing keys, and non-string values are errors. Later ops may refer to ids that earlier ops created.

| op | required | optional |
|---|---|---|
| `task.add` | `title, target, deliverable, done` | `goal, authority, status` |
| `task.update` | `id` | `title, goal, target, deliverable, done, authority, status` |
| `session.upsert` | `id, task` | `name, title, cwd, branch, state, summary` |
| `edge.add`, `edge.remove` | `from, kind, to` | |
| `wait.add` | `kind, summary` | `task, session` |
| `wait.resolve` | `id` | `resolution` |
| `artifact.add` | `task, kind, label, ref` | |
| `note` | `text` | `task, session` |
| `report` | `session, text` | `task` |
| `launch` | `id, session` | `name, cwd, branch, title` |
| `lang` | `code` | |

## `ledger.md`

It is rewritten atomically after every mutating transaction commits, from a committed snapshot; writers are serialized with `.ledger.md.lock`, and the first line `<!-- hq-ledger revision N -->` keeps an older snapshot from replacing a newer file (`export` always rewrites). Sections, in order:

1. Header: folder, language, revision, dashboard URL.
2. Waiting for you: open waits.
3. Tasks not done: each with target, goal, deliverable, done when, authority, edges, sessions, and artifacts.
4. Finished tasks: the latest 50.
5. Recent events: the latest 30.

Treat it as read-only. The SQLite file is the state of record.

## HTTP (read-only, 127.0.0.1 only)

- `GET /`: the dashboard page, with the current state embedded so it renders before the first poll.
- `GET /api/state[?since=REV]`: the full snapshot: `revision, lang, generated_at, server_url, tasks, sessions, edges`, `waits` (open, plus the latest 50 resolved), `artifacts`, and `events` (the latest 200) with `events_total`. When `since` equals the current revision, it returns `{"revision":N,"unchanged":true}`.
- Other paths return 404. Other methods return 405 with `Allow: GET`. A `Host` other than `127.0.0.1:<port>` or `localhost:<port>` returns 403.

The page has four parts. Visible words are data; explanations are in `title` and `aria-label` only, in `en` and `ja`.

- **Header bar:** icon chips for active sessions out of 8, waiting on you, blocked, and done; a progress bar segmented by task status; the last-update time; a connection dot; and a history toggle.
- **Progress map:** one swimlane per target; columns follow `depends_on` and `spawned_from` order. Each task node shows its lifecycle stepper, its latest session, the time since the last report (warning after 30 minutes without a report while `starting` or `working`), a PR chip, and an open-wait badge. Hovering shows a preview tooltip. Clicking or pressing Enter pins the detail panel.
- **Waiting-on-you column:** one 24 px line per item.
  - Each item has a chevron and opens as a sliding drawer with an × button. At most two are open at once.
  - The drawer repeats the summary only when the line truncates it. It shows the W and T ids and the session id with copy icons.
- **Detail panel:** a sliding drawer under the waits with an × button. It holds copyable ids, branches, cwd, URLs, wait operations, and summaries. It stays open until × or Esc closes it, or another node is clicked. Polling never rebuilds it while its data is unchanged, and defers a rebuild while text is selected inside it.

- **Side column toggle:** an icon button collapses the whole side column (waits and detail) to a thin rail that keeps the waiting count, so the map takes the full width. Clicking the rail, or pinning a node's detail, expands it again. The collapsed state is remembered per viewer in `localStorage`; the page works without it. Below 900 px the toggle collapses the section vertically.

Esc closes, in order: the history drawer, the focused wait drawer, the detail panel, and then the last-opened wait drawer. Esc never collapses or expands the side column; while it is collapsed, Esc only closes the history drawer. Slide transitions are disabled under `prefers-reduced-motion`.
