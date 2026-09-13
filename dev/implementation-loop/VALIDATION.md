# Validation record

## Convergence policy revision — 2026-09-13

Two observed implementation runs confirmed the value of criterion-level state,
repository re-observation, deterministic verification, finding-driven reopening,
and an independent final review. The later run also exposed a convergence
failure: repeatedly replacing the reviewer after each fix broadened review from
the agreed task into a search for theoretical bypasses, and review findings were
used to introduce permanent repository constraints that the task had not
authorized.

The generalized correction stays within this procedure skill's responsibility:

- A finding changes ledger state only when it names its authority, repository
  reachability or support, practical impact, and affected criterion or scope
  owner. Reviewer severity labels are not authority.
- Findings are dispositioned as material actionable, scope/design escalation, or
  non-blocking. A new permanent constraint or design decision is returned to its
  owner instead of being adopted as a repair.
- The first final review remains an independent fresh-context full-diff review.
  Localized fixes return to the same reviewer for targeted regression review;
  reviewer replacement alone does not reset the review surface.
- A fresh full review is repeated only when an authorized material change alters
  architecture, agreed scope, public contract, data model, or trust/security
  boundary, or when new material evidence invalidates the prior review's
  assumptions.
- One criterion is the primary Act target in an iteration. Deterministic and
  review evidence can update other affected ledger rows during re-observation.
- Stop depends on agreed scope: terminal criteria, current green deterministic
  verification, no unresolved material scoped finding, a complete staged review
  chain, and no unauthorized scope expansion.

Responsibility boundaries remain unchanged. `issue-kickoff` owns agreement on
criteria and scope; a user or design owner authorizes new permanent decisions;
specialist skills own implementation method; `pr-handoff` packages an already
converged diff. No runner, persistence format, or reviewer framework was added.

### Scenario self-review

- A first independent review can still block on a reachable defect that violates
  an acceptance criterion or existing rule, so the useful initial finding from
  the observed experiment still reopens work.
- After that defect is fixed, review is constrained to the prior finding, changed
  area, and fix-induced regressions. Changing reviewer does not authorize a new
  search across unrelated syntax and resolver edge cases.
- A proposed syntax, module-resolution, or workspace-layout prohibition must
  point to an existing rule or supported harmful path. When correction instead
  requires a new repository-wide rule, it is escalated and is not added
  automatically.
- Deterministic checks still rerun after every final-review fix, and a material
  architecture or threat-model change still triggers a fresh full review. Cost
  is reduced by narrowing repeated review, not by weakening the initial review
  or the verification gates.

### Revision representative trajectory

A fresh executor applied the revised skill to a bounded dependency-checker
scenario with two satisfied criteria and three independent-review claims: one
reproduced defect in a supported production import form, one unsupported
theoretical CommonJS bypass, and one hypothetical workspace-symlink bypass whose
proposed fix required a permanent repository rule.

The executor reopened only the criterion invalidated by the reproduced defect,
kept the CommonJS and symlink claims non-blocking, introduced no new prohibition,
and returned the localized fix to the same independent reviewer for targeted
re-review. The other criterion remained satisfied while its deterministic
evidence was refreshed. With both criteria satisfied, global checks green, the
initial full review and targeted re-review complete, no unresolved material
scoped finding, and no unauthorized expansion, the executor stopped. It reported
no ambiguity that would make the trajectory diverge and changed no files.

## Responsibility and structure — 2026-09-12

- Job: an implementation agent converges an agreed change one acceptance
  criterion at a time and delivers current verification and review evidence.
- Layer: procedure/orchestration. Specialist skills retain domain implementation;
  `issue-kickoff` retains criteria and scope; `pr-handoff` retains PR and commit
  planning.
- Completion: all criteria are `satisfied` or explicitly `blocked`, global
  verification passes for the current diff, and an independent fresh-context
  full-diff review has no actionable finding.
- Invocation: model-invoked after `issue-kickoff` or equivalent intake when
  feedback-cycle coordination adds value. A small direct change can use its
  specialist workflow without this loop; no criterion-count threshold is fixed.
- Structure: runtime rules and state transitions stay in `SKILL.md`. This record
  holds source observations and evaluation limits so experimental choices do not
  become execution requirements.

An independent skill is warranted because it has its own invocation and owner:
cross-criterion selection, reversible state, feedback routing, blocked-work
continuation, and final convergence apply across Terraform, frontend, backend,
debugging, and other implementation domains. Adding these rules to any one
specialist skill would duplicate them elsewhere; adding them to `issue-kickoff`
or `pr-handoff` would extend those skills beyond their entry or exit boundaries.

## Requirements classification

`Observed` records the supplied Issue #1 run and does not by itself create a
general rule. `Required` is the first-version operating contract selected from
that evidence and the explicit requested boundaries. `Experimental` remains an
evaluation question and is not prescribed by the skill.

| Candidate | Class | First-version decision |
|---|---|---|
| `session-goal` fixed Why/What and `issue-kickoff` prepared criteria, scope, verification, and branch | Observed | Consume agreed inputs without requiring those exact producers. |
| Acceptance criteria are implementation work units | Required | One ledger row and evidence trail per agreed criterion. |
| One iteration changes one criterion | Required | Select exactly one pending criterion; handle prerequisites explicitly. |
| Re-observe current repository state before selection | Required | Reconcile status, diff, relevant files, rules, and ledger each iteration. |
| Prefer deterministic verification to agent judgment | Required | Verification precedes review; inspection cannot replace an available deterministic check. |
| Review findings feed the next iteration | Required | Findings keep or return affected criteria to `pending`. |
| A previously satisfied criterion can reopen | Required | `satisfied → pending` is an explicit transition. |
| External conditions are a formal blocked state | Required | Record evidence and unblock condition; continue independent criteria. |
| Run the project-wide quality gate in every iteration | Observed | Require affected checks per iteration and one global gate at the end; evaluate the cost/value of an unconditional per-iteration gate. |
| Finish with an independent fresh-context full-diff review | Required | A non-author reviews the authoritative inputs and current full diff. |
| Final review findings reopen work | Required | Map each actionable finding to a criterion, fix through the loop, and rerun final gates. |
| Compound stop condition | Required | Terminal criteria, green global verification, and green final review must all hold for the current diff. |
| Persist state in `.agent-loop.md` or another new file | Experimental | No format introduced; use available working context or an existing repository/user convention. |
| Use an independent reviewer for every criterion | Experimental | Iteration review may be performed by the implementer; evaluate whether independence changes outcomes enough to justify its cost. |
| Make the final review the only review | Experimental | Initial version retains review in each iteration plus an independent final review. |
| Reuse the same final reviewer after a fix | Experimental | Require independence, not reviewer identity; compare same-reviewer and new-reviewer reruns later. |
| Invoke the loop for a single small criterion | Experimental | Use coordination value rather than a fixed count; test activation and non-activation cases. |
| Let the skill manage iteration, time, or cost budgets | Experimental | Budget policy remains external until evidence supports a reusable rule. |

## Existing-skill comparison

| Skill | Existing owner | Boundary with `implementation-loop` |
|---|---|---|
| `session-goal` | Session Why/What and `.agent-goal.md` | Supplies purpose; no criterion state or implementation loop moves here. |
| `issue-kickoff` | Acceptance criteria, scope, verification plan, branch | Produces the confirmed handoff consumed by the loop. |
| `session-handover` / `session-resume` | Cross-session checkpoint and reconciliation | May carry the ledger as session status; no new persistence format is required. |
| Specialist implementation skills | Domain method and domain evidence | Execute one selected criterion; return results to the loop. |
| `pr-handoff` | Proposed PR description and commit plan | Starts only after convergence; does not verify or reopen implementation. |

## Evidence and limits

The supplied `life-game-rogue` Issue #1 execution is prior observational evidence:
local review kept the GitHub Pages criterion pending after detecting over-broad
permissions, and a later independent review reopened it after finding missing
`pages: read`. The corrected diff was reverified and rereviewed. This supports the
feedback and reversible-state requirements, but it predates this packaged skill
and therefore is not evidence that the current wording produces the intended
trajectory.

## Representative execution

A fresh executor ran this exact skill against an isolated Python fixture with
three agreed criteria: function formatting, CLI formatting, and an external
release operation for which no endpoint or credential existed. The executor kept
state in working context and created no loop-state artifact.

Observed trajectory: establish three pending rows → re-observe and implement AC1
only → run its mapped test and self-review → mark AC1 satisfied → re-observe and
implement AC2 only → observe its mapped test fail before the change → rerun it
green and self-review → mark AC2 satisfied → re-observe AC3 → record the absent
release capability and mark it blocked without fabricating an operation. Global
`python3 -m unittest -v` then passed 2 tests, and `git diff --check` passed.

A separate fresh-context reviewer received the authoritative task, scope, full
diff, verification evidence, and blocker. It reported no actionable finding
after checking requirement coverage, excess change, configuration, security, and
maintainability. The tracked diff remained limited to `formatter.py`; task and
test inputs were unchanged.

This run exercises one-criterion selection, repeated observation, deterministic
verification before satisfaction, implementer review, formal blocking, the
compound stop gate, and final reviewer independence. It does not test automatic
invocation, finding-driven reopening, continuing useful work after encountering
a blocker before other pending criteria, cross-session persistence, a specialist
skill handoff, or competing reviewer-reuse policies.

## Remaining evaluations

1. Confirm in a repository-backed implementation that a localized fix receives
   targeted same-reviewer re-review, while
   an authorized trust-boundary change resets to a fresh full review.
2. Put a scope/design escalation before an independent pending criterion and
   confirm the affected row is blocked while other work continues.
3. Compare measured defect yield, token use, and wall-clock time for the staged
   policy against repeated fresh full reviews.
4. Observe a session boundary before adding any loop-specific persistence or
   budget mechanism.

## Mechanical and static checks

- `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/implementation-loop`
  passed after the convergence-policy revision.
- `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/* meta/*` passed for
  all 21 packages.
- `uv run scripts/generate_apm_yml.py` processed 21 skills; only the changed
  implementation-loop package metadata remains in the revision diff.
- `git diff --check` passed.
- The frontmatter name matches the directory, the README description matches the
  frontmatter, and both `.agents/skills/` and `.claude/skills/` links resolve to
  the canonical package.
- Static acceptance review maps the finding gate, scope escalation, staged review
  policy, primary-target semantics, reversible state, deterministic gate, and
  scope-aware Stop rule to explicit runtime instructions.
- A focused credential-pattern scan found no embedded token, key, or private-key
  material. No script or external loop runner was added.
