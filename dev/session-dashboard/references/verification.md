# Initial verification record

Observed on 2026-09-27. Fixtures are synthetic work reports, not real completed
project work. No claim is made about uninterrupted model/process lifetime.

## Deterministic evidence

- `python3 -m unittest discover -s dev/session-dashboard/tests -v`: 12 passed
  on Python 3.14.7. Covers inbox persistence, duplicate IDs, stale writes,
  withdrawal, reason requirements, concurrent updates, hook filtering, completion,
  empty content, HTML escaping/export recovery, HTTP isolation and CLI failures.
- `python3 -m unittest discover -s dev/local-intake/tests -v`: 29 passed.
- `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/* meta/*`:
  all 24 packages passed, no warnings.
- `git diff --check`: passed.
- Socket tests initially failed inside the execution sandbox; passed with approved
  loopback access. These failures were environmental, not counted as passing runs.
- New suite and CLI help are included in the existing Python 3.11–3.14 CI matrix.
  Only local Python 3.14.7 has been executed here; remote CI remains unrun.

## Host execution evidence

| Host | Observed | Limits |
| --- | --- | --- |
| Current Codex desktop subagent tools | Recorder read its bounded instructions, applied report 1, ended its turn, resumed via follow-up and applied report 2; state and HTML reached revision 2 | Native hooks and app restart survival not exercised; installed CLI 0.157.1 was not used for this execution |
| Claude Code 2.1.283 | Custom recorder launched; first compound command was denied; with separate allowed commands the same recorder applied reports 1 and 2; persisted state reached revision 2 | Agent reuse is reported by the outer Claude execution; independent observation confirms stored revisions. No native hook setup or server lifetime test in Claude |

Claude's first denial did not change permissions. The retry kept the same narrow
allowlist and used single commands. Recorder guidance now calls for separate calls.
The Claude host was resumed across invocations. The bounded test exercises recorder
execution, not automatic activation of the complete skill in arbitrary projects.

## Browser evidence

Codex in-app browser, loopback server:
- Actual accessibility tree exposed goal, conditions, requests, TODOs, agent reports
  and history; no write controls were present.
- Without page reload the second recorder receipt appeared as revision 2.
- At 360 × 800, columns stacked; measured page scroll width 345px, viewport 360px.
- Real End key scrolled the document; focus remained on BODY.
- Stopping the server displayed a connection error while retaining the last content.
  Restarting the same loopback endpoint restored the live status without reloading.
- File URL navigation was rejected by the browser URL policy. No workaround was
  attempted. Offline HTML is self-contained by code/export tests, but opening it
  directly in a browser remains unverified.
- Actual browser 200% zoom and screen-reader announcements remain unverified. Narrow viewport evidence is not zoom evidence.

## Convergence ledger

| Criterion | State/evidence |
| --- | --- |
| Purpose, phase/slice TODOs, ownership/results | Implemented; schema/render tests and observed browser content |
| Human requests and blocked-work references | Implemented; schema tests and observed read-only request region |
| Agent reports, acceptance, lifecycle separation | Implemented; recorder host checks and fixture hook tests; native hooks unverified |
| Plan changes with reasons | Implemented; rejection/history tests |
| Milestone updates and repeat recorder use | Implemented; durable inbox tests and both host checks |
| Durable record after shutdown | Implemented; restart/export tests; direct offline browser check blocked by browser URL policy |
| Portable skill and distribution | Validator and aligned project links; full-skill activation behavior remains unverified |

An independent fresh-context reviewer inspected the complete diff, all new files,
installation links, CI and metadata against an 18-path hash manifest. No material
actionable finding or scope/design escalation was found. The reviewer consumed
the supplied execution evidence without repeating passing tests; only file identity
and configuration were additionally inspected. Verification limits remained
non-blocking review observations, not claims of runtime success.
This file reports bounded evidence, not universal host compatibility or behavioral
improvement over a previous skill (this is a new skill).

## Usage widget extension

User-requested elapsed/token/model widgets were added after the initial review.
The current dashboard suite passes 16 tests; all 24 package validators and
`git diff --check` also pass. New cases cover unknown versus observed zero,
provenance, invalid counts, escaping, legacy records, running/frozen time, late
reports and resumption. HTTP checks confirm separate elapsed data and stable
content versions when stored state is unchanged.

The in-app browser exposed all three widgets. The existing fixture has no usage
metadata and correctly shows unknown tokens/models. At 360 × 800, widgets stack
and page width remains 345px within a 360px viewport. Numeric/model rendering is
covered by synthetic tests, not a new provider usage collector.

A fresh independent full-diff review found no material issue or scope escalation.
The same reviewer then checked the focused change separating clock text updates
from whole-document replacement, with no regression found. Prior verification
limits still apply. Provider-specific automatic metrics collection is not included.

## Developer density follow-up

The user requested a denser view. CSS now uses 14px body text, tighter headings,
spacing and TODO rows; empty paragraphs are hidden. At 360px the metrics remain
three 97px columns and document scroll width is 345px. At 1100 × 850 the plan and
agent reports are visible together; scroll width is 1085px with no overflow. The
clock visibly advanced without a page reload. Viewport overrides were reset.
An independent targeted CSS/design review found no material issue. This supersedes
the earlier 360px stacked-metric layout observation. Runtime/data logic remains
covered by the 16-test run; no additional suite run was needed for CSS alone.

## Session identity extension

Session start, CWD and dashboard start now have separate labeled header rows.
18 dashboard tests pass, including old-record unknowns, timezone validation,
round-trip storage and escaped paths; all 24 package validators and diff checks
pass. The live browser shows the observed project CWD, unknown session start,
and the earlier dashboard timestamp. At 360px, document width remains 345px.
The real host session start was not available from the supplied context, so it
was not inferred from dashboard activation or the first implementation command.
A fresh independent full-diff review covered all 18 paths and found no material
actionable issue or scope escalation, including optional context compatibility.

## Markdown copy extension

The native copy button exports the currently displayed main document, including
TODO checkboxes and metadata. Controls and the readonly fallback remain outside
the refreshed region. The same script is embedded in saved HTML.

18 Python regression tests and four dependency-free Node tests pass. Run the
latter with `node --test dev/session-dashboard/tests/test_markdown.cjs` (Node 18+).
They check literal Markdown punctuation/entities, TODO states, metadata, latest
content, clipboard success, missing/denied clipboard, snapshot retention, selection
and focus restoration using DOM substitutes. The package validator and diff check
pass. Browser pointer and Enter activation both displayed the success message.
The browser clipboard inspection returned no text, so exact clipboard bytes were
not independently verified there. Denial/unavailable paths were tested with mocks;
direct saved-file browser execution remains subject to the earlier limitation.

Independent review identified incomplete escaping of literal Markdown punctuation
and entities. Escaping now covers CommonMark ASCII punctuation, with regression
coverage for entities, setext-like lines, links, HTML and backslashes.
The reviewer rechecked the fix and reran all four Node tests; no further material
finding remained in the final delta.

## Operations hierarchy redesign

The report-first surface was replaced with a status header, five linked counters,
an expanded attention queue and shared-surface plan/agent rows. Quiet records and
metadata use native disclosures. Counts are based on explicit reported states;
working agents without results are not counted as unverified results. Cancelled
TODOs stay in the denominator and have a separate count.

19 Python tests and six Node tests pass, including count semantics and Markdown
export of collapsed records, summary counters and TODO ownership. Package validation
and whitespace checks pass. In the in-app browser, pointer navigation from the
Attention counter and Enter activation of disclosure/copy controls worked. An actual
semantic report update preserved the expanded session details and focused summary.
At 360 × 800, scroll width was 345px; the plan and agents stacked and counters wrapped.
The viewport override was reset. The sample session is a UI fixture, not a claim of
current host-agent activity. Copy showed success; clipboard-byte, screen-reader,
actual 200% zoom, direct saved-file and print checks retain their prior limitations.

Independent review found a missing text separator between TODO title and owner in
Markdown export. The fix adds an explicit owner label and a regression test. The
schema, storage, authority model and lifecycle inference rules remain unchanged.
