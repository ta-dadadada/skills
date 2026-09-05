# Design review pass

Use the primary scenario and failure cases from Step 1. For each applicable row,
report **pass / defect / unverified**, the observation or artifact location, and
any correction. Mark inapplicable checks with a reason. A design walkthrough
validates specified behavior; runtime evidence validates implemented behavior.
In implementation mode, review the proposed structure before coding, then check
the running interface afterward. In design mode, inspect the produced
specification/prototype before reporting results. A separate review document is
optional; use the final response for observed evidence. Check contracts for
contradictions before marking pass.

| Check | Evidence to seek |
|---|---|
| Task | Complete the main job from its entry point; every required action has a discoverable GUI path |
| Hierarchy and density | Required simultaneous information remains legible with realistic data; decoration does not displace it |
| Navigation | Page and detail transitions retain expected context; Back/direct entry work where applicable |
| Action locality | Actions sit near their target and affect their advertised scope |
| Disclosure | Supplementary information can be reached without making primary work harder |
| Efficiency | Frequent operations have a justified efficient path; optional features stay within scope |
| State visibility | Applicable loading, refreshing, saving, selection, and success states are distinguishable |
| Recovery | Empty, no-match, validation, access, and error cases have honest next steps; failed edits retain input |
| Keyboard and focus | Main task works without pointer input; focus is visible, ordered, and restored after transient UI |
| Semantics | Controls have names, forms have labels, tables have headers/sort state, and updates are announced appropriately |
| Contrast and targets | Applicable text/control contrast and target-size requirements are checked; color is supplemented by another cue |
| Responsive and zoom | Wide/narrow layouts and 200% zoom preserve the actual task, including simultaneous comparison where required; mere access to hidden data is insufficient |
| Consistency | Shared components/tokens and user-facing terms match the surrounding product |
| Implementation integrity | Controls work, data scope is truthful, permissions are respected, and relevant repository checks pass |

For implementation, exercise a normal path, a relevant empty/error path, and
the main keyboard path in the running UI. Exercise mutation failure when writes
are in scope. Exercise additional domain acceptance cases supplied by the task.
Screenshots support visual findings, not claims about interactive behavior.

Use repository-approved browser/accessibility tools when available. Report the
actual viewport, zoom, and check results. If runtime or assistive-technology
testing is unavailable, retain that limitation and specify the pending check;
avoid converting code inspection into a runtime or accessibility-compliance claim.
