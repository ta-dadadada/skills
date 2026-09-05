# Implementation references and limits

This package implements the design/implementation boundary requested by the user
on 2026-09-05. Native semantics, naming, keyboard patterns, and runtime evidence
are implementation responsibilities; the companion retains accessibility outcomes.

Primary references consulted during authoring:

- [APG names and descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/):
  visible/native naming, ARIA overrides, and computed-name checks.
- [APG keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/):
  focus order, compound-widget movement, and focus versus selection.
- [APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/):
  containment, initial/return focus, and dismissal.
- [APG grid](https://www.w3.org/WAI/ARIA/apg/patterns/grid/): managed navigation and editing.

For a component API or an unsupported/custom pattern, consult its current primary
documentation and test the actual browser behavior. These procedures are authoring
guidance and an evidence discipline, not a complete accessibility standard or
certification. The naming preference is an authoring sequence, not the browser's
accessible-name computation order.
