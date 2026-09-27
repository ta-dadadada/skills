# Reports, storage and commands

Examples run from the skill directory. Replace `/path/to/session` with a durable
ignored directory dedicated to this host session. In another directory use the
absolute path to `scripts/dashboard.py`. Python 3.11+ and SQLite are required.

```bash
python3 scripts/dashboard.py --directory /path/to/session init --session-id HOST_SESSION_ID --input assets/example.json
python3 scripts/dashboard.py --directory /path/to/session serve
python3 scripts/dashboard.py --directory /path/to/session status
python3 scripts/dashboard.py --directory /path/to/session submit --input /path/to/report.json
python3 scripts/dashboard.py --directory /path/to/session apply --report milestone-1
python3 scripts/dashboard.py --directory /path/to/session export
```

The example snapshot contains fictional facts. Replace them before actual use.
`serve` prints its loopback URL, chooses an available port, and stays in the foreground;
use the host's supervised background execution and preserve the process handle.
No shell daemonization or separate model API service is required.

## Report envelope

```json
{
  "id": "milestone-1",
  "expected_revision": 0,
  "reason": "Investigation showed that configuration replaces new implementation",
  "snapshot": {}
}
```

Replace `snapshot` with the full schema from [the example](../assets/example.json).
`submit` validates and durably queues the report; `apply` checks the expected
semantic revision and commits the snapshot. Reusing an identical ID/payload is
idempotent; changed payloads with the same ID are rejected. Hook observations
have a separate lifecycle and do not invalidate semantic revisions.

Only the main agent authors snapshots and decides whether outcomes satisfy work.
The recorder applies the submitted report without changing its meaning. These are
agent authority rules, not authentication between processes sharing local files.

| Field | Meaning |
| --- | --- |
| `goal`, `completion_conditions` | Agreed purpose and observable success conditions |
| `current_work` | Last explicitly reported work, not a live activity inference |
| `status` | `active`, `paused`, `completed`, `interrupted` |
| `summary` | Outcomes, remaining work and unverified checks; required on completion |
| `phases` | Ordered `{id, title, todos}`; phases or slices are equally supported |
| TODO | `{id, title, status, owner, result}`; globally unique TODO IDs |
| TODO `status` | `pending`, `in_progress`, `done`, `blocked`, `cancelled` |
| `requests` | `{id, kind, title, detail, status, blocks, resolution}` |
| Request | Kind `decision`/`review`; status `open`/`resolved`; `blocks` references TODO IDs |
| `agents` | `{id, assignment, status, latest_report, result, review, reported_at}` |
| Agent status | `working`, `waiting`, `reported`, `failed`, `stopped` |
| Agent review | `pending`, `accepted`, `changes_requested`; independent of lifecycle |

A done TODO needs a result. A resolved request needs its chat resolution. Completing
a session requires no unfinished TODO or open request. Cancelled work is permitted
when the reason is recorded. A change to the plan's structure, titles, ownership,
purpose, conditions or cancellations requires `reason`; ordinary progress may omit
its text but still supplies the field. Keep timestamps as ISO 8601 text.

## Failure and recovery

- A stale report remains queued. The main agent reads `status`, withdraws the stale
  report with an explanation, and submits a reconciled snapshot using a new ID.
- `withdraw --report ID --reason TEXT` preserves an obsolete queued report and its
  withdrawal in history. It cannot withdraw already applied reports.
- `status` includes pending IDs, latest receive/apply times, semantic revision,
  snapshot and runtime observations. Use it after interruption or lost receipts.
- `session.sqlite3` is canonical, including all submitted snapshots. `state.json`
  and `report.html` are replaceable exports. Back up the whole directory when idle.
- Export failure after a committed operation does not undo the journal. Correct the
  filesystem problem and run `export`; do not invent a new report to retry a render.
- The HTML is regenerated at every update and contains all current content. Opening
  it as a file makes no network requests. The server is read-only and exposes only
  the page and its rendered update; it does not serve the directory or transcripts.
- Keep this local record in an ignored directory; it contains user-supplied work
  details. No public hosting is part of this skill.

## Optional lifecycle hook

Invoke the following with the host's JSON event on stdin:

```bash
python3 scripts/dashboard.py --directory /path/to/session hook
```

Only matching `session_id` and `SubagentStart`/`SubagentStop` events are recorded.
Only agent ID, type, event and receipt time are retained; tool inputs and transcript
paths/content are ignored. Stop means response ended, never accepted work. Missing
hooks leave observation coverage unknown. Agent identity in semantic reports should
use the host's actual ID so observations can be matched by the reader.

## Optional usage widgets

Snapshots may omit `metrics` (old records stay valid) or include:

```json
{
  "models": ["observed-model-name"],
  "total_tokens": 12345,
  "scope": "Main agent only; cumulative through this report",
  "source": "Host usage response",
  "reported_at": "2026-09-27T12:00:00Z"
}
```

These are illustrative values. Populate only from actual host evidence. Use
`total_tokens: null` and `models: []` when unavailable; zero means an observed zero.
Scope must state whether counters cover one turn, the main agent, a particular
subagent or the entire session, and whether child usage is included. Source and
observation time are required. Preserve reported counters rather than summing
parent/child or cached/uncached fields whose overlap is unknown. A configured
default model is not evidence of the model that actually executed. There is no
provider-specific automatic collection, log scraping, or quota lookup. The main
agent forwards available metadata through the existing report path.

Elapsed time is measured from the first journal event, not from the conversation's
start. It advances while active, freezes at a reported pause/interruption/completion,
and on resumption includes the intervening waiting time. Later usage-only reports
do not extend a frozen duration. The saved HTML keeps its export-time reading.

## Session identity

Optional `session_context` is `{ "started_at": null, "cwd": null }`. Supply the
actual session start as an ISO 8601 timestamp with timezone, and its working
directory as observed in the host. Keep unknown fields null; old snapshots remain
valid and display unknown. The header separately shows the journal's dashboard
start timestamp so activating the dashboard later does not misrepresent session
start. CWD means the session workspace, not the recorder's command directory.
No history/log scraping or guessed timestamp is required. Preserve the context
in later reports and update CWD when the session actually changes directories.
