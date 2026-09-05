# Data workspaces

## Representation and views

Prefer a table for homogeneous records whose attributes need comparison or
repeated editing. Use a list for scanning records with little column comparison,
a card/grid for visual objects, and a board for work organized by stage.

Model alternate slices of the same records as filters, sort/group settings, or
views before introducing separate workflows. Persist views when reuse warrants
it and storage exists; distinguish private/shared view scope if supported.
Presentation changes keep the underlying records and action semantics consistent.
Separate pages remain appropriate for genuinely different tasks or permissions.

Specify visible attributes from the job. Use domain labels, consistent number
and date formatting, clear alignment, and a way to inspect truncated values.
When simultaneous attribute comparison is required, preserve it at narrow widths
through accessible horizontal scrolling or another comparison surface. Access to
one hidden value at a time in detail is not equivalent to comparing records.
Choose pagination or virtualization from actual volume and available components;
retain accessible navigation and clear loading/result counts.

## Minimum interaction contract

Specify only capabilities the task needs:

- Search/filter: query scope, active conditions, clear/reset, zero-match recovery.
- Sorting: active column/direction, stable ordering, and server/client ownership.
  Apply sorting/filtering to the advertised dataset, including unloaded pages.
- Selection: stable record identity, selected count, current-page versus all-match
  scope, and behavior after filters, paging, refresh, or view changes.
- Batch action: eligible targets, permissions, partial failures, and result feedback.
- Detail: selected record, retained list context, close/Back, and narrow-screen return.
- Inline edit: start, commit, cancel, validation, pending feedback, and failed-save
  recovery that retains input. Use a full form where fields are interdependent.

Pass mutation and recovery requirements to `frontend-ui-design`.
Column resizing, reorder, multi-sort, nested filters, clipboard editing, and
aggregations are task-driven extensions, not a table's admission requirements.

## Frontend handoff

Pass the chosen table/list/board representation and its interaction contract to
`frontend-ui-design`. Table/grid semantics, responsive access, and keyboard/focus
execution have their authoritative home in that companion skill.
