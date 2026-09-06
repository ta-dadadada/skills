---
name: shiranui-hansode
description: Evaluate agent instructions when the user explicitly requests a structural review, empirical comparison, or iterative tuning. Compare outcomes, required boundaries, and observed execution across the selected environments. Not an automatic follow-up to skill edits.
license: MIT
---

# Empirical Prompt Tuning

Forked from [mizchi/skills: meta/empirical-prompt-tuning](https://github.com/mizchi/skills/tree/main/meta/empirical-prompt-tuning); substantially modified for this repository's conventions (added per-step `Done when:` criteria, reworked the `Related` section, and other changes below) and treated here as an independent skill.

Author review can assess static consistency but cannot establish execution quality. Use fresh executors without authorial context, inspect their artifacts and observable actions, and separate evidence from self-report. Match the evaluation scope to the request: structural review, bounded comparison, or an explicitly requested tuning loop.

## When to use

- An explicit request to check instruction structure or description/body consistency.
- An explicit request to compare execution before and after an instruction change.
- An explicit request to iteratively tune instructions against fixed requirements.

## When not to use

- Automatic evaluation after every skill edit.
- Treating a subjective preference as a proven execution improvement.
- A one-off prompt whose evaluation cost is not justified by the requested task.

## Workflow

Choose the requested mode before running steps. Structural review ends after Step 0 without executing scenarios or editing the target. Bounded comparison runs Steps 0–4 for the requested versions and reports results; it does not enter the tuning loop. Steps 5–7 require an explicit tuning request. Reuse the caller's fixed cases and budget when supplied.

0. **Iteration 0 — description / body consistency check** (static, no dispatch needed)
   - Read the triggers / use cases claimed by the frontmatter `description`
   - Read the scope the body actually covers
   - Record gaps with file/section evidence. In execution modes, resolve or isolate a gap before interpreting results; structural review reports it without modifying the target
   - Example: description says "navigation / form filling / data extraction" but the body is only a CLI reference for `npx playwright test` — detect that kind of gap
   - Keep invocation coverage separate from execution quality: a successful explicitly invoked run does not establish that the description selects the skill correctly
   - **Done when:** description/body coverage and gaps are recorded. Structural review delivers findings and stops here; execution modes carry relevant gaps into the evaluation limits.

1. **Baseline preparation**: Fix the target prompt and prepare the following inputs.
   - **Evaluation scenarios** scoped to the change: start with the affected case and relevant boundary or non-activation cases. Add cases or repetitions when differences, failures, or uncertainty justify them; do not require a full-suite comparison for every change.
   - **Requirements checklist** (for computing accuracy). For each scenario, enumerate 3 to 7 items the deliverable must satisfy. Accuracy % = items satisfied / total items. Fix this in advance (do not move it afterward).
   - Record tool/version, model identifier, reasoning settings, permissions, available tools, installed instructions, task fixture, target revision, and resource limit. Use identical fixtures and settings within each before/after pair; report environmental differences separately.
   - **Done when:** scenarios, checklists, environment records, and comparison scope are fixed before execution.
2. **Fresh execution context**: Start a separate session or fresh agent for each case/version with no authorial history or previous variant results. Use the environment's supported launcher, permissions, and tracing; consult [executor-environments.md](references/executor-environments.md) for environment-specific capture. Independent runs may run concurrently in isolated fixtures when supported.
   - **Done when:** each selected case/version has a fresh executor, or its unavailable execution environment is recorded.
3. **Execution**: Hand the executor a prompt that follows the **executor invocation contract** described below, and have it execute the scenario. The executor produces an implementation or output and returns a self-report at the end.
   - **Done when:** each dispatched executor has returned a report in the contract's structure.
4. **Two-sided evaluation**: Record the following from the returned results.
   - **Executor self-report** (extracted from the body of the executor's report): unclear points / material judgment and assumptions / places where template application got stuck
   - **Trace interpretation**: each unclear point is tagged with the phase it originated in (Input review / Plan artifact / Execution / Formatting — see "Executor invocation contract"). Phase-local fixes land better than global "the prompt was unclear" fixes; a single input ambiguity often looks like a chain of Execution-phase failures.
   - **Structured reflection**: each unclear point must be returned as `Issue / Cause / General Fix Rule`. The `General Fix Rule` is the class-level abstraction that feeds the "Failure pattern ledger" — without it, fixes stay as one-off patches that rediscover the same mistake later.
   - **Instruction-side measurements** (the judgment rules are defined canonically in this section; refer to it from elsewhere):
     - Success/failure: counts as success (○) only when **all** requirements tagged `[critical]` are ○. If even one is × or partial, it is failure (×). The label is the binary ○ / × only.
     - Accuracy (achievement rate of the requirements checklist, %. ○ = full score, × = 0, partial = 0.5; sum and divide by total items)
     - Operation count (reads/searches, writes, checks, and other observable operations); preserve the capture source and native call count separately, following the environment reference. Missing data is N/A, not zero
     - Duration (elapsed execution time with source and unit; distinguish tool-reported time from wall time)
     - Retry count (repeated attempts visible in the trace, with self-reported decision retries labelled separately)
     - **On failure, add a one-line note to the "unclear points" section of the presentation format stating "which [critical] item dropped"** (for root cause tracing)
   - The requirements checklist must include **at least one** `[critical]`-tagged item (if there are zero, the success judgment becomes vacuous). Do not add or remove [critical] tags after the fact.
   - Judge correct outcomes and critical boundaries before cost. Distinguish permitted routine choices from unsupported business, scope, or authority decisions and assumptions presented as facts. Causes in self-reports are hypotheses until corroborated by artifacts or traces.
   - **Done when:** every attempted scenario has results or an explicit execution limit, findings distinguish evidence from self-report, and bounded comparison delivers its findings without entering Step 5.
5. **Apply the diff**: Put the minimum fix into the prompt to eliminate the unclear points. One theme per iteration (multiple related fixes are OK, unrelated fixes go to next time).
   - **Before applying the fix, explicitly state "which item in the requirements checklist / judgment wording this fix satisfies"** (fixes inferred from axis names often do not land. See the "Fix propagation patterns" section below.)
   - **Consult the failure pattern ledger first**. If the structured reflection's `General Fix Rule` already matches a known pattern, the first question is "why didn't the existing fix prevent it?" — the fix may need to move closer to the top of the prompt, or be re-worded, before a new ledger entry is added.
   - **Done when:** the prompt is edited, the edit is stated to satisfy a named checklist item or judgment wording, and the ledger has been checked for a matching pattern.
6. **Re-evaluate**: Run 2 → 5 again with a new executor (do not reuse the same agent: it has learned the previous improvements). Expand cases or repetitions only to resolve a specific uncertainty within the agreed budget.
   - **Done when:** a fresh executor has evaluated the edited prompt against the same scenarios and checklists.
7. **Convergence check**: The rough rule is "stop when 2 consecutive iterations have zero new unclear points AND metric improvements fall below the thresholds (below)". Make it 3 consecutive for high-importance prompts.
   - **Done when:** the "Iteration stopping criteria" section below has been checked against the latest rounds and yields convergence, divergence, or an explicit resource-cutoff call.

## Evaluation axes

| Axis | How to capture | Meaning |
|---|---|---|
| Success/failure | Did the executor produce the intended deliverable (binary) | Minimum bar |
| Accuracy | What % of requirements the deliverable satisfies | Degree of partial success |
| Operation count | Observable operations with capture method; native call count kept separately | Cost indicator requiring trace interpretation |
| Duration | Recorded elapsed time and source | Operational cost; affected by tool latency and environment |
| Retry count | How many times the same decision was redone | Signal of instruction ambiguity |
| Unclear points (self-report) | Executor enumerates as bullets | Qualitative improvement material |
| Judgment (self-report and trace) | Routine choices, explicit assumptions, or unsupported consequential decisions | Distinguishes permitted discretion from requirement or boundary defects |

**Weighting**: Correct outcomes and required boundaries are primary; unnecessary questions, reads, repeated checks, and premature stopping are execution findings. Time and operation count are auxiliary. Do not trade a critical regression in one environment for gains in another.

### Interpreting execution cost

Compare the same case before and after within one environment. More operations may reflect task complexity, necessary verification, batching differences, or tool latency rather than instruction waste. Inspect repeated or irrelevant work before attributing a difference to the instruction. Raw call counts are not directly comparable across tools. Add inline guidance or adjust reference conditions only when the trace supports that diagnosis.

### Fix propagation patterns (conservative / overshoot / zero-shoot)

Fix → effect is not linear. Pre-estimation can play out in the following 3 patterns:

- **Conservative swing** (estimate > actual): one fix aimed at multiple axes but only moved one. "Aiming at multiple axes tends to miss."
- **Overshoot** (estimate < actual): one structural piece of information (e.g., a combination of command + config + expected output) satisfied judgment wording across multiple axes at once. "Combinations of information structurally hit multiple axes."
- **Zero-shoot** (estimate > 0, actual = 0): a fix inferred from the axis name did not reach any of the judgment wording. "Axis names and judgment wording are different things."

To stabilize this, **before applying the diff, have the executor verbalize "which judgment wording this fix satisfies"**. Estimation accuracy does not come out unless you tie things at the threshold-wording level. When adding a new evaluation axis, also concretize the judgment criteria for each point down to the threshold-wording level (at a granularity the executor can judge, such as "all explicit" or "full text of a minimum working configuration" — so it knows what constitutes 2 points).

## Executor invocation contract

The prompt given to the executor takes the following structure. Request observable actions and concise results, not private reasoning. This is the input contract for "two-sided evaluation".

```
You are an executor reading <target prompt name> with a blank slate.

## Target prompt
<For execution quality, provide the target instruction or its path. For invocation testing, provide the candidate descriptions without telling the executor which skill to choose.>

## Scenario
<One paragraph setting the scenario context>

## User requirements (only information available in the real request)
1. <explicit user requirement>
2. <normal item>
3. <normal item>
...
(Keep evaluator-only expected decisions and scoring criteria outside the executor prompt. Critical tags belong in the evaluator checklist.)

## Task
1. Follow the target prompt to execute the scenario and produce the deliverable.
2. On completion, respond with the report structure below.

## Report structure
- Deliverable: <artifact or execution summary>
- Requirement achievement: observable result for each supplied requirement
- **Trace** (tag OK / stuck / skipped for each phase, one-line reason when not OK):
  - Input review (sources read or unavailable)
  - Plan artifact (produced or unnecessary)
  - Execution (actually doing the work)
  - Formatting (shaping the deliverable to the expected form)
  - *Collapsed form allowed*: when all four phases are OK, a single line `Trace: all OK` is sufficient. Emit phase-by-phase only when any phase is stuck or skipped. (This avoids happy-path boilerplate; the trace structure only earns its cost when something actually goes wrong.)
- **Unclear points (structured)**: for each issue, three lines:
  - Issue: <what observably happened>
  - Cause: <why, diagnosed at the instruction level>
  - General Fix Rule: <a class-level rule, not a spot fix, that would prevent this class of mistake>
- Judgment: material routine choices and their evidence; explicit assumptions; unresolved consequential decisions
- Retries: number of times you redid the same decision and why
```

The evaluator scores the fixed checklist from artifacts, observable actions, and labelled self-report. The environment reference defines how to capture available metrics; no particular tool-return field is required by this contract.

## Environment constraints

A separate session or fresh agent can supply an executor. If one selected environment is unavailable, complete independent checks and report that cell as unavailable with the reason. A self-reread remains static review, never a substitute execution result. Structural review needs no executor and does not count toward empirical convergence.

## Iteration stopping criteria

- **Convergence (tuning mode only)**: use a declared stopping rule; the following is a starting heuristic, not a model-independent guarantee. Require all critical items to pass in every supported environment before calling the result converged. For 2 consecutive rounds:
  - New unclear points: 0
  - No requirement regression; accuracy improvement vs previous is between 0 and +3 percentage points
  - Comparable operation-count variation vs previous: within ±10%, when measured
  - Comparable duration variation vs previous: within ±15%, when measured; record unavailable metrics rather than treating them as stable
  - **Overfitting check**: at convergence judgment, add 1 hold-out scenario not used so far and evaluate. If accuracy drops 15 points or more from the recent average, overfitting. Go back to baseline scenario design and add edges.
- **Divergence (suspect the design)**: if new unclear points do not decrease across 3+ iterations → the design direction of the prompt itself may be wrong. Stop fixing by patches and rewrite the structure
- **Resource cutoff**: stop when importance and improvement cost no longer balance (the "ship at 80 points" call)

## Failure pattern ledger

Maintain a cumulative list of failure modes across iterations. Without it, each iteration re-discovers the same class of mistake, and accuracy improvements stall without the operator noticing that the same `General Fix Rule` keeps surfacing under different surface wording.

Entry format:

```
- **Pattern name**: short descriptive handle (not "ambiguous X"; prefer "over-eager template application when skip clause is absent")
  - Example: <representative Issue wording from some iter>
  - General Fix Rule: <the class-level rule from that iter's structured reflection>
  - Seen in: iter N, iter M, ...
```

Rules:
- Before generating a fix in Workflow step 5, scan the ledger. If the current `General Fix Rule` matches an existing entry, update `Seen in` and investigate why the existing fix did not prevent recurrence (wording ambiguity? position too late in the prompt? missing example?) before creating a new entry.
- A pattern that recurs 3+ times despite targeted fixes is a structural signal — escalate to the "Divergence" criterion above rather than continuing to patch.
- The ledger is per-target-prompt, not global across all shiranui-hansode runs.

## Variant exploration (optional, plateau-breaking)

When iterations approach a plateau but convergence criteria (2 consecutive clears) are not met, suspect local optimum and run a 2-variant round:

- **Conservative variant**: current prompt + next-best minor fix
- **Exploratory variant**: current prompt with one structural change — reorder sections, split a dense paragraph, drop a redundant section, or add a missing scaffolding (e.g., a worked example)

Run fresh executors on identical scenarios in isolated fixtures, concurrently only when supported. Reject critical regressions in any supported environment. Among qualifying variants prefer higher requirement achievement, fewer evidenced defects, then lower comparable cost. If only one environment improves, report the split result and retain the common version unless the others preserve quality and boundaries; isolate a proven tool-specific need in a thin adapter.

Pairwise-comparison caveats:
- Do **not** ask an executor to rate "A vs B" directly. LLM position bias and self-preference bias make such judgments noisy at small n.
- Compare on the objective axes only (accuracy, operation count, unclear-points count, phase-weakness counts). Keep their capture methods fixed and repeat uncertain comparisons; small samples do not establish reproducibility.
- If qualitative comparison is genuinely needed, counterbalance: run both orderings (A,B) and (B,A) and accept a verdict only if both orderings agree.

Cost: variant exploration doubles dispatch count per iteration. Use when plateau is suspected, not by default.

## Presentation format

Record and present to the user with the following form at each iteration:

```
## Iteration N

### Environment and scope
<Mode, target revisions, tool/model versions, reasoning settings, permissions, fixture, capture source, unavailable cells, and resource limit>

### Changes (diff from previous)
- <one-line fix content>
- Pattern applied: <pattern name from ledger, or "(new)">

### Execution results (per scenario)
| Scenario | Success/Failure | Accuracy | operations | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| A | ○ | 90% | 4 | 20s | 0 | — |
| B | × | 60% | 9 | 41s | 2 | Execution |

### Structured reflection (newly surfaced this time)
- <Scenario B>: [critical] item N is × — <one-line reason for drop>
  - Issue: <what observably happened>
  - Cause: <why, at the instruction level>
  - General Fix Rule: <class-level abstraction>
- <Scenario A>: (nothing new)

### Judgment and assumptions (newly surfaced this time)
- <Scenario B>: <fill-in content>

### Ledger updates
- Added: <pattern name> (from Scenario B)
- Re-seen: <pattern name> (originally iter K) — existing fix did not prevent recurrence because <reason>

### Next fix proposal
- <one-line minimum fix>

(Convergence check: X consecutive clears / Y rounds remaining to stop condition)
```

## Red flags (beware of rationalization)

| Rationalization that surfaces | Reality |
|---|---|
| "A self-reread proves the change works" | static review cannot establish execution behavior; use a fresh executor for that claim |
| "Every edit needs the full suite" | select affected and boundary cases; expand where differences or failures justify the cost |
| "One clean run proves reliability" | report its limited coverage; tuning convergence and bounded comparison are different claims |
| "Let's knock out multiple unclear points at once" | You lose track of what worked. One theme per iteration. |
| "Split each related micro-fix strictly into its own iter" | Trap in the opposite direction. "One theme" is a semantic unit. 2-3 related micro-fixes can be bundled into 1 iter. Splitting too far explodes the iter count. |
| "Metrics are good, so ignore qualitative feedback" | Time reduction can also be a sign of being too thin. Keep qualitative primary. |
| "Rewriting from scratch is faster" | Correct if unclear points do not decrease across 3+ iterations. Before that stage, it is escape. |
| "Let's reuse the same executor" | It has learned the previous improvements. Always dispatch a new one. |

## Common failures

- **Scenario too easy / too hard**: neither produces signal. One at the median of real use, one edge
- **Only looking at metrics**: chasing only time reduction strips important explanations and makes it fragile
- **Too many changes per iteration**: you can no longer trace "which fix back then worked". One fix per iteration
- **Tuning scenarios to match the fix**: making the scenario side easier just to make unclear points look eliminated → putting the cart before the horse

## Related

- `shiranui-hanten` — use it to build or restructure a skill. Its Step 6 (Validation & verification) can hand off here for an explicitly requested review, comparison, or tuning scope.
