---
name: implementation-loop
description: >-
  Convergence loop for implementing an already agreed change one acceptance
  criterion at a time: re-observe the repository, use deterministic evidence,
  reopen criteria only for material findings tied to agreed scope, escalate new
  project constraints instead of silently adopting them, and use targeted
  re-review after an initial independent fresh-context full-diff review. Use
  after issue-kickoff or equivalent intake when settled criteria, dependencies,
  blockers, or review feedback require coordination across implementation
  cycles. Not for deriving scope or criteria, supplying domain-specific
  implementation methods, PR/commit planning, or a small direct change whose
  normal workflow already provides a sufficient convergence path.
license: MIT
metadata:
  author: ta-dadadada
---

# Implementation Loop

Converge an agreed change by treating each acceptance criterion as a reversible
unit of work. The loop owns observation, selection, evidence, review feedback,
and state transitions; specialist skills own how a selected change is designed
or implemented. A criterion becomes satisfied only after deterministic evidence
and scoped review agree, and it can return to pending whenever material later
evidence invalidates that conclusion. Review searches for defects in the agreed
change; proposed new requirements go to their scope owner. The loop converges
when current global checks are green, scoped review findings are resolved, and
the diff contains no unauthorized expansion.

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
| `satisfied` | Its mapped deterministic verification passed and criterion review has no unresolved material finding. |
| `blocked` | No available authorized action can advance it; the missing external action or condition is recorded. |

Allowed transitions are `pending → satisfied`, `pending → blocked`,
`blocked → pending`, and `satisfied → pending`. A blocked criterion returns to
pending before it can be verified and satisfied.

## Review finding gate

A review label alone never changes the ledger. For each finding, require the
reviewer to provide:

1. the claim and affected path;
2. its authority: an exact acceptance criterion, task requirement, applicable
   existing project rule, ADR, or convention, production path supported by the
   changed implementation, or a concrete correctness, security, or data-loss
   condition;
3. evidence that the path is reachable or supported in this repository, rather
   than merely theoretically expressible;
4. the practical impact and the affected criterion or agreed scope; when no
   ledger row covers that scope, the scope owner who must map the genuine gap.

Classify the supplied evidence into exactly one disposition:

| Disposition | Required handling |
|---|---|
| `material actionable` | The finding is supported by the gate above and can be corrected within agreed scope and existing rules. Keep or return every invalidated criterion to `pending`; a material scoped finding with no row remains unresolved until its owner maps the gap. |
| `scope/design escalation` | Correction needs a new acceptance criterion, permanent prohibition, architecture or coding rule, public contract, or other project-wide decision. Return the decision to the user, acceptance-criteria owner, or design owner; do not adopt it as a repair. |
| `non-blocking` | The claim is speculative, unreachable, unsupported by project evidence, or has no material impact on agreed scope. Record it only when useful; it does not reopen a criterion or prevent Stop. |

When an escalation is necessary to complete an existing criterion, that
criterion can become `blocked` with the decision and owner recorded. An
out-of-scope improvement that is not necessary for an agreed criterion remains
non-blocking for this task. A concrete harm on a supported production path is
not dismissed merely because the issue omitted its syntax or mechanism.

## Delegated review handoff

When an iteration or final review is delegated, send one bounded review brief
instead of asking the reviewer to reconstruct the implementation session. Fresh
context means independent judgment, not missing context. The brief contains:

1. the review mode and exact surface: criterion review, initial full-diff review,
   or targeted re-review, including the questions the reviewer must answer;
2. the authoritative goal, acceptance criteria, in-scope and out-of-scope
   boundaries, and applicable existing project rules, ADRs, and conventions;
3. the exact repository state under review and its diff, with enough identity to
   tell whether later edits make supplied evidence stale;
4. the convergence ledger's verification evidence for that state: each command
   or procedure, the claim and criteria it covers, its result, and the relevant
   output or observation; list checks not run or unavailable with the reason
   instead of implying they passed; and
5. for re-review, the prior findings, their dispositions, the fix delta, and any
   known evidence limits.

Pass only observed results as verification evidence. Mark results reported by
another source as such, and do not present planned checks as completed. A
reviewer consumes current evidence for the same repository state and claim and
does not rerun a handed-off check merely to reproduce a passing result. Reviewer
independence applies to review judgment, not duplicate verification execution.

A reviewer may run a check when an acceptance criterion or project rule requires
an independent run; the supplied evidence is absent, stale, ambiguous, or
inconsistent with the diff; or a new concrete finding needs targeted
reproduction. State the evidence gap and claim before running it, and prefer the
narrowest check that resolves them. The review response identifies supplied
evidence it relied on, any additional check and why it was necessary, remaining
unverified claims, and findings in the Review finding gate format. The reviewer
does not implement the fix.

**Done when:** the reviewer can judge the assigned surface without rediscovering
the task or repeating current checks, and any additional execution has a stated
evidence reason.

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
- Reconcile every relevant row with current evidence. New material evidence that
  invalidates a satisfied row reopens it to pending before selection. A row can
  also become satisfied when its own mapped verification and scoped review
  evidence now hold, even when it was not the prior iteration's primary target.
- Select the highest-priority pending criterion whose dependencies permit useful
  work as the iteration's single primary implementation target. This limits what
  Act is trying to change; it does not limit evidence-based ledger transitions
  to one row. If the target is externally blocked, record the blocker through
  Step 6 and begin another iteration before selecting independent work.

**Done when:** current repository evidence supports the ledger, and exactly one
actionable pending criterion is selected as the primary target, or all remaining
pending criteria have concrete blockers to classify.

### Step 3 — Route and implement the minimum change

- Choose the specialist workflow that matches the selected criterion, such as
  `terraform-implementation`, `frontend-ui-implementation`,
  `backend-api-implementation`, `characterization-testing`, or
  `hypothesis-driven-debugging`. Let it own its domain decisions and required
  checks while this loop retains the criterion boundary and state.
- Implement only what the selected criterion and its necessary prerequisites
  require. If an unplanned prerequisite is independently observable work, return
  it to the acceptance-criteria owner rather than silently adding a criterion.
- Keep collateral changes traceable to the primary target. The change may
  objectively satisfy another criterion, but that result is recognized from
  verification and re-observation rather than by adding another primary target.
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
- When one check objectively covers other criteria, record the result against
  each covered row and run any remaining mapped checks those rows require. This
  evidence is reconciled in Step 5; it does not turn them into additional Act
  targets.
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
- When this iteration review is delegated, use the Delegated review handoff and
  keep its review mode limited to the selected criterion and materially affected
  interactions.
- Apply the Review finding gate to every claim. Only a `material actionable`
  finding keeps or returns an affected criterion to `pending`. A
  `scope/design escalation` goes to its owner without changing requirements or
  code; a `non-blocking` observation does not change ledger state.
- Re-observe all criteria materially affected by the change. Mark any such row,
  including the primary target, satisfied only when its own mapped verification
  passed at the current repository state and scoped review has no unresolved
  material finding. Record both forms of evidence. The implementing agent may
  perform this iteration review; reviewer independence is mandatory at the
  final gate.

**Done when:** every finding has a disposition and affected state, and the
primary target and every other materially affected row reflect current
verification and review evidence, with the primary target satisfied, pending, or
ready for blocked classification.

### Step 6 — Classify blockers and continue independent work

- Mark a criterion blocked only when permission, an external service or setting,
  an unavailable plan, required human action, or another condition outside the
  agent's available authority prevents progress. This includes a necessary
  scope/design decision that the current task does not authorize. Record the
  evidence, the actor or condition that can unblock it, and any dependent
  criteria.
- Continue iterations for independent pending criteria. A blocked row does not
  stop unrelated work.
- Keep escalated improvements that are unnecessary for an agreed criterion out
  of the ledger's blocking path; report them separately instead of extending the
  task.
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
- For the initial final review, use the Delegated review handoff with an
  independent reviewer who did not author the implementation. Set the mode to
  full-diff review and require requirement coverage, excess change,
  configuration, security, and maintainability across the whole diff. A fresh
  reviewer still receives the complete brief; freshness does not require it to
  rediscover scope or repeat the supplied global verification.
- Apply the gate to every final finding. Reopen criteria only for `material
  actionable` findings, route `scope/design escalation` without silently
  changing the task, and retain `non-blocking` observations without extending
  the loop.
- After correcting a finding, rerun global deterministic verification, update
  the handed-off repository state and evidence, and return to the same
  independent reviewer when available. Limit re-review to the prior findings,
  the changed area, and regressions plausibly introduced by the fix. The
  reviewer remains separate from the maker, consumes the updated evidence under
  the handoff rules, and does not implement the fix.
  When that reviewer is unavailable, give an independent replacement the prior
  review and fix context with the same targeted mandate; reviewer replacement
  alone does not require a new full adversarial review.
- Reset to a fresh independent full-diff review only when either an authorized
  change materially alters the architecture, agreed scope, public contract, data
  model, trust boundary or security model, or new material evidence invalidates
  assumptions of the prior full review. Obtain scope or design authorization
  before making a change that requires it. Theoretical room for another reviewer
  to search is not a reset condition.
- When an independent initial review or required re-review cannot be obtained,
  leave that final gate incomplete and report the exact missing capability.

**Done when:** global verification passes at the current repository state, one
initial independent fresh-context full-diff review exists, every delegated review
accounts for supplied and additional verification, every material finding is
resolved by the applicable targeted or reset review, and every escalation has a
recorded disposition; or the exact unavailable final gate is reported without
claiming convergence.

### Step 8 — Stop and hand off

- Stop when every agreed criterion is satisfied or explicitly blocked, global
  deterministic verification is green for the current diff, no unresolved
  material finding is tied to agreed scope, the required review chain from Step
  7 is complete, and the diff contains no unauthorized scope expansion.
- Report each criterion's final state and evidence or blocker, the global
  verification result, the review result and scope, any escalations or
  non-blocking observations worth retaining, and any effects that remain
  externally unverified. Describe blocked work as blocked rather than completed.
- End the loop when these gates hold. The possibility of discovering further
  speculative edge cases does not justify another review cycle.
- Hand the converged diff and recorded evidence to `pr-handoff` when PR
  description or commit planning is requested.

**Done when:** the report proves every scope-aware Stop gate from current evidence
and preserves every blocker, escalation, and verification limit for the next
consumer.

## Red flags

| Rationalization | Reality |
|---|---|
| "I already inspected this at the last iteration" | Repository state is re-observed before every selection; prior reasoning is not current evidence. |
| "Only the selected row may change state" | One iteration has one primary Act target; current evidence may update every materially affected row. |
| "The diff looks right, so verification passed" | Review and deterministic verification answer different questions; neither substitutes for the other. |
| "This was satisfied earlier" | Satisfaction is reversible when later evidence or a finding invalidates it. |
| "One blocked item stops the issue" | Only its dependents stop; independent pending criteria continue. |
| "The reviewer listed it, so it blocks" | A claim reopens work only after authority, reachability, impact, and affected scope pass the finding gate. |
| "Ban that construct so the checker is complete" | A new permanent constraint is a scope/design decision, not an automatic bug fix. |
| "A fresh reviewer might find another bypass" | Fresh full review is required initially and after a material reset; targeted re-review closes localized fixes. |
| "Independent review means rerunning every test" | Independence applies to judgment. Reuse current evidence for the same state and claim; run another check only for a stated evidence gap or independent-execution requirement. |
| "The checks are green, so the loop is done" | Current global verification, terminal criterion states, scoped review, and the no-unauthorized-expansion guard must all hold. |

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
