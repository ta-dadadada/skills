# Validation record

## Responsibility split — 2026-09-05

Validated with `shiranui-hanten`. Findings: the former skill mixed design,
implementation recipes, and runtime evidence; its implementation branch is now
an explicit handoff. Small-change intake and discoverable menus remain supported.

- Job/layer: a frontend agent produces and reviews a UI design contract; domain layer.
- Completion: a coherent scoped design and acceptance cases are delivered;
  requested code continues to the implementation companion with the same contract.
- Invocation: model-invoked. New/changed UI and domain handoffs enter design;
  working-UI requests continue through Step 5. Settled-design coding routes out.
- Ownership: design requirements live here, concrete HTML/ARIA/CSS/JS and runtime
  review in `frontend-ui-implementation`, business structure in `business-ui-design`.
  Handoff fields have one authoritative home in `references/handoff.md`.
- Pruning: retained surface/state/visual decisions, replaced concrete table recipes
  with requirements, separated design review from measured runtime outcomes.

## Fresh representative execution

Run first, before implementation and business trials. Executor: `gpt-5.6-terra`,
`medium`, fresh context. Task: a design-only Copy book link action in an existing
Book actions menu, with success feedback and manual-copy recovery on failure.

Observed artifact and executor-reported operation order: read SKILL and triggered
references → create the specification → read the complete artifact with `sed` →
report findings and limitations. A compact scope statement replaces a full intake
questionnaire. The menu stays the GUI route; the contract covers failure recovery,
list context, keyboard/focus and accessibility outcomes. The executor did not
read or invoke the implementation skill and wrote no application code.

The artifact included a design-review table at creation; the executor subsequently
read it and checked its claims against the contract, finding no contradiction.
Only that subsequent inspection supports the reported review. Source access,
actual focus/announcement behavior, narrow layout and zoom remained explicitly
unverified. The artifact contains requirements rather than ARIA recipes.

## Earlier evidence and limits

Earlier two-skill trials informed proportional intake, value/commit events, and
post-artifact inspection. They do not verify the new implementation boundary.
The later business-chain trial exposed concrete ARIA/CSS choices in the shared
design record. Handoff guidance was clarified to separate requirement outcomes
from later implementation notes; the executor applied that focused correction.
The business trials also exposed skipped pre-code artifact inspection. The design
workflow now explicitly places it before implementation. The Terra small-change
follow-up still omitted that boundary and is recorded as nonconforming evidence
in the business validation record, rather than counted as a pass. A fresh
Sol/medium new-queue run subsequently wrote the design, read it separately for
review, and only then wrote code. An unnecessary restriction on early reference
loading was pruned: contract review precedes code; feasibility reading can happen
earlier. These results establish one successful trajectory, not model-independent
reliability.
This representative run assesses design procedure, not runtime accessibility or
the correctness of every possible generated design.

## Mechanical and placement checks

- `python3 meta/shiranui-hanten/scripts/validate_skill.py dev/frontend-ui-design` passed.
- The full `dev/* meta/*` validator passed for all 18 packages.
- `git diff --check` and explicit whitespace checks covering new files passed.
- Names match canonical directories. Both `.agents/skills/` and `.claude/skills/`
  links resolve to the canonical packages. Root README/APM include all three skills.
- Description triggers match workflow branches. Full linked-file review and
  pruning found no embedded credentials or internal endpoints.
