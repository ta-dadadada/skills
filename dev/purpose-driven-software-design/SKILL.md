---
name: purpose-driven-software-design
description: >-
  Design software changes and review software structure using shared criteria
  for responsibility, change locality, information hiding, simplicity, and
  verification. Use when deciding where rules or logic belong, introducing or
  evaluating abstractions and commonization, adding variations, or reviewing
  a diff or an explicitly named whole scope for design and maintainability.
  Design produces a reasoned structure and verification plan; review produces
  evidence-backed proposals without editing. Applies to APIs, events, batches,
  CLIs, frontend, and domain logic. Not a comprehensive bug, security, or
  performance audit. Routine mechanical or locally conventional changes do not
  need this workflow unless design review is explicitly requested.
license: MIT
metadata:
  author: ta-dadadada
---

# Purpose-Driven Software Design

Design and evaluate structure by the purpose it serves and the cost of plausible changes. Both routes use the same [design principles](references/design-principles.md); read them before making design judgments. Keep working notes proportional to the decision. Report evidence, assumptions, and unexamined scope distinctly.

## When to use

- Decide placement of rules, responsibilities, state transitions, dependencies, or abstractions.
- Add variations or assess commonization and changeability.
- Review a change or an explicitly specified whole target for software design and maintainability.

## When not to use

- Routine mechanical changes or small changes absorbed by existing conventions, unless explicitly asked to review their design.
- A comprehensive correctness, security, or performance audit. Report concrete defects encountered, but do not claim audit coverage.
- Establishing an unfamiliar business domain from scratch; use `domain-modeling` when that is the actual task.

## Workflow

### Route and scope

Choose **Design** when asked to decide a structure, and **Review** when asked to evaluate existing or proposed code. Reuse the established purpose and constraints rather than restarting discovery. A review request does not authorize edits. If implementation or fixes are also explicitly requested, finish the review and then continue that authorized work; review completion does not cancel the wider task.

For a diff, identify its comparison base and account for the changed files, reading the surrounding implementations, callers, tests, and documents needed to judge them. For an explicitly requested whole-target review, inventory and read every in-scope source, test, and document rather than sampling only the diff. State excluded generated/vendor/binary material and unavailable or unread files; incomplete coverage must remain visible. Resolve material scope ambiguity from context, or ask if it cannot be resolved.

### Shared discovery

- Establish the actor, behaviour, constraints, and non-goals relevant to the task. Do not invent business requirements from current code.
- Read project rules, architecture guidance, and the closest relevant implementations. Separate declared conventions from inferred patterns.
- Trace relevant wired execution paths from entry to effect; identify rule definitions and enforcement, responsibilities, dependencies, and existing tests. Do not treat dead or duplicate definitions as active paths. Verify build/runtime claims only when needed and possible, and state what was actually checked.
- Identify evidenced axes of change and what is stable within the relevant scope. Lack of edits alone does not establish stability. Use history when it resolves a specific uncertainty rather than requiring a repository-wide investigation.

**Done when:** the scope, relevant behaviour and structure, conventions, change evidence, and material unknowns are identified sufficiently to support the selected route.

### Design

1. **Define responsibilities and guarantees.** For each relevant rule or transition, name its scope, definition and enforcement locations, known entry paths, defensive checks, and what changes when the rule changes. Consider invalid states, failure, retry, concurrency, and duplicate execution where relevant. Record unverified paths explicitly.
2. **Choose a proportionate structure.** Apply the shared principles to placement, boundaries, reuse, and representation. Explain what to follow, adapt, or avoid in existing patterns, with a concrete reason for deviations. For a new abstraction or shared component compare retaining the simpler structure and adding the proposed boundary, including benefits and costs. A local placement needs only a brief explanation.
3. **Probe changeability.** For the evidenced axes, use the extension probe in the shared principles. Explain remaining coordination costs or accepted tradeoffs. If no axis is evidenced, do not invent a future feature just to perform this step.
4. **Map verification.** Map the relevant behaviours and guarantees to existing or proposed checks, identifying what failures they cover and what remains unverified. Reuse sufficient existing coverage; justify new checks or testability seams by their benefit.
5. **Deliver or continue.** Present the chosen responsibilities, boundaries, tradeoffs, verification plan, and unresolved decisions. If implementation was requested, proceed within that scope and check the resulting implementation against these decisions and the extension probe; otherwise stop at the design.

**Done when:** the design explains where relevant rules and behaviour belong, why its complexity is justified, how likely changes land, how behaviour will be verified, and what remains uncertain. Any separately requested implementation still has its own completion criteria.

### Review

1. **Evaluate the actual target.** Use the shared discovery and principles against the diff and relevant context, or the entire explicitly requested scope. Review responsibilities, change propagation, information hiding, reuse, structural consistency, API simplicity, and verification as applicable. Mark irrelevant criteria rather than manufacturing findings.
2. **Challenge candidate findings.** Check surrounding safeguards, conventions, independent change contexts, and existing test coverage. Consider retaining the current structure. For future-change arguments, name the change, its evidence, and the files/responsibilities affected. Discard taste-only claims and speculative extensions.
3. **Report proposals.** Consolidate findings with the same cause and order by concrete impact. Distinguish issues introduced or worsened by the change from existing improvement opportunities relevant to it. Do not expand an ordinary diff review into an unrelated repository audit. Do not edit or prescribe merge blocking solely because a design alternative exists.

Each finding includes:

- Location and observed structure, with source evidence.
- Concrete impact or evidenced likely-change scenario.
- Proposed improvement and its expected benefit.
- Added complexity, tradeoff, or conditions under which retaining the current structure is reasonable; uncertainty where applicable.

Finish with scope/coverage and verification limits. State that no actionable design findings were found when appropriate; there is no finding quota. Do not imply tests ran merely because they were read.

**Done when:** the requested scope has been assessed (or missing coverage disclosed), each retained finding has evidence, benefit, and tradeoff, and the report distinguishes current-change findings, relevant existing opportunities, and unknowns. Review-only work ends with proposals, not implementation or a mandatory redesign.

## Red flags

- A review silently proceeds into implementation or full redesign.
- An alternative is recommended only because a principle or preferred architecture names it.
- Shared criteria are copied into route-specific rules and begin to disagree.
- Reading a sample is reported as reviewing an explicitly requested whole target.
- Speculative future variations are treated as confirmed requirements.

## Related

- [Shared design principles](references/design-principles.md) — authoritative judgment criteria for both routes.
- `domain-modeling` — establishes business meanings and rules when that is the requested task.
- `backend-api-implementation` — implements API contracts when implementation is authorized.
