# Design-to-implementation handoff

This is the authoritative handoff contract. Use an existing specification,
prototype annotations, or task notes; no fixed document template is required.
For a small change, reference unchanged context and record only the delta.
State required outcomes here, such as accessible sort direction, rather than
choosing an ARIA attribute or CSS rule. If one document spans both phases, keep
later code-level decisions in a separate implementation-notes section; they are
not part of the reviewed design contract.

Pass these inputs to `frontend-ui-implementation`:

- Primary scenario, entry point, successful outcome, and delivery scope.
- Selected information structure, components, navigation, and surfaces.
- Interaction/state contracts: triggers, actions, feedback, recovery, preserved
  context, and applicable permission/data boundaries.
- Responsive transitions and information that must remain available together.
- Keyboard operation and focus requirements.
- Accessibility requirements and observable outcomes.
- Acceptance cases, including supplied domain cases and design-review findings.
- Existing design system/component constraints, distinguishing inspected facts
  from supplied descriptions.
- Unresolved assumptions, missing integrations, and consequential unknowns.

Mark inapplicable items briefly or inherit them from established context.
Identify unresolved contradictions as defects, rather than accepted behavior.
The implementation skill may resolve routine coding choices within this contract.
An impossible, contradictory, or component-conflicting decision returns here for
revision of that decision and its affected acceptance cases. Preserve the rest
of the design and continue implementation after the focused review.
