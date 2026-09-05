# Tables and grids

## Native table default

Use `<table>` with identifiable headers (`th`, appropriate `scope`) and a caption
or other appropriate accessible name. Interactive controls inside cells do not
by themselves require a grid. Put a native button inside a sortable header and
set `aria-sort` on the active `th`; update real ordering and sort state together.
Label selection controls with their record context and expose selection outcomes.

Implement filtering, sorting, paging, and selection against the contract's actual
data scope, not just the mounted rows. Keep stable record keys through updates.
For required horizontal comparison, use an intentional overflow container, expose
its purpose, and make keyboard scrolling reachable where needed. Preserve required
columns together; hiding each value in detail does not preserve comparison.

## Grid only for a contracted cell interaction model

Use a tested grid component when the task needs managed cell navigation/editing.
Implement and exercise the chosen model, including:

- A managed focus entry/exit point and arrow movement between cells.
- Enter or the contracted key to enter editing/commit; Escape to cancel/exit
  editing without stealing native text-editing keys.
- Selection state and range behavior only where requested, distinct from focus.
- Clipboard commands only where contracted, with explicit scope, validation,
  permissions, and failed-write recovery.

Virtualized rows need coherent position/count semantics and focus recovery when
unmounted. `role="grid"` supplies none of the movement, editing, or selection
logic. Consult the [APG grid pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/)
for the chosen interaction model; keep optional features within the supplied scope.
