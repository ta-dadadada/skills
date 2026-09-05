# States and input

## Forms

Use persistent visible labels, optional format guidance, and errors associated
with the relevant fields. Placeholder text may illustrate input. Group fields
by task and state the save scope: field, section, or whole form.
Specify the value-change and commit events (for example input, blur, or submit),
when dependent content updates, and the input constraints. Keep proposed defaults
separate from confirmed domain rules. A missing rule remains an unresolved
acceptance condition; do not describe contradictory behaviors as completed design.

Choose validation timing that helps correction without interrupting unfinished
input. On failed submission, retain values, identify the problem and repair,
and move/announce focus appropriately. Explain inactive actions near their
trigger; where useful, let attempted submission reveal actionable validation.
Distinguish validation, permission, and pending-request reasons for inactivity.

For asynchronous saves, expose pending/success/failure status, prevent accidental
duplicate submission, and retain edits on failure. Optimistic changes need
rollback or reconciliation. When concurrent edits are possible, follow the
existing conflict contract and expose a recoverable conflict state.

## State contract

For each applicable state, name its trigger, visible feedback, allowed actions,
and exit/recovery. Record an explicit reason for inapplicable states.
For each action, choose visible/enabled, visible/inactive with a reason, or hidden
in each applicable permission and processing state. Use that same choice in the
screen description, state contract, and acceptance cases.

| State | User-visible contract |
|---|---|
| Initial loading | What is being loaded; stable layout and announced progress |
| Refreshing | Existing context remains intelligible; stale/pending status is clear |
| First use / empty collection | What belongs here and an eligible first action |
| No matching results | Active query/filter context and an easy reset/change path |
| No access | Access limitation and an available request/switch/back path |
| Recoverable load error | What failed and a retry or corrective action |
| Saving | Pending status and predictable duplicate-submission handling |
| Save failure | Preserved input, cause where known, and retry/correction |
| Partial operation failure | Successful and failed parts, with scoped recovery |
| Success | Visible outcome and continuing context; undo where supported |
| Unrecoverable error | Clear state plus an available support/back path |

Use actual product capabilities for recovery actions. Represent permission
failures distinctly from empty data, and preserve security boundaries in error
details. Convey status with text or symbols as well as color.
