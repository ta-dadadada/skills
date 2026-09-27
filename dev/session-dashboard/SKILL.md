---
name: session-dashboard
description: >-
  Maintain a browser dashboard and durable work record for one session: goal,
  phase or slice TODOs, progress, human decisions and reviews, subagent reports,
  and reasons for plan changes. Use only when the user explicitly requests a
  session dashboard, including updates or resumption of an activated dashboard.
  Assign a recording subagent and update at milestones. Replies remain in chat.
  Not for autonomous planning, browser approvals, or cross-session aggregation.
license: MIT
compatibility: >-
  Python 3.11+ with SQLite, a local browser and loopback HTTP access. Codex or
  Claude Code must expose subagent creation and continuation. Optional lifecycle
  hooks need host-specific configuration. The script requires a durable writable
  session directory. No third-party Python packages or network service required.
metadata:
  author: ta-dadadada
---

# Session Dashboard

Keep an explicitly requested session dashboard current while the main agent
continues its work. The main agent owns purpose, plans and completion judgments;
a recording subagent applies reports and maintains the display. The browser is
read-only. Completion means that current reports are reflected, the durable record
is readable, and remaining work or verification limits are explicit. Activating
this skill does not replace the underlying task or its completion criteria.

## When to use

- The user requests a browser progress dashboard for this session.
- Update or resume that explicitly activated dashboard across turns.

## When not to use

- No dashboard was requested; do not activate for ordinary progress commentary.
- Planning the work itself, approving changes in the browser, or aggregating sessions.

## Workflow

### 1. Activate or resume

Reuse the agreed goal and plan. If absent, show unknown work as an empty plan;
do not invent agreement. Choose a durable ignored session directory in the user's
project, separate from other sessions. Record its absolute path, host session ID,
recorder ID and server handle in the working context and any requested handover.
Resolve this package's scripts from its canonical directory; never assume the
consumer's working directory is the skill directory.

Read [the protocol](references/protocol.md), then the applicable environment guide:
[Codex](references/codex.md) or [Claude Code](references/claude-code.md). Follow the
host's actual available tools rather than assuming tool names from another host.
For an existing directory, inspect `status`, recover pending reports and restart
only the missing display process; never initialize over existing data.

Include optional `session_context` with the actual host session start timestamp
and session working directory when known. Unknown values stay null. Do not use
the recorder/script directory or dashboard launch time as substitutes. Preserve
this context in subsequent snapshots, updating CWD when the session moves.

Prepare an initial snapshot using [the example](assets/example.json) as a schema
example, replacing every illustrative value with actual session facts. Run `init`,
start `serve` under the host's supported process supervisor and open its printed
loopback URL. Keep the handle so only this server can be stopped later. A server
that cannot stay alive is a limitation to report, not a reason to claim live mode.

### 2. Assign the recorder

Create one recording subagent using [the recorder instructions](references/recorder.md).
Supply the absolute script and session paths and the authoritative scope. Retain its
ID and resume/message it at milestones; do not keep an LLM in a polling loop.
Assign it recording work only. It may finish its current turn and be called again.
Register its assignment in the main agent's next snapshot. If continuation is
unavailable, create a replacement with the saved state and report that replacement.
If subagents are unavailable, disclose the limitation; do not silently describe
main-agent updates as a resident subagent.

**Done when:** the page opens, durable storage exists, and the recorder has applied
an actual submitted report and returned its revision. An unavailable component
remains explicitly unverified while independent task work continues.

### 3. Report milestones

The main agent submits snapshots for TODO starts/completions, plan changes,
requests/resolutions, agent launches/reports and meaningful long-work updates.
Read the current revision; preserve unaffected information and submit a new report
with a unique ID. Persist the report before messaging the recorder with its ID.
The recorder runs `apply` and returns the revision or exact failure. A pending
receipt is not proof of reflection. Reconcile conflicts against current state;
never force old snapshots over newer work.

Keep phases or slices with their TODOs, owner, status and result. Include reasons
for changed goals, completion conditions, plan structure, assignments or cancelled
work. Keep decision/review requests with context, blocked TODO IDs and resolutions
from chat. Distinguish an agent's report from the main agent's acceptance of it.
Update reported timestamps from actual observations. When the host exposes usage,
include optional metrics with observed model names, token totals, scope, source and
time as described in the protocol. Preserve unknowns; do not estimate tokens from
text, infer the actual model from a configured default, sum overlapping counters,
or substitute account quota percentages. The elapsed widget starts at dashboard
activation and includes waiting time; it is not the full pre-activation session time. Retain completed work and
resolved requests unless a recorded plan change explains their removal.

Optional hooks record only observed agent lifecycle. Filter by the active session
ID, avoid transcript scraping, and exclude recorder-generated events from any
feedback loop. Lifecycle observations never infer TODO completion or semantic
progress. Without hooks, the main agent reports the observed agent states itself;
identify the source and do not promise automatic discovery.

### 4. Preserve and finish

At a conversational pause keep the record active or paused, with unresolved work
visible. A turn ending is not proof the user's task is complete. At actual task
completion, submit the final snapshot with summary, outcomes, remaining work and
unverified checks. Use interrupted/paused when work remains. Apply pending intended
reports before stopping the recorder and this session's server. Withdraw obsolete
pending reports explicitly through the main agent, preserving the reason.

Run `export` and verify `report.html` opens without the server. Deliver the saved
record path and unresolved items. Do not delete the session directory. On abrupt
interruption, the journal and last export remain; on resume inspect pending reports
and label uncertain statuses rather than inventing activity or completion.

**Done when:** the final intended revision is exported, obsolete reports are
accounted for, the saved HTML is readable offline, and the user has its location.

## Red flags

| Mistake | Correction |
| --- | --- |
| Agent stopped, so the TODO is done | Only the main agent accepts results |
| Recording subagent must keep thinking | Resume it when there is a report |
| A tool call implies progress | Record explicit milestones and observations |
| Last message means session complete | Preserve pauses and unfinished work |
| Save only when shutting down | Save every report and reflected state |
| Reuse a report ID with altered content | Reconcile and submit a new ID |

## Related

- [Protocol and commands](references/protocol.md) — data, persistence and recovery.
- [Recorder instructions](references/recorder.md) — bounded delegation contract.
- [Design contract](references/design.md) — UI and verification criteria.
- `session-goal` supplies purpose; `implementation-loop` owns execution decisions.
- `session-handover` preserves restart context; this dashboard is not its replacement.
