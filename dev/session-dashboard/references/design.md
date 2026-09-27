# Design and acceptance contract

This ops skill lets the main agent and a recording subagent maintain one session's
read-only dashboard. Success means that the agreed goal, phase/slice TODOs,
human requests, agent observations, and reasons for plan changes are visible and
remain readable after shutdown. Invocation is explicit. No approval UI, autonomous
planning, or cross-session aggregation is included.

## Responsibility and storage

The main agent owns the semantic snapshot. It submits a versioned report before
messaging the recorder, so a lost message cannot lose the report. The recorder
applies the submitted report unchanged and returns its receipt. A deterministic
local runtime validates reports, serializes writes, preserves history, and renders
HTML. Hooks may record lifecycle observations but never complete a TODO.

A session directory contains a SQLite journal (canonical), a JSON export, and a
self-contained HTML export. Use a durable, project-local ignored directory, not
an OS temporary directory. Saving happens at every event, not just shutdown.
An optimistic revision rejects stale semantic reports. Report IDs make retries
idempotent. Runtime lifecycle updates do not advance the semantic revision.

## Screen contract

Entry is the loopback URL during work or the saved HTML after shutdown. The reader
sees purpose and completion conditions, human requests, plan, agent reports, and
history in that order. Human requests name blocked TODOs separately from optional
reviews. Completed work keeps its result. Empty sections explain the absence of
reported information. There is no inferred percentage or automatic completion.

Use a light neutral background, dark ink, restrained teal emphasis, and amber for
requests. Status always has words. A wide layout pairs the plan with agent reports;
below 600px these stack in reading order. Long text wraps at 360px and 200% zoom.
No inputs, dialogs, tabs, sorting, or custom keyboard controls are needed. Native
heading/list semantics and ordinary browser scrolling provide access. Refresh
preserves scroll and focus; a persistent status region announces connection errors
and recovery without announcing the entire document. A failed refresh retains the
last content and states that it may be stale. Offline HTML explicitly says it is
a saved record and performs no network requests.

## Acceptance and verification

| Criterion (source: agreed conversation) | Evidence |
| --- | --- |
| Purpose, conditions, phase/slice TODOs, ownership and results | Schema/render tests and browser inspection |
| Pending human decisions/reviews with blocked TODOs; chat replies | Schema tests and read-only UI inspection |
| Agent assignment, reports, review state, lifecycle observations | Report and hook tests; host smoke checks |
| Reasons survive plan additions/removals/reordering | Revision and history tests |
| Updates at milestones; recorder handles repeated reports | Durable inbox/retry tests and host smoke checks |
| Readable record after shutdown and interruptions | Export, restart, offline browser and failure tests |
| Portable skill with Codex/Claude Code instructions | Validator, installation links, bounded execution checks |

## Design review

Static walkthrough: the four user questions have dedicated sections; requests
precede work details; agent lifecycle is separate from accepted results. Empty,
live, disconnected and offline states have explicit text. No mutation controls
or focus-changing refresh are specified. The UI contract is coherent; runtime
browser checks, actual zoom and assistive technology remain to be verified.

## Usage widgets (requested extension)

Three read-only widgets follow the purpose: elapsed time since dashboard
initialization (including waiting), reported token total, and observed models.
Elapsed time advances during active viewing and freezes while paused/interrupted
or completed. Resuming includes the intervening wall time; this is not CPU time
or the duration before dashboard activation. Saved HTML shows export-time values.
Token/model values are optional and show unknown rather than zero when absent.
Every supplied metric includes its scope, source and observation time. Never sum
main-agent and child usage unless the source establishes non-overlapping totals.
Keep three compact columns down to 360px; stack metrics at 320px or narrower. Text and values wrap.

Design review: these widgets add no input or focus behavior. Scope and provenance
prevent mistaking partial usage for a session total. Tests cover legacy snapshots,
unknown versus zero, validation, frozen/restarted time and safe rendering. Browser
checks cover the three widgets and narrow layout. Provider-specific automatic
usage collection remains outside this extension.

## Developer density adjustment

The user requested a denser developer-facing view. Use 14px body text with 1.45
line height, compact headings and 6px TODO row padding. Remove empty paragraphs,
keep metrics in three columns above 320px, and use the wider available viewport.
Retain explicit status text, provenance and a single-column narrow-screen layout.
Review: no controls or semantic data changed; check desktop/narrow reading and
long-value wrapping at runtime.

## Session identity follow-up

Display session start, session CWD and dashboard start separately beneath the
heading in compact labeled rows. Unknown session start/CWD remain explicit.
Timestamp offsets remain visible; long directory names wrap without overflow.
Old records must remain readable. Optional context comes from the main agent's
host observations; dashboard initialization must not masquerade as session start.
Design review: no new actions; verify parsing, unknowns, escaping and narrow layout.
