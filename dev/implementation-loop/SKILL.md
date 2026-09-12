---
name: implementation-loop
description: >-
  Convergence loop for implementing an already agreed change one acceptance
  criterion at a time: re-observe the repository, select one pending criterion,
  route its implementation through the relevant specialist workflow, prefer
  deterministic verification, review the result, continue independent work
  around blocked criteria, reopen criteria on findings, and finish with global
  verification plus an independent fresh-context full-diff review. Use after
  issue-kickoff or equivalent intake when settled criteria, dependencies,
  blockers, or review feedback require coordination across implementation
  cycles. Not for deriving scope or criteria,
  supplying domain-specific implementation methods, PR/commit planning, or a
  small direct change whose normal implementation workflow already provides a
  sufficient convergence path.
license: MIT
metadata:
  author: ta-dadadada
---

# Implementation Loop

Converge an agreed change by treating each acceptance criterion as a reversible
unit of work. The loop owns observation, selection, evidence, review feedback,
and state transitions; specialist skills own how a selected change is designed
or implemented. A criterion becomes satisfied only after deterministic evidence
and review agree, and it can return to pending whenever later evidence invalidates
that conclusion. The whole change is done only when the current full diff passes
global verification and an independent fresh-context review.

## When to use

- Acceptance criteria, scope, and verification plans are already agreed, and the
  implementation benefits from explicit convergence across feedback cycles.
- Several criteria, dependencies, external blockers, or later review findings
  make completion state liable to change during implementation.
- Continuing implementation after `issue-kickoff` or equivalent intake has
  prepared the work.

## When not to use

- Scope or acceptance criteria still need to be derived or confirmed — use
  `issue-kickoff` first.
- A specialist implementation workflow is sufficient by itself for a small,
  direct change with no useful coordination overhead.
- The task is only domain design or implementation guidance; use the applicable
  specialist skill directly.
- The diff is already converged and only needs a PR description or commit plan —
  use `pr-handoff`.

## Working state

Maintain one ledger whose rows contain the criterion, its mapped verification,
dependencies, current state, and evidence or blocker. Keep it in the available
working context; persist it only when the user or repository already requires a
durable artifact. The skill defines no new state-file format.

| State | Meaning |
|---|---|
| `pending` | Work or evidence remains, including work reopened by a finding. |
| `satisfied` | Its mapped deterministic verification passed and criterion review has no actionable finding. |
| `blocked` | No available authorized action can advance it; the missing external action or condition is recorded. |

Allowed transitions are `pending → satisfied`, `pending → blocked`,
`blocked → pending`, and `satisfied → pending`. A blocked criterion returns to
pending before it can be verified and satisfied.

## Workflow

### Step 1 — Establish the convergence ledger

- Consume the agreed goal, acceptance criteria, in/out-of-scope boundary, and
  criterion-to-verification mapping from `issue-kickoff` or an equivalent
  confirmed source. Preserve their wording and ownership instead of deriving a
  replacement specification here.
- Create or reconcile one ledger row per criterion. Reuse a prior state only when
  its evidence still identifies the repository state it verified; otherwise set
  the affected row to pending.
- When a missing or ambiguous input would change implementation, return that gap
  to `issue-kickoff` or the user, then resume this workflow with the amended input.

**Done when:** every agreed criterion has exactly one ledger row, mapped
verification, known dependencies, and a state justified by current evidence, and
the scope boundary is available to every later review.

### Step 2 — Re-observe and select one criterion

- At the start of every iteration, inspect the current repository status and
  diff, the code or configuration relevant to the pending work, the ledger, and
  any applicable project rules. Treat earlier plans and inferences as history,
  not as facts about the current checkout.
- Reconcile observations with the ledger. New evidence that invalidates a
  satisfied row reopens it to pending before selection.
- Select the highest-priority pending criterion whose dependencies permit useful
  work. One iteration has one selected criterion. If it is externally blocked,
  record the blocker through Step 6 and begin another iteration before selecting
  independent work.

**Done when:** current repository evidence supports the ledger, and exactly one
actionable pending criterion is selected, or all remaining pending criteria have
concrete blockers to classify.

### Step 3 — Route and implement the minimum change

- Choose the specialist workflow that matches the selected criterion, such as
  `terraform-implementation`, `frontend-ui-implementation`,
  `backend-api-implementation`, `characterization-testing`, or
  `hypothesis-driven-debugging`. Let it own its domain decisions and required
  checks while this loop retains the criterion boundary and state.
- Implement only what the selected criterion and its necessary prerequisites
  require. If an unplanned prerequisite is independently observable work, return
  it to the acceptance-criteria owner rather than silently adding a criterion.
- Keep the selected criterion pending while implementation and evidence are
  incomplete.

**Done when:** the selected criterion has the smallest complete implementation
allowed by its specialist workflow, with every changed path traceable to that
criterion, or a concrete blocker prevents further authorized action.

### Step 4 — Verify before judging

- Run the selected criterion's mapped deterministic verification and the
  repository checks required for the affected surface. Prefer executable tests,
  builds, linters, type checks, schema validation, and real-operation checks over
  an agent's inspection when both can answer the same claim.
- A failed check leaves the criterion pending and supplies the next iteration's
  evidence. A check unavailable because of an external condition records the
  exact condition for Step 6; lack of evidence never produces `satisfied`.
- Run a project-wide quality gate here when project rules require it for each
  change or the selected criterion can invalidate distant behavior. Step 7 still
  runs the final global verification against the complete current diff.

**Done when:** every runnable mapped check has a recorded result at the current
repository state, failures remain pending, and unavailable checks identify the
condition that prevented them.

### Step 5 — Review and transition

- Review the selected change against its criterion, the full scope boundary, and
  its interaction with the existing diff. Check requirement coverage, excess
  change, configuration, security, and maintainability separately from the
  deterministic verification result.
- Map every actionable finding to the affected criterion. A finding keeps the
  selected criterion pending or reopens any affected satisfied criterion to
  pending; it becomes input to the next iteration. A finding that exposes missing
  or changed scope returns to the acceptance-criteria owner before implementation
  continues.
- Mark the selected criterion satisfied only when its mapped verification passed
  at the current repository state and this review has no actionable finding.
  Record both the evidence and review result in its ledger row. The implementing
  agent may perform this iteration review; reviewer independence is mandatory
  only at the final gate.

**Done when:** every finding has a disposition and affected state, and the
selected criterion is either satisfied with current verification and review
evidence, pending with its next evidence, or ready for a blocked classification.

### Step 6 — Classify blockers and continue independent work

- Mark a criterion blocked only when permission, an external service or setting,
  an unavailable plan, required human action, or another condition outside the
  agent's available authority prevents progress. Record the evidence, the actor
  or condition that can unblock it, and any dependent criteria.
- Continue iterations for independent pending criteria. A blocked row does not
  stop unrelated work.
- When its condition changes, move a blocked criterion to pending, re-observe the
  repository, and verify it through the normal loop; never move it directly to
  satisfied.

**Done when:** every non-actionable criterion has a specific blocker and unblock
condition, and either another independent pending criterion will enter Step 2 or
all rows are satisfied or blocked.

### Step 7 — Run the final gates

- After no pending row remains, run the project's global verification against the
  complete current diff. Map a failure to the affected criterion, reopen it to
  pending, and return to Step 2.
- Give an independent reviewer with fresh context the authoritative goal,
  acceptance criteria, scope boundary, current full diff, and verification
  evidence. Have it review requirement coverage, excess change, configuration,
  security, and maintainability across the whole diff. The reviewer must not have
  authored the implementation; no particular agent or reviewer reuse policy is
  required.
- Map each actionable final finding to its affected criterion and reopen that row
  to pending. Resolve findings through the normal loop, then rerun global
  verification and an independent review against the updated full diff. When an
  independent review cannot be obtained, leave the final gate incomplete and
  report the exact missing capability.

**Done when:** global verification passes at the current repository state and an
independent fresh-context review of that same full diff has no actionable
finding, or the exact unavailable final gate is reported without claiming
convergence.

### Step 8 — Stop and hand off

- Stop only when every criterion is satisfied or explicitly blocked, global
  verification is green for the current diff, and the final independent review
  is green for that diff.
- Report each criterion's final state and evidence or blocker, the global
  verification result, the final review result, and any effects that remain
  externally unverified. Describe blocked work as blocked rather than completed.
- Hand the converged diff and recorded evidence to `pr-handoff` when PR
  description or commit planning is requested.

**Done when:** the report proves all three stop gates from current evidence and
preserves every blocker and verification limit for the next consumer.

## Red flags

| Rationalization | Reality |
|---|---|
| "I already inspected this at the last iteration" | Repository state is re-observed before every selection; prior reasoning is not current evidence. |
| "Two related criteria are faster together" | One iteration has one work unit; dependencies are selected and evidenced explicitly. |
| "The diff looks right, so verification passed" | Review and deterministic verification answer different questions; neither substitutes for the other. |
| "This was satisfied earlier" | Satisfaction is reversible when later evidence or a finding invalidates it. |
| "One blocked item stops the issue" | Only its dependents stop; independent pending criteria continue. |
| "The final reviewer found just one issue" | Every actionable finding reopens affected work before the stop gates run again. |
| "The checks are green, so the loop is done" | Current global verification, terminal criterion states, and a green independent full-diff review are all required. |

## Related

- `session-goal` — owns the session's Why and What before implementation intake.
- `issue-kickoff` — owns agreement on acceptance criteria, scope, verification
  mapping, and the working branch; this loop consumes that handoff.
- Specialist design, testing, debugging, and implementation skills own the work
  inside a selected criterion; this loop owns cross-criterion convergence.
- `session-handover` and `session-resume` — preserve and reconcile in-flight work
  when the loop crosses sessions; this skill introduces no persistence format.
- `pr-handoff` — consumes the converged diff and evidence for PR and commit
  planning after the stop gates pass.
