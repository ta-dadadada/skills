# Software Design

Use these criteria when designing, implementing, or reviewing software. Apply them to the project's purpose, language, scale, conventions, and available evidence; principle names alone do not justify a change.

## Concepts and responsibility

Keep a central concept's data and meaningful behaviour together, with an identifiable responsibility. Methods are a useful expression of domain operations when appropriate to the language; cohesive functions and modules are also legitimate. A data-only model or pure function is not a defect by itself. Split oversized concepts by distinct roles and reasons to change when the scale warrants it; avoid mandatory DDD stereotypes or universal bans on direct state changes.

Identify where each relevant rule is defined and enforced within its context. Distinguish malformed-input validation, use-case preconditions, domain invariants, and persistence/concurrency guarantees. Check known in-scope entry points for missing enforcement; label external or unverified paths rather than claiming coverage. Defensive checks can echo a rule without being independent business policies.

## Likely changes and information hiding

Aim for OCP along likely change patterns, not every imaginable extension. Ground likelihood in requirements, existing variants, repeated same-reason edits, or relevant history; mark predictions without evidence as hypotheses. Choose which boundary contains each change and weigh the cost of touching existing code against the machinery needed to avoid it. A local switch can be appropriate; repeated changes across a stable core warrant investigation, not an automatic polymorphism mandate.

Implement today's needs simply while hiding details callers need not know. Even one implementation can justify an interface or seam for current information hiding, substitution in tests, or a project convention. Do not build future variants, factories, registries, or plugin systems solely on speculative demand.

When a changeability decision needs a concrete check, name a representative likely change and list the files it would add or edit without implementing it. Evaluate their responsibilities and why changes propagate, not merely the file count. Include related documentation when one knowledge change requires coordinated edits.

## Commonization and simplicity

Commonize based on shared meaning, change intent, and change timing, not textual similarity. Even a shared rule does not automatically require a cross-module implementation: separate simple implementations can be preferable when sharing introduces incidental branching, coupling, or coordination. Make the scope of each rule explicit and weigh divergence risk against these costs. Never use intentional duplication to excuse a demonstrated inconsistency with an actual requirement.

Require useful effects from layers, wrappers, interfaces, and responsibility splits. Consider the effort to follow a behaviour across components as well as local readability. Prefer APIs that expose meaningful operations without undocumented call ordering or implementation knowledge. Use types to express meaning and constraints where useful, without requiring a Value Object for every primitive.

## Project structure and conventions

Respect the project's declared architecture and existing conventions; distinguish declarations from inferred habits. Feature-first and layer-first layouts are both valid. Names and placement should consistently reveal conceptual groupings, responsibilities, and boundaries. Flatness, technical grouping, or a name such as Service is not sufficient evidence of a problem.

Do not impose Clean Architecture or dependency inversion on a project that has not adopted them. Where a convention perpetuates a concrete problem, explain the benefit and cost of a bounded alternative. Neither following nor departing from existing code is automatically correct.

## Transactions and side effects

Consider keeping transaction control with the caller coordinating multiple operations, while hiding the details that follow a domain operation. Recording a domain event in a model and delivering it through common infrastructure after successful transaction completion is one possible separation, not a required architecture. Distinguish recording an event from performing external I/O. Evaluate failure, rollback, retries, duplicates, and concurrency where they affect the requested behaviour; do not invent delivery or consistency requirements.

## Verification

Assess unit-test ease alongside existing integration, contract, and end-to-end coverage. A seam for isolated testing is an option, not an obligation when broader tests reliably cover the relevant behaviour. Do not demand a test tier or reject a suite solely because of its composition.

Name the failures a test can detect and any actual gaps. Persistence, protocol, and concurrency claims need evidence appropriate to those behaviours. Distinguish inspecting a test from running it, and passing tests from proof of untested behaviours. Balance confidence, execution/maintenance costs, and design complexity.

## Evidence and recommendations

For every recommendation explain the observed structure, its concrete consequence or evidenced change scenario, the proposed improvement, its benefit, and its cost or conditions. Personal preference and principle compliance alone do not qualify. Consider why retaining the current design may be reasonable. Keep uncertain assumptions visible; do not invent business rules to complete an analysis.
