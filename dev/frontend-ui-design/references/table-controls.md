# Table and grid requirements

Use when the task or domain has selected tabular presentation. Representation
choice and dataset-specific action contracts remain inputs.

Specify identifiable column/row headers, accessible active sort column/direction,
selection labels and feedback, and any significant result updates to announce.
At narrow widths, preserve required simultaneous comparisons through deliberate
column priority or horizontal scrolling, with access to remaining values.

Ordinary tables may contain interactive controls without becoming a cell-navigation
grid. Choose a grid interaction contract only when the task needs managed cell
navigation or editing. Define entry/exit, movement, edit/commit/cancel, and selection
behavior needed by that task; clipboard operations remain scope-driven.
Concrete table semantics, grid implementation, and runtime checks belong to
`frontend-ui-implementation`.
