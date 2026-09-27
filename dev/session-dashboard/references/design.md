# Design and acceptance contract

This ops skill maintains one session's read-only dashboard and durable record.
The main agent owns goals, plans, completion and acceptance judgments. The recorder
applies submitted snapshots unchanged; deterministic local code validates versions,
serializes writes and renders HTML. Hooks record lifecycle observations only.
Invocation is explicit; chat remains the response/approval surface.

A session directory contains a canonical SQLite journal, JSON and self-contained
HTML exports. Every applied event is saved. Expected revisions reject stale writes;
report IDs make retries idempotent. Presentation must not change stored semantics.

## Operations hierarchy

Job: a developer opening the dashboard must scan current session state, explicit
TODO completion, human requests, failures/unverified results, and agent work in
seconds. Deliver a working UI using the existing snapshot schema and local export.
Use a compact status header, linked count strip, phase progress rows, an attention
queue, then a shared-surface plan/agent split. Running/blocked work precedes quiet
work within each phase; completed/cancelled items, resolved requests, history and
session identity use native disclosures. Keep session start discoverable in the
header; full timestamps/CWD/IDs and metric provenance remain in secondary details.

Counts are explicit: done / all TODOs, with cancelled counted separately (never
completed); Attention counts open human requests; Failed counts failed agents;
Unverified counts reported/results-bearing agents whose review is pending, plus
unapplied reports. Running counts in-progress TODOs. Pending agents still working
are not unverified results. Blocked TODOs and changes-requested agents also appear
in attention. Counts link to their supporting sections, not invented filters.
Free-text summary remains visible if present, since it can contain unresolved risk.
No timing inference or lifecycle-to-completion inference is added.

Use an off-white shared canvas, charcoal type, muted secondary text, fine rules,
blue running states, amber attention/unverified states and red failure states.
No decorative cards, shadows, blinking or animation. Native details/summary and
anchors support keyboard use; focus and open disclosures survive semantic refresh.
Below 760px the plan and agent sections stack; counts wrap without horizontal
scrolling at 360px. Copy exports the complete record, including collapsed details,
so lower visual priority never removes durable information. Print expands details.

Design review: the five questions each have a direct surface; counters have named
sources and denominators; zero/unknown remains explicit; attention never hides in
a collapsed archive. No new mutation, approval, filter or provider integration.
Static contract passes task/hierarchy/disclosure/recovery/action-scope checks.
Runtime keyboard, refresh preservation, copy, narrow layout and contrast remain
implementation checks; screen-reader and actual 200% zoom require separate evidence.

## Secondary information and export

Session start, CWD and dashboard start remain separate. Unknown values stay explicit;
never infer session start from dashboard creation. Elapsed time is wall time since
dashboard creation, includes waiting, freezes while paused/interrupted/completed,
and includes the intervening interval upon resumption. Saved HTML uses export time.
Usage totals/models are optional, with source/scope/observation timestamp; missing
values are not zero and overlapping counts are not summed.

A native Markdown-copy button announces success. Clipboard denial/unavailability
reveals a labeled readonly textarea, focuses/selects the click-time snapshot and
provides Close returning focus to the button. Controls stay outside the refreshed
main region. Copy includes collapsed content and escapes Markdown punctuation.
The same code is embedded in saved HTML and does not require the server.

Live refresh retains the last view on connection failure, visibly marks disconnection
and reconnects automatically. Displayed states are last reports, never proof of
liveness. Saved HTML identifies itself as a saved record and makes no requests.
Empty collections explicitly report absence of information, not inferred success.

## Acceptance

- Five operational questions have directly scannable surfaces, linked to detail.
- Counts agree with reported records; cancelled work is not completed work.
- Human requests, blocked work, failures, revisions requested and unverified
  results remain expanded even when the session is marked completed.
- Phase and owner identity, results, resolution reasons and history remain accessible.
- Working agents are distinct from reported results and accepted results.
- Desktop/narrow keyboard and pointer paths work; refresh preserves disclosure,
  focus, scroll and manual-copy context; offline exports retain all content.
- Package validation and runtime tests pass. Browser/AT/print claims are limited
  to executed checks recorded in verification.md.
