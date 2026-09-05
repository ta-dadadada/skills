---
name: frontend-ui-implementation
description: >-
  Contract-first frontend UI implementation: realize a reviewed UI design with
  native HTML, appropriate ARIA, keyboard/focus behavior, responsive code, and
  runtime evidence. Use when coding a supplied UI design, completing a
  frontend-ui-design handoff, or fixing implementation against a settled
  interaction contract. If the design is missing, obtain it through
  frontend-ui-design first. Not for standalone UI design or backend-only work.
license: MIT
metadata:
  author: ta-dadadada
---

# Frontend UI Implementation

Realize the supplied UI contract in working code and verify observable behavior.
The design skill owns what the UI should do; this skill owns HTML, ARIA, CSS,
JavaScript/framework implementation and runtime checks.

## When to use

- Implementing a reviewed UI design, in any frontend domain.
- Continuing a `frontend-ui-design` handoff for working UI.
- Repairing code whose intended interaction behavior is already established.

## When not to use

- Standalone design decisions: use `frontend-ui-design`.
- Backend-only work or inventing business rules.

## Workflow

### Step 1 — Consume the contract and inspect the codebase

Read the supplied design and acceptance cases, relevant code, and local rules.
The design skill's `references/handoff.md` defines the handoff; inherit unchanged
context for a small fix. If no design exists, run `frontend-ui-design` to produce
and review the design only, then resume here. A reviewed supplied contract is
sufficient; re-running discovery is unnecessary.

Find existing components, tokens, routing, form/data conventions, and repository
checks. Distinguish real integration from fixtures. Choose coding details within
the contract and record material mappings as implementation notes, separate from
the design requirements even when they share one document. For an impossible,
contradictory, or component-conflicting decision, return only that decision and
affected cases to the design phase for resolution.
Keep consequential missing inputs explicit; complete independent work while a
required answer is pending. If the design companion is needed but unavailable,
report the dependency and unfinished scope.

**Done when:** the reviewed contract and code conventions are available, required
integrations and checks are identified, and blocking design conflicts are resolved
or explicitly isolated from executable scope.

### Step 2 — Implement semantics and interaction

Read [semantics-and-forms.md](references/semantics-and-forms.md) for native
elements, names, form relationships, and state exposure. Read
[keyboard-and-focus.md](references/keyboard-and-focus.md) for interactive UI.
For tables or grids, also read [tables-and-grids.md](references/tables-and-grids.md).

Build a complete vertical slice using existing components and data contracts.
Connect controls to their advertised actions; implement state feedback and
recovery while preserving edits and context. Verify what library components
actually provide before adding handlers or ARIA. Match names and state to real
behavior; a role or attribute supplies semantics, not event handling.
Identify fixture-only behavior and missing integration as such.

**Done when:** the scoped scenario is implemented with appropriate elements,
names/relationships, working input and key behavior, and the contracted states
and recovery; unfinished integration is explicit.

### Step 3 — Implement responsive transitions

Translate the supplied transitions into CSS and component structure. For example,
split panes become sequential views, a sidebar becomes navigable disclosure, and
an auxiliary pane becomes a sheet when the contract calls for them. Reuse tokens
and supported breakpoints; choose breakpoints where real content needs them.

Preserve component state, navigation/return paths, logical DOM/focus order, and
required horizontal comparisons across transitions. Keep hidden duplicate controls
out of the focus/accessibility tree. Use flexible sizing and wrapping with long
content; provide intentional scroll regions for required two-dimensional content.
Keep focus indicators visible and unclipped. Scope visual changes to the contract.

**Done when:** wide and narrow structures implement the specified transitions
without losing the primary task, context, or required comparison information.

### Step 4 — Verify the running UI and deliver

Read [runtime-review.md](references/runtime-review.md). Exercise the actual
interface, including supplied domain acceptance cases, then fix observed defects
and recheck affected cases. Run relevant repository tests, lint, and type checks.
Keep verification notes proportional to the change and report real observations
separately from intended behavior.

Deliver code/artifact locations, material implementation decisions, check results,
and remaining defects, integrations, or unverified cases. Static review supports
static claims; runtime checks support only the behavior and environments exercised.

**Done when:** each applicable runtime and repository check has evidence or an
explicit unverified status, observed defects are fixed or reported, and the
requested working UI and its practical verification limits are delivered.

## Red flags

| Symptom | Correction |
|---|---|
| A settled design triggers fresh discovery | Reuse the contract; return only a conflicting decision |
| Clickable generic elements imitate native controls | Start with the matching native element |
| Every control receives a naming attribute | Use native visible naming before ARIA naming |
| A role is counted as working interaction | Exercise the pattern's keys, state changes, and focus |
| Failed saves erase drafts | Keep draft state separate from confirmed server state |
| Static inspection is called accessibility verification | Report the evidence level and unverified runtime/AT checks |

## Related

- `frontend-ui-design` — design contract owner; required when design is missing or conflicting.
- Domain skills supply acceptance cases through that contract; preserve their scope.
- [sources.md](references/sources.md) — primary implementation references and limits.
