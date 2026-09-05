# Table and grid controls

Use these semantics when the task or domain has selected a table. Representation
choice and dataset-specific action contracts remain inputs to the frontend work.

Start with native table semantics and named column/row headers. Use buttons for
sortable headers with an exposed sort state (for example, `aria-sort`); provide
labels for selection controls and announce significant result/selection updates.
Keep horizontal scroll regions keyboard reachable when required. At narrow
widths, preserve essential comparisons through deliberate column priority or
accessible horizontal scrolling, with access to remaining values.

Use an established accessible grid component only when cell navigation/editing
requires a grid interaction model. A grid needs managed focus and defined arrow,
Enter, and Escape behavior; attaching a grid role alone does not implement it.
Keep optional cell-navigation and clipboard capabilities within task scope.
