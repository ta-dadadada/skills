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
a recording subagent applies reports and verifies persistence and exports. The
main agent owns server startup, restart, shutdown and browser opening; these are
not recorder tasks. The main agent does not recheck routine record updates.
The browser is read-only. Completion means that current reports are reflected, the durable record
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
For an existing directory, have the recorder inspect `status` and recover assigned
pending reports. Return only the revision cursor and any decision needed; load the
full snapshot in the main agent only if its authoring context was lost or a conflict
requires reconciliation. Restart only the missing display process; never initialize
over existing data. For denied operations, follow [execution permissions](references/execution-permissions.md).

Include optional `session_context` with the actual host session start timestamp
and session working directory when known. Unknown values stay null. Do not use
the recorder/script directory or dashboard launch time as substitutes. Preserve
this context in subsequent snapshots, updating CWD when the session moves.

Prepare an initial snapshot using [the example](assets/example.json) as a schema
example, replacing every illustrative value with actual session facts. The main
agent runs `init`, then launches `serve` directly through the host shell's supported
background/long-running execution, as it would a project development server. It
opens the printed loopback URL and retains the process handle for restart/shutdown.
Do not delegate server launch, browser opening or hosting setup to the recorder.
Use existing execution permissions first; request a concrete permission only after
an observed denial or a known restriction, not a speculative settings change.
A server that cannot stay alive is a limitation to report, not a reason to claim live mode.

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
Preserve the last authored snapshot and the last confirmed revision cursor in
working context. Use them to submit a report with a unique ID; do not read `status`,
`state.json`, HTML, or the browser merely to verify each update. Persist the report
before messaging the recorder with its ID, then continue independent task work.
The recorder owns apply, persistence/export checks, and bounded recovery. Normal
success needs no separate message or narrative: when the host requires a completion
reply, return only `APPLIED <report-id> <revision>`. This receipt updates the cursor
without a main-agent recheck. Surface only failures requiring a decision, permission,
or reconciliation; do not forward state dumps or routine logs.

Serialize semantic submissions: while a receipt is pending, retain later milestone
changes locally and continue the task. Submit the next snapshot after the cursor
arrives; do not guess a revision or poll. A pending receipt is not proof of reflection.
On a stale revision, the recorder returns the conflicting fields and revision;
the main agent resolves meaning and submits a new ID. Never force an old snapshot
over newer work. A genuinely lost cursor may be recovered by the recorder.

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

The recorder runs `export` and checks the final revision, pending reports, and saved
HTML on disk. If an offline browser check is needed, the main agent owns that
check. Reuse unchanged offline-display evidence; do not reopen after each update.
If offline opening is blocked by browser policy, record it as unverified
without an alternate route around that policy. Return one compact final receipt
with revision, saved path and limits. The main agent delivers that path and limits
without rereading the record. Do not delete the session directory. On interruption,
the journal and last export remain; the recorder inspects pending reports on resume
and labels uncertain statuses rather than inventing activity or completion.

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
| Main agent rereads state after every receipt | Recorder owns reflection checks; retain only the cursor |
| Retry an unchanged denied command | Classify the denial and use the supported permission flow |

## Related

- [Protocol and commands](references/protocol.md) — data, persistence and recovery.
- [Recorder instructions](references/recorder.md) — bounded delegation contract.
- [Design contract](references/design.md) — UI and verification criteria.
- `session-goal` supplies purpose; `implementation-loop` owns execution decisions.
- `session-handover` preserves restart context; this dashboard is not its replacement.
