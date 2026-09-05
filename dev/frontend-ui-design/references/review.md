# Design review pass

Use the primary scenario and failure cases from Step 1. For each applicable row,
report **pass / defect / unverified**, the observation or artifact location, and
any correction. Mark inapplicable checks with a reason. A design walkthrough
validates specified behavior; runtime evidence validates implemented behavior.
Inspect the produced specification/prototype before reporting results. A separate
review document is optional; use the final response for observed evidence.
Check contracts for contradictions before marking pass. Here, pass means the
design specifies a coherent behavior; it never means runtime accessibility passed.

| Check | Evidence to seek |
|---|---|
| Task | Walk the specified scoped scenario through the standard GUI, including signposted menus or contextual affordances, without shortcut knowledge |
| Hierarchy and density | Required simultaneous information remains legible with realistic data; decoration does not displace it |
| Navigation | Page and detail transitions retain expected context; Back/direct entry work where applicable |
| Action locality | Actions sit near their target and affect their advertised scope |
| Disclosure | Supplementary information can be reached without making primary work harder |
| Efficiency | Frequent operations have a justified efficient path; optional features stay within scope |
| State visibility | Applicable loading, refreshing, saving, selection, and success states are distinguishable |
| Recovery | Empty, no-match, validation, access, and error cases have honest next steps; failed edits retain input |
| Keyboard and focus | Main task has a complete keyboard contract; focus visibility, order, and return after transient UI are specified |
| Semantics | Control names, field labels, table headers/sort state, and update announcements are specified |
| Contrast and targets | Applicable text/control contrast and target-size requirements are specified; color is supplemented by another cue |
| Responsive and zoom | Wide/narrow and 200% zoom requirements preserve the task, including simultaneous comparison where required; mere access to hidden data is insufficient |
| Consistency | Shared components/tokens and user-facing terms match the surrounding product |
| Handoff completeness | Required behavior, system constraints, acceptance cases, and unresolved assumptions are available to implementation |

Carry applicable runtime checks forward as acceptance cases in the handoff.
Design inspection can assess specified contrast targets, focus order, and zoom
transitions; measured contrast, actual key operation, and assistive-technology
behavior require implementation evidence. Name those pending checks explicitly.
