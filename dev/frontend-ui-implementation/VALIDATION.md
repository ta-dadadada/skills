# Validation record

## Responsibility split — 2026-09-05

Created under `shiranui-hanten` to separate coding and runtime evidence from UI design.

- Job/layer: a frontend agent realizes a reviewed UI contract in code and reports
  observed runtime behavior; procedure layer.
- Completion: the requested slice works, applicable runtime/repository checks have
  evidence or explicit unverified status, and defects/integrations are reported.
- Invocation: model-invoked. Supplied designs, design handoffs, and repairs against
  settled behavior enter Step 1. Missing design routes through the design-only
  phase before resuming; conflicting decisions receive a focused return.
- Ownership: native elements/naming/forms/state in semantics-and-forms; key/focus
  mechanics in keyboard-and-focus; table/grid mechanics in tables-and-grids;
  minimum runtime checks and evidence levels in runtime-review. The design
  companion owns the handoff fields and intended interaction outcomes.
- Pruning: mandatory workflow stays in SKILL; conditional table/grid details are
  loaded only for tabular UI. Naming preference is explicitly not computed-name
  precedence. Role attributes are separated from implemented key behavior.

## Representative execution

Run after the design-only trial, with a fresh `gpt-5.6-terra` / `medium`
executor. Task: implement a supplied reviewed reading-preferences contract in
plain HTML/CSS/JS, including a named modal, required Display name, asynchronous
save/failure/retry, loading/empty/load-error fixtures, and responsive/focus cases.

Observed artifacts and executor-reported operations: read implementation skill
and conditional references → build a local fixture → exercise it in an isolated
browser → correct Tab/Shift+Tab containment → recheck both directions → record
evidence. The supplied contract was reused without a new design exercise.
The implementation used native dialog, buttons, input/label, associated errors,
and live status; the parent inspected the code and evidence file.

Runtime observations cover pointer save, keyboard opening/validation/Escape,
modal containment/return, draft-preserving failed save and retry, loading/empty,
load failure/retry, runtime accessibility-tree properties, and 320×500 layout.
`node --check app.js` passed. The plain fixture has no test/lint/typecheck setup.

Evidence review found that keyboard validation was not proof of keyboard completion,
and that “announced success” overstated the observed status update. The runtime
reference now explicitly separates partial paths from completed scenarios. A
focused executor follow-up completed Tab → Enter → text input → Tab → Save
with keyboard alone, observed the updated summary and trigger focus, and corrected
the status wording to the observed accessibility-tree text update.

200% browser zoom and screen-reader announcements remain unverified: the available
browser API could resize the viewport but could not set/confirm browser zoom,
and no assistive-technology session was available. Simulated requests and in-memory
persistence establish no real backend integration. Custom grid/menu/drag behavior
and the missing/conflicting-design return branch were statically reviewed, not
exercised by this form trial. No general accessibility-conformance claim is made. The later Sol/medium
business-chain trial additionally covered a design-to-code handoff, record detail
return, keyboard horizontal scrolling, and a split-to-sequential narrow layout.

## Mechanical and placement checks

- `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/frontend-ui-implementation` passed.
- The full `dev/* meta/*` validator passed for all 18 packages.
- `git diff --check` and explicit whitespace checks covering new files passed.
- Names match canonical directories. Both `.agents/skills/` and `.claude/skills/`
  links resolve to the canonical packages. Root README/APM include all three skills.
- Description triggers match workflow branches. Full linked-file review and
  pruning found no embedded credentials or internal endpoints.
