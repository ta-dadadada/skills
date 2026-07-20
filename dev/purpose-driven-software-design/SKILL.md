---
name: purpose-driven-software-design
description: >-
  Purpose-first design workflow for software changes that involve a design
  decision — introducing or relocating a rule, responsibility, state
  transition, dependency, abstraction, or axis of variation — not for
  every behaviour change: clarify whose problem the change solves, pin
  ambiguous domain terms, discover the existing design and the evidenced
  axes of change (Follow / Adapt / Avoid), give every rule an authoritative
  owner, choose the smallest sound extensible structure — open along
  evidenced axes, closed against hypothetical ones — map each behaviour to
  the cheapest test level, review changeability. Applies to APIs, event
  handlers, batch jobs, CLIs, frontend, and domain logic alike. Use when
  deciding where data and logic belong, when a new
  variation keeps forcing edits to the same core code, when introducing or
  resisting an abstraction or commonization, or when reviewing a change for
  changeability. Not for purely mechanical changes, nor required for small
  local changes that fit the existing design as is.
license: MIT
metadata:
  author: tadaair
---

# Purpose-Driven Software Design

Code, classes, functions, modules, and abstractions are means, never the goal: a change starts from whose problem it solves and which state it makes true, and structure follows that purpose. Data and logic sit where their purpose and responsibility place them, and every rule has one authoritative owner — extra boundary checks and storage constraints are defense-in-depth, while a second independent definition of the same rule is a split specification. The project's existing conventions are the default; a deviation is justified only where the convention would reproduce a known correctness, security, or changeability problem, and it stays as small as its reason. The structure is open along axes of change backed by evidence and closed against hypothetical ones — the measure of the design is what the next change costs.

## When to use

- Changes that introduce or relocate a rule, responsibility, state transition, dependency, abstraction, or axis of variation — in APIs, event handlers, batch jobs, CLIs, frontend, or domain logic — especially when deciding where new data and logic belong.
- Adding a variation of existing behaviour (a new type, provider, policy, channel), especially when the last such addition forced edits across the same set of files.
- Introducing, or resisting, an abstraction or a commonization; reviewing a finished change for changeability.

## When not to use

- Purely mechanical changes that alter no behaviour and no structure: tool-applied renames, formatting, comment edits, dependency housekeeping.
- Small, local changes that fit the existing design as is — no new rule, responsibility, boundary, or placement decision to make.

## Workflow

### Step 1 — Clarify the purpose

- Name the actor and the problem: whose problem does this change solve, and what state counts as success — which behaviour becomes possible after the change that is impossible now.
- Name the non-goals: what this change deliberately leaves untouched.
- Pin every ambiguous domain word to one meaning, and split any word the request or the codebase uses in two senses; record the constraints the change must satisfy.
- State the change as behaviour to realize, in domain terms. Structure — classes, interfaces, tables, endpoints, components — is chosen in Step 4, after purpose, rules, and axes are on the table.

**Done when:** actor, problem, success state, non-goals, constraints, and the pinned domain terms are written down, and the change is described as behaviour to realize rather than as structures to build.

### Step 2 — Discover the existing design

- Trace the relevant execution paths end to end — entry point to side effect — and map the modules, data, and dependencies they cross; read the closest existing implementation of a similar purpose.
- Anchor the trace to the code that is actually wired and built: follow what the router, schema, or entry registration binds, and confirm the path compiles. Treat duplicated, unreachable, or non-compiling definitions of the same symbol as artifacts to record for cleanup, not as live execution paths — name them as such rather than reasoning about the design as if they run.
- Record where each relevant invariant and state transition is enforced today, where the same knowledge is duplicated, and where responsibilities pool into catch-all homes (Handler, Service, Manager, Util, Common) or into purely technical groupings that hide purpose.
- Classify each pattern you will touch: **Follow** (adopt as is), **Adapt** (minimally adjust for this purpose), **Avoid** (reproduces a concrete correctness, security, or changeability problem — name the problem; taste and general principle do not qualify).
- Identify the axes of change — where variation actually arrives — from evidence: multiple existing implementations, the same type/kind/status/provider/mode branch repeated across sites, git history and issues showing repeated same-reason edits, explicit requirements, per-configuration differences, multiple external integrations. Record each axis with its evidence; an axis with no evidence is a hypothesis and is recorded as one, not treated as a requirement.
- Separate what the evidence shows to be stable — settled requirements, explicitly closed sets, deliberately fixed flows, code that stayed unchanged across relevant variations — from what changes often. Lack of edits alone is not evidence of stability: untouched code may be avoided, fragile, effectively abandoned, or simply never asked to change.

**Done when:** the relevant execution paths, responsibilities, and dependencies are mapped; every pattern to touch carries a Follow / Adapt / Avoid verdict (Avoid with its concrete problem); and the stable core and the evidenced axes of change are named, each axis with its evidence.

### Step 3 — Define rules and ownership

- Write down, for the Step 1 behaviour: valid and invalid states, permitted and forbidden transitions, invariants, pre- and postconditions, what must hold after a mid-flight failure, and the expected behaviour under retry, concurrency, and duplicate execution.
- Distinguish the kinds of check: boundary validation that rejects malformed input, use-case preconditions, domain rules that keep invalid states out, and constraints only persistence or concurrency control can guarantee (uniqueness, ordering, atomicity).
- Give each rule one authoritative owner — the component that defines it. Layered defense is welcome: a boundary may pre-check for early feedback and the database may constrain as the last barrier, each echoing the owner's rule. Two independent definitions of one rule are a split specification.
- Choose the vehicle the project's language and design offer — module, function, type, class, schema, algebraic data type, database constraint; no single mechanism is mandatory.
- Confirm every known in-scope write path crosses the owner — a rule that a second entry point can bypass has no owner yet. Record external, unknown, or unverifiable write paths (other repositories, external services, legacy batches, manual operations, direct DB updates) explicitly rather than claiming coverage over them.

| Per rule | Question the design must answer |
|---|---|
| Guarantee | what does the rule keep true? |
| Owner | which component defines it? |
| Coverage | does every known in-scope entry point cross the owner, and are unverifiable paths recorded? |
| Echoes | where do defensive pre-checks and storage constraints sit? |
| Change | what gets edited when the rule changes? |

**Done when:** each rule and invariant answers the five questions above with one authoritative owner; boundary validation, use-case preconditions, domain rules, and persistence constraints are distinguished; no known in-scope entry point bypasses an owner; and external or unverifiable write paths are recorded as such, with coverage claimed over nothing unverified.

### Step 4 — Choose the smallest sound and extensible design

- Put data and the logic serving the same purpose together; keep what changes for the same reason together and what changes for different reasons apart. Similarity of shape is not a reason to share code — shared purpose and shared reason to change are.
- Separate the stable core from volatile policy: judgments that vary — pricing, notification, provider selection, business policy — sit behind a seam, and the settled flow stays put. Place each piece where name and location reveal its purpose; a catch-all module (Common, Util, Helper, Manager) is a location of last resort.
- Open the design exactly along the Step 2 evidenced axes: adding the next variation on such an axis should mean adding code at the seam, not editing the same branch in several files again. Use whatever the project favours — functions, modules, composition, strategy, data-driven dispatch, polymorphism; no mechanism is mandatory, inheritance included.
- Keep simple conditionals where they are right: closed sets, local decisions, differences with no evidence of growth. The structure to remove is the same branch replicated across sites and growing with every new kind — the branch itself is not the enemy.
- With one concrete implementation and no evidenced axis, build no interface, factory, strategy, registry, or plugin machinery; keep any mechanism scoped to what this change needs. The cost of understanding an abstraction must stay below the change cost it avoids.
- Deviate from the existing structure only within an Avoid verdict's reason from Step 2, no wider.
- Before implementing, answer for the chosen design: the stable core; the axes; the files the next variation on each axis adds or touches; the evidence behind each seam; the change risk the simpler design would keep; the complexity the more abstract design would add; why this is the smallest design that satisfies today's requirement.
- Keep the record proportional to the decision: a local change introducing no new abstraction and touching no evidenced axis needs only a brief statement of placement, owner, and why the existing design absorbs it; the full comparison above is for introducing a seam, abstraction, shared component, or new responsibility boundary. The questions get answered either way — briefly or in full, never skipped.

**Done when:** the chosen design names its stable core and its evidenced axes; the next variation on each axis lands as local additions rather than repeated edits to the core; every seam carries evidence; both the simpler and the more abstract alternative have been weighed and declined for stated reasons; and the record's depth matches the decision's weight — brief for local placements, full for new seams and boundaries.

### Step 5 — Map behaviour to verification

- Give every behaviour, rule, and invariant from Step 3 a named verification, placed at the cheapest level that reliably catches its failure — the level is chosen by what the failure is, not by convention or test-pyramid slogan.
- Domain rules test where their owner lives; protocol, serialization, and middleware behaviour tests at the boundary; uniqueness, transactions, and locking test against real persistence; external integrations get contract or integration tests; the few critical user paths get end-to-end or real-operation checks.
- Let each test answer: which failure does it catch, and is this the cheapest reliable place to catch it? A suite that is all end-to-end and a suite that is all unit tests both fail that question somewhere; so does verifying one behaviour identically at several levels — an owner-level test plus a thin boundary echo usually suffices.

**Done when:** every behaviour, rule, and invariant maps to a named verification with the failure it catches and the reason for its level; boundary, domain, persistence, and integration failures are each caught where they occur.

### Step 6 — Review changeability

- After implementing, name where the next plausible spec change lands, and confirm: one rule change edits its owner plus echoes, not a scatter of copies; each piece of knowledge appears once; no known in-scope entry point bypasses an owner (unverifiable paths stay recorded, not assumed covered); each module holds one reason to change; nothing is commonized on looks alone.
- Confirm placement and naming reveal purpose, deviations from convention stayed as small as their reasons, and no migration scaffolding has quietly become permanent ambiguity.
- Run the extension probe: pick one representative next variation on each evidenced axis — name it, do not build it — and list the files it would add and the files it would edit. Local additions at the seam pass; repeated edits across the stable core mean the seam missed the axis, and the mismatch is either fixed or accepted with a recorded reason.
- Weigh each abstraction introduced: it is justified by today's evidence, and its understanding cost stays below the change cost it removes; an abstraction that outgrew its problem gets folded back into the simpler form.

**Done when:** the extension probe's file list shows local additions rather than core-wide edits (or the exception carries a recorded reason); each rule's owner, the stable core, and the seams are nameable; and every introduced abstraction carries evidence and pays for itself.

## Red flags

| Rationalization | Reality |
|---|---|
| "The neighbouring code does it this way, so it's right" | convention is the default, not proof of sound design; a pattern with a named correctness, security, or changeability problem stays out of new code |
| "Best practice says restructure this" | deviation from the existing structure needs a concrete problem in this change, not a general ideal |
| "The handler / the UI already validates it" | a rule enforced at one entry point vanishes when another path writes the same data; the owner sits where the known write paths cross, and unverifiable paths are recorded, not assumed covered |
| "The DB constraint makes domain design unnecessary" | storage constraints are the last barrier, not the authoritative owner of business intent and state transitions |
| "The same check in several places makes it safe" | echoes of one owner are defense-in-depth; two definitions of one rule are a split specification |
| "These look the same, so share the code" | commonize on shared purpose and shared reason to change, not on shape |
| "We'll likely need it later, so abstract now" | a hypothetical future is not evidence; axes come from existing variants, repeated branches, change history, and stated requirements |
| "OCP, so add an interface / make it polymorphic / make it a plugin" | mechanisms are means; a seam that matches no evidenced axis adds complexity, not changeability |
| "It's one more case in the switch" | when each addition edits the same branch in several files, the axis has already appeared — this addition is the moment to separate it |
| "The existing code is untouched, so OCP is satisfied" | the goal is not frozen code but a core that stops absorbing repeated same-reason edits |
| "Conditionals violate OCP, remove them all" | closed sets and local decisions are well served by a plain branch; the smell is the replicated, growing branch |
| "Integration tests cover everything" | boundary, domain, persistence, and integration failures are caught cheapest at different levels |
| "Too small a change to design" | a new rule or reason to change placed in the wrong home is debt at any size |

## Related

- `backend-api-implementation` — the API-contract instantiation of this workflow: fixing the input/output contract, contract-first tests, real-request verification. This skill decides where rules and logic live and where the structure opens; pair it with the implementation skill for the surface being built.
