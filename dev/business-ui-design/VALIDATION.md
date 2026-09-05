# Validation record

## Responsibility split — 2026-09-05

Updated under `shiranui-hanten` after splitting common UI design from implementation.

- Job/layer: a UI agent chooses operational information structure and passes it
  through frontend design and requested implementation; domain layer.
- Completion: the requested artifact and applicable business acceptance evidence
  return through the chain, with unknown rules and unfinished scope explicit.
- Invocation: model-invoked. Business design/reshaping and implementation enter
  Steps 1–2; Step 3 passes delivery intent through the design companion. Step 4
  reconciles domain cases using returned evidence rather than rerunning common checks.
- Ownership: business archetypes/record operations stay here. The frontend design
  companion owns common contracts, and the implementation companion owns code and
  runtime checks. Fragile references to companion step numbers were removed.
- Findings/pruning: prior frequency intake lacked a downstream decision. Step 2
  now evaluates batch, inline, views, or accelerators against observed repetition
  and task scope, without making every efficiency feature mandatory.

## Representative execution

Run after frontend design and implementation verification with a fresh
`gpt-5.6-terra` / `medium` executor. Task: implement a three-ticket operations
queue; compare ID/priority/age/owner, assign different owners one record at a time,
sort age and filter owner over the fully loaded collection, and recover failed
writes while retaining drafts. Bulk operations, saved views, clipboard, shortcuts,
and a detail page were outside scope.

Observed artifacts and executor-reported sequence: read business → frontend
design → frontend implementation and their references; draft design and code,
persisting them in one operation; exercise the local running fixture;
correct defects and recheck; update evidence. One record preserves the domain
choices through implementation. Repetition justified row-local assignment rather
than expanding scope to every efficiency feature. The parent inspected the
record, code, and reported runtime observations.

Runtime evidence covers pointer assignment, key-based assignment from a directly
focused field, failed-write retention/retry, sort/filter over the full fixture,
loading/empty/load-error recovery, and 320×800 horizontal comparison. The executor
corrected a scroll-region accessibility issue, focus loss on table remount, and
hidden assignment labels, then reran affected checks. `node --check app.js` passed. The final reported axe run
had 38 passes, no violations, and no incomplete results; this is automated-rule
coverage only, not accessibility conformance or screen-reader evidence.

The shared record initially mixed ARIA/CSS decisions into the design contract.
The handoff guidance now separates outcome requirements from implementation notes,
and the executor moved concrete mappings into those notes without redesigning
the UI. The core business structure remained unchanged. The recorded operation sequence
also showed that the design and code were persisted together, so this run does
not prove a separate pre-code design inspection. The design workflow now names
that ordering explicitly. A fresh Terra/medium quick-view change trial checked
the boundary again: the feature worked, but its reported sequence still loaded
all companions and wrote code before the final contract record. That trial is
functional evidence only and is not a passing design-before-code workflow test.
A separate fresh `gpt-5.6-sol` / `medium` read-only queue trial produced DESIGN.md,
read it in a separate operation to review the contract, then wrote the HTML/CSS/JS.
The parent inspected that design artifact and the reported operation sequence.
This supplies a successful pre-code inspection trajectory for a new design.
Reading implementation references early is permitted; the substantive boundary
is reviewed design before code, not the order in which reference files are loaded.
Sol then exercised pointer inspection/return, Tab/Enter inspection/return, empty
and error recovery, and 390×844 sequential detail with keyboard horizontal
scrolling of the comparison table. The reported active elements returned to the
originating record controls. JavaScript syntax checks passed. This trial carries
both a successful design-before-code sequence and observed implementation behavior.

Limits: the keyboard assignment initially used automation to focus the starting
field, so that run alone does not establish page-entry Tab reachability. Actual
200% browser zoom and assistive-technology announcements are unverified. The
Sol run additionally exercised normal Tab traversal for its own two-record task;
it does not retroactively cover the earlier fixture. The three-record fixture provides no evidence for remote paging, real permissions,
real backend failures, grid navigation, or concurrent multi-record writes.

## Earlier evidence and limits

Earlier design-only order-queue trials established the need to preserve comparison
on narrow screens and distinguish real post-artifact review from planned checks.
Those trials did not exercise this three-skill implementation chain and supply no
runtime or accessibility-compliance evidence for it.

## Mechanical and placement checks

- `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/business-ui-design` passed.
- The full `dev/* meta/*` validator passed for all 18 packages.
- `git diff --check` and explicit whitespace checks covering new files passed.
- Names match canonical directories. Both `.agents/skills/` and `.claude/skills/`
  links resolve to the canonical packages. Root README/APM include all three skills.
- Description triggers match workflow branches. Full linked-file review and
  pruning found no embedded credentials or internal endpoints.
