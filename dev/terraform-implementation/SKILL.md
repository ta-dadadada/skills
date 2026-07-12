---
name: terraform-implementation
description: >-
  Blast-radius-first workflow for implementing a change in an existing
  Terraform codebase: discover the project's conventions (layout, state
  boundaries, naming, pinning, checks), predict every touched resource's
  plan action (create / update in-place / replace / destroy) before writing
  code, implement following those conventions, verify with fmt + validate +
  the project's configured linters, hand off the diff with the prediction.
  terraform plan runs only when explicitly instructed. Provider-agnostic.
  Use when adding, changing, renaming/moving, or removing resources, data
  sources, modules, variables, or outputs in existing Terraform code. Not
  for designing a new stack from scratch (backend, state layout, directory
  strategy) or for operating infrastructure (apply, destroy, state
  surgery).
license: MIT
compatibility: >-
  Step 4 runs the terraform CLI and the project's configured linters —
  locate tools via PATH or the project's version manager; a check whose
  tool cannot be located is recorded in the handoff.
metadata:
  author: tadaair
---

# Terraform Implementation

Every edit to Terraform code is a proposal against live infrastructure: the same small diff can be a harmless in-place update or a destroy-and-recreate of a production database. So the blast radius — the plan action expected for every touched resource — is predicted before any code is written, and every later step answers to that prediction. The project's existing conventions are the default for layout, naming, and pinning; a deviation is justified only where the convention would reproduce a known correctness, security, or changeability problem, and it stays as small as its reason. The change is done when it passes the project's configured checks and the handoff states the predicted blast radius — `terraform plan` itself runs only when explicitly instructed.

## When to use

- Adding, changing, or removing resources, data sources, modules, variables, or outputs in an existing Terraform codebase.
- Renaming or moving resources and modules — refactors where state must follow the code.

## When not to use

- Designing a new stack from scratch — backend, state layout, and directory/environment strategy are settled before this skill applies.
- Operating infrastructure: apply, destroy, or state surgery (`terraform state rm`/`mv` against live state). Adopting existing resources via `import` blocks in code is in scope; imperative operations are not.
- Non-Terraform IaC (CloudFormation, Pulumi, CDK).

## Workflow

### Step 1 — Discover the project's conventions

- Map the layout: where deployable root modules live versus shared modules, how environments are separated (directories, workspaces, tfvars), and which root module(s) the requested change lands in.
- Read one or two existing resources or modules closest in shape to the change, end to end: naming, tagging, variable/output style, provider and module version pinning. Flag any pattern you will deliberately keep out of the new code — one carrying a known correctness, security, or changeability problem — with its reason.
- Record the configured checks and their commands: fmt, validate, linters and policy scanners (tflint, checkov, conftest, …), CI jobs — Step 4 runs these. Record where plan and apply execute for this repo (CI, Atlantis, Terraform Cloud, locally) — Step 5's handoff is written for that pipeline.

**Done when:** you can name, with file paths, the target root module(s), the naming/tagging/pinning pattern to follow, the configured checks with their commands, and where plan/apply executes.

### Step 2 — Predict the blast radius

- Map the requested change onto concrete resources and modules. For each touched resource, record the expected plan action — create, update in-place, replace, or destroy — with the reason. When an argument's change behaviour is unclear, consult the provider's resource documentation (fields marked "forces replacement") rather than guessing.
- Express every rename and move as a `moved` block, and every adoption of existing infrastructure as an `import` block, so state follows the code.
- Inventory the consumers of anything whose interface changes: other modules and root modules referencing the changed variables or outputs, and `terraform_remote_state` or data-source readers in the repo. Record consumers you cannot verify — other repositories, out-of-band readers — as unknown; a purely additive change (a new variable with a default, a new output) needs only the known-consumer check. State per known consumer whether the change is compatible; an incompatible change, or a breaking change with an unknown population, gets an explicit migration decision before you proceed.
- A predicted replace or destroy of a stateful resource — databases, storage, queues, anything holding data — requires the user's explicit confirmation before implementation proceeds.

| Concern | Question the prediction must answer |
|---|---|
| Plan action | for each touched resource: create, update in-place, replace, or destroy — and why? |
| State moves | is every rename/move expressed as a `moved` block, every adoption as an `import` block? |
| Stateful resources | does any replace/destroy hit a data-holding resource, and has the user confirmed it? |
| Interface compatibility | does every consumer of changed variables/outputs keep working, or is a migration decided? |
| Environments | which environments does the change reach — and is that exactly the set requested? |
| Secrets | do credentials and sensitive values stay out of code, entering through the mechanism the project already uses? |
| Pinning | are new providers and modules pinned the way the project pins them? |

**Done when:** every touched resource has a predicted action with a reason, every move is listed as a `moved`/`import` block, every table row has a verdict (addressed, or not applicable with a reason), consumers are inventoried with unknowns recorded, and any stateful replace/destroy carries the user's confirmation — or none is predicted.

### Step 3 — Implement

- Write the change following the Step 1 record — the same layout, naming, tagging, and pinning as the neighbouring code; where a neighbour's pattern was flagged in Step 1, deviate minimally and record why.
- Add the `moved` and `import` blocks from Step 2 alongside the resource changes they describe.
- Route per-environment values through the project's existing mechanism (tfvars, workspace, module arguments); shared code stays environment-neutral.
- Keep the diff scoped to the Step 2 prediction: version bumps, refactors, and cleanups beyond the requested change widen the blast radius and belong in their own change.
- When implementation reveals a gap in the prediction — an extra resource touched, a different plan action — re-enter Step 2 and update the prediction before the code.

**Done when:** the diff implements exactly the Step 2 prediction — every predicted touch present, nothing beyond it — reads like the neighbouring code, and any deliberate deviation is recorded with its reason.

### Step 4 — Verify statically

- Run the checks recorded in Step 1: `terraform fmt`, `terraform validate` (after `terraform init -backend=false` when the working directory is uninitialized or backend credentials are absent), and the project's linters and scanners.
- Leave init byproducts as the project keeps them: refresh a lock file the repo already tracks; remove `.terraform/` directories and lock files it does not track.
- Fix findings and re-run until green. A check that cannot run here — tool not locatable, no credentials — goes into the Step 5 handoff by name with the reason.

**Done when:** every runnable configured check passes, and every check that could not run is recorded with its reason.

### Step 5 — Hand off; plan only when instructed

- Deliver the handoff: the diff, the Step 2 blast-radius prediction (per-resource actions, consumer inventory, confirmations obtained), and the checks that could not run. This is what the human reviews the real plan output against, wherever plan executes (Step 1).
- Only when the user explicitly instructs plan execution: run `terraform plan` in the target root module(s) and compare each planned action against the Step 2 prediction, resource by resource. A planned action the prediction missed — above all an unexpected replace or destroy — means re-entering Step 2 before anything else.

**Done when:** the handoff states diff, prediction, and unrun checks; and, when plan was instructed, every planned action matches the prediction or the mismatch has been resolved through Step 2.

## Red flags

| Rationalization | Reality |
|---|---|
| "validate passed, so the change is safe" | validate checks syntax and types, not what happens to live infrastructure; the blast-radius prediction is the safety argument |
| "It's just a rename" | a rename without a `moved` block plans as destroy-and-create |
| "The plan will catch it" | plan runs elsewhere, later, reviewed by someone else; the prediction comes first, plan only confirms it |
| "While I'm here, bump the provider" | unrelated changes widen the blast radius; they get their own diff |
| "The neighbouring module already does it this way" | convention is the default, not proof of sound design — patterns flagged in Step 1 stay out of the new code |
| "Hardcode the value for this environment" | a literal in shared code reaches every environment; use the project's per-environment mechanism |
| "Nobody reads this output" | other root modules, remote-state readers, and other repositories are consumers too — inventory before changing |
| "The resource is re-creatable, destroy is fine" | whether data loss is acceptable is the user's call; a stateful replace/destroy proceeds only on their confirmation |
