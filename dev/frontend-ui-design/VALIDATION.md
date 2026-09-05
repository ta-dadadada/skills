# Validation record

## Method and scope

Validated under `shiranui-hanten`, before `business-ui-design`, on 2026-09-05.
Fresh executors used `gpt-5.6-terra` with `medium` reasoning as requested.
The current representative trial is design-only; implementation-mode behavior,
application runtime, and accessibility compliance are not empirically verified.

## Requirements, static checks, and placement

- Job/layer: a frontend agent produces a task-complete design or implementation
  with observed evidence; domain layer (frontend interface work).
- Completion: the primary scenario is specified or exercised at the requested
  delivery level; applicable checks and limitations are reported.
- Invocation: model-invoked. Design and implementation map to the corresponding
  Step 4 branches. Domain handoff maps to Step 1 record reuse. Excluded brand
  and backend work has no execution branch.
- Structure: ordered steps live in SKILL.md. Surfaces, input/state contracts,
  visuals, table semantics, review criteria, and provenance have separate homes.
  Pre-code review is conditional on implementation; artifact inspection is shared.
- Read/prune: SKILL.md and every linked reference read in full. Historical
  premature-completion issues are described below. No unresolved structural
  wording finding, credentials, or internal endpoints remained in the final pass.
- Mechanical: `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/frontend-ui-design`
  passed, as did whitespace checks.
- Placement: name matches the canonical directory; both `.agents/skills/` and
  `.claude/skills/` links resolve to the canonical package.

## Representative execution

Task: personal reading-app text-size settings. Integer 12–24 px, valid input
updates a sample immediately, invalid input retains the previous valid preview
and reports errors on blur/Save, explicit asynchronous Save prevents duplicates,
failure retains draft/retry, and success marks saved. Wide/narrow and keyboard
behavior are required; product components are supplied facts without source/runtime.

Observed/reported sequence: read the skill and triggered references → specify
the task and behavior → write the design artifact → separately read the generated
Markdown → report static observations and unavailable runtime checks. The artifact
contains the required value/validation/save paths, responsive/keyboard contracts,
and acceptance scenarios. No business companion or unstated procedural decision
was needed. Current design-branch mechanical, static, and representative execution
checks are complete.

## Findings incorporated during authoring

Earlier trials filled pre-build/final review tables during artifact creation.
Requiring separate pre-build records for design-only specifications encouraged
ceremonial records. The final structure applies pre-code review to implementation
and uses actual post-artifact observations in the final response for design work.
Earlier checkpoint-oriented trial results do not establish current-branch coverage.
Input guidance also names value/commit events and consistent action states after
trials exposed contradictory immediate-versus-committed update descriptions.

These trials assess procedure execution, not universally correct generated UI.
Every generated artifact still needs review; runtime claims require runtime evidence.
