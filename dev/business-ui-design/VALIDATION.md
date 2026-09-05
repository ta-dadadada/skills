# Validation record

## Method and scope

Validated under `shiranui-hanten` after current-branch `frontend-ui-design`
verification, on 2026-09-05. Fresh executors used `gpt-5.6-terra` with `medium`
reasoning as requested. The representative execution is design-only; runtime,
implementation-mode behavior, and accessibility compliance remain untested.

## Requirements, static checks, and placement

- Job/layer: a UI agent selects business information structure and produces a
  task-complete design or implementation through the frontend companion; domain layer.
- Completion: domain acceptance and shared frontend checks have evidence at the
  requested delivery level, with unknowns and unverified work explicit.
- Invocation: model-invoked. Design and implementation/reshaping enter Steps 1–2;
  Step 3 forwards delivery mode to companion Steps 1–4; Step 4 performs companion
  Step 5 and business acceptance together. General frontend work routes out.
- Structure: business steps and acceptance live in SKILL.md; archetypes, data
  workspaces, and provenance have separate references. Common frontend rules
  remain in the companion. A missing companion is an explicit incomplete path.
- Read/prune: SKILL.md and every linked reference read in full. No unresolved
  structural wording finding, credentials, or internal endpoints remained in
  the final pass. Historical findings are recorded below.
- Mechanical: `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/business-ui-design`
  passed, as did whitespace checks.
- Placement: name matches directory; both project tool paths resolve to the
  canonical package. The companion is also reachable through both tool paths.

## Representative execution

Task: 2,000-order queue; compare ID/customer/amount/due/status, repeatedly inspect
routable detail, and approve one eligible authorized record. Server owns paging,
filtering, sorting, eligibility and denial reasons. Pending prevents duplicate
approval, success refreshes status, failure preserves context/retry, conflict
reloads current state. Wide/narrow and keyboard behavior are required. Saved
views, bulk actions, shortcuts, and backend work are excluded.

Observed/reported sequence: read business skill and conditional references →
read installed frontend companion and triggered references → produce the design
artifact → separately inspect it with `sed` and `rg` → report actual artifact
observations and unavailable runtime checks. One record carries the domain
choices and frontend behavior. The artifact preserves comparison through narrow
horizontal scrolling, detail return context, server action scope, and exclusions.
Mechanical, static, and representative current design-branch checks are complete.

## Findings incorporated during authoring

- A trial moved a comparison attribute to detail on narrow screens. Data-workspace
  guidance now distinguishes simultaneous comparison from access to one value.
- Trial review tables were prefilled during artifact creation. Stronger checkpoint
  wording alone did not fix this reliably. Hanten's branching test moved pre-code
  review to implementation only; design evidence is reported after artifact inspection.
- Composition previously completed the entire companion and then reviewed again.
  The final structure runs companion production first and a single combined final
  inspection afterward, with no duplicate review boundary.
- An intermediate executor hit its usage limit; it supplies no passing evidence.

The result verifies a representative procedure, not every generated UI detail.
Source-specific choices (such as denied-action presentation and API schemas)
remain implementation inputs. No application runtime was exercised.
