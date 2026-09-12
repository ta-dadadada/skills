---
name: work-report
description: >-
  Create a concise Markdown report of work for a requested period, or the
  current session when no period is specified. Use when the user asks for
  a work report, today's work summary, or a recap over a date range.
  For explicit periods, inspect available diffs and memory beyond the
  session. For either scope, ask about discovered outside-session changes
  before including them. Write for readers outside the project. Not for resumption handovers,
  PR descriptions, or performing the work being reported.
license: MIT
metadata:
  author: ta-dadadada
---

# Work Report

The executing agent turns evidenced work in a bounded period into a concise,
standalone Markdown report. This is a reporting procedure: completion means
that scope and outside-session changes are resolved, claims match evidence,
and the report makes sense without access to the project or conversation.

## When to use

- Reporting work with no period specified: use the current session.
- Reporting work for an explicit period, including “today” or a date range:
  investigate relevant work beyond the current session.

## When not to use

- Preparing a resumption handover or PR description.
- Implementing, testing, committing, or publishing the reported work.

## Workflow

### 1. Establish scope

- Use the project or work context identified by the request and conversation.
- With no period, cover the session in which the skill was invoked, from its
  start through the reporting request. A context compaction does not start
  a new session. Do not silently expand to the entire day.
- With an explicit period, resolve calendar dates and timezone from available
  context. “Today” means local midnight through the reporting request;
  completed date ranges include their final calendar day. State the resolved
  period. Ask only if an unresolved boundary materially changes inclusion.

**Done when:** the project, session or calendar boundaries, and reporting
cutoff are established before collecting evidence beyond the conversation.

### 2. Gather and attribute evidence

- Start with the session's requests, actions, decisions, and observed results.
  Include material investigation or design work even if it produced no diff.
- For explicit periods, also inspect available project history and diffs
  (committed, staged, unstaged, and relevant untracked work), plus accessible
  memory or prior work notes. Bound retrieval to the project and period.
  Use equivalent sources for non-Git projects.
- Distinguish work in this session, work outside it, and changes of uncertain
  origin. A current diff, file timestamp, or commit date alone does not prove
  when work happened or who performed it; corroborate with available records.
  Separate a change's creation from a later commit or merge.
- If outside-session changes are discovered, or a relevant change cannot be
  attributed to this session, present a short, concrete summary and ask the
  user whether it belongs in the report, resolving timing or attribution as
  needed. This applies even when discovered during a session-only request.
  Reuse an explicit answer already given for those changes; a request for
  “today” alone is not confirmation of discovered changes.
- Keep the established period when asking. For a session-only report, clarify
  the discovered changes' origin and exclude confirmed earlier work unless
  the user explicitly expands the period. Discovery itself does not expand it.
- Continue preparing confirmed material while awaiting the answer. Do not
  include unconfirmed changes or finalize the report as complete. If the user
  asks for a partial report, deliver one with its excluded scope stated.
- When sources are unavailable or incomplete, state that coverage limitation;
  do not claim that no outside-session work occurred. Separate planned,
  attempted, completed, and verified work. Do not rerun tests merely to report
  them; preserve when and against what state existing results were observed.

**Done when:** candidate work has evidence and period attribution, discovered
outside-session changes have a user decision, and coverage gaps are identified.

### 3. Write the Markdown report

- Write in the user's language, with a factual professional tone. Identify
  the project or product in ordinary terms and explain any essential jargon.
- State the period and lead with the outcome. Group by meaningful result,
  explaining what changed and why it matters rather than listing files,
  commands, or the conversation chronology.
- Default to one short overview and 3–6 concise bullets, roughly one screen.
  Use fewer bullets for small amounts of work; omit empty sections. Preserve
  material failures and unfinished work even when compressing.
- Make every item understandable outside the project. Do not use relative
  file links, machine-local absolute paths, editor links, unexplained internal
  nicknames, or “as discussed above.” Describe the component and behavior.
  Optional references must be verified, reader-usable web links; the prose
  must remain understandable without opening them. Omit inaccessible sources
  rather than inventing public URLs or exposing private details.
- Include verification and remaining work only when material. A successful
  check supports only the behavior and version it actually covered.
- Return Markdown in the conversation by default. Save a `.md` file when
  requested, honoring the destination. Reporting does not authorize sending
  the report to other people or publishing it.

Suggested shape; localize headings and omit optional empty sections:

```markdown
# Work report — <project or product>

Period: <current session, or resolved dates and timezone>

<One-sentence outcome and purpose.>

- <Result and its practical significance.>
- <Another material result.>

## Verification and remaining work

<Observed checks, unfinished items, or material coverage limitations.>
```

### 4. Check and deliver

Confirm that each claim is evidenced and in scope, outside-session decisions
are respected, status is accurate, and the Markdown stands alone without
project-local navigation. Remove repetition and low-value detail. Deliver
only the report (and a file link if a saved artifact was requested).

## Red flags

- Treating every dirty file as work performed in this session or today.
- Silently narrowing “today” to the current session because history is harder
  to inspect, or expanding a session-only request to all available history.
- Including discovered outside-session changes without the user's answer.
- Presenting missing history as evidence that no other work occurred.
- Producing a file inventory instead of explaining outcomes to an outside reader.

## Related

- `session-handover` — context for resuming interrupted work.
- `pr-handoff` — review preparation for a finished change.
