---
name: domain-modeling
description: >-
  Evidence-first domain modeling workflow: fix the modeling purpose and
  scope, extract graded domain facts and vocabulary from the available
  sources, reconstruct behaviour as scenarios, commands, and domain
  events, capture business rules and invariants, derive candidate
  concepts and bounded-context candidates, challenge the model, and
  deliver a domain-model report that keeps evidence, inference,
  hypothesis, and open question distinct. Behaviour before structure;
  tactical DDD patterns only where they sharpen the model. Use when
  exploring an unfamiliar business domain, extracting a domain model
  from requirements or an existing codebase, defining ubiquitous
  language or resolving terminology conflicts, identifying business
  rules and invariants, discovering bounded contexts and their
  relationships, distilling the core domain, or reviewing an existing
  domain model. Not for deciding code structure — hand that to
  purpose-driven-software-design — and not for one-off diagram
  generation from an already-documented model.
license: MIT
metadata:
  author: tadaair
---

# Domain Modeling

A domain model is a purposeful explanation of a domain — what happens, why, under which rules, where meanings shift, and what remains uncertain — not an inventory of DDD artifacts. The workflow is evidence-first: every statement in the model carries its grade — **evidence** (confirmed, with a source), **inference** (interpretation derived from evidence), **hypothesis** (tentative, awaiting validation), or **open question** — and keeps that grade through to the report; a gap in the evidence becomes a question or a recorded assumption, never a plausible invention. Behaviour comes before structure: actors, scenarios, decisions, events, and rules are established first, and concepts, tactical patterns, and boundaries are derived from them. The deliverable is the smallest useful model, written in the domain's own language, that a reader can understand without opening the implementation.

## When to use

- Exploring an unfamiliar business domain from requirements, specifications, or conversation.
- Extracting the domain model buried in an existing system — code, database schemas, APIs, event definitions.
- Defining ubiquitous language, resolving terminology conflicts, identifying business rules and invariants, or discovering bounded-context candidates.
- Reviewing an existing domain model.

## When not to use

- Deciding where rules and logic live in code, or any other software-structure decision — that is `purpose-driven-software-design`; this skill establishes what the domain is.
- Rendering diagrams for a model already analyzed and documented — nothing left to model.

## Workflow

Two routes.

**Build** — Steps 1–7 in order. Read points: [references/tactical-patterns.md](references/tactical-patterns.md) and [references/strategic-patterns.md](references/strategic-patterns.md) before Step 5; [references/report-template.md](references/report-template.md) at Step 7. Step 3 names the one case that sends you into tactical-patterns earlier.

**Review** — for judging an existing model. Run Step 1; run Step 2 against the model's sources — on this route Step 2 is done when every distinct claim the model under review makes has at least one graded statement or glossary observation against it; read [references/tactical-patterns.md](references/tactical-patterns.md) and [references/strategic-patterns.md](references/strategic-patterns.md) — the criteria the checks judge against; apply Step 6's checks to the model under review, judging the model's claims against that evidence base — a scenario, rule, or term the model fails to supply is itself a check failure. The review deliverable, in this order:

1. Purpose and scope (Step 1)
2. Graded evidence base with glossary observations (Step 2)
3. Findings, each as observation → impact → evidence → recommendation → confidence
4. Outcomes of the five checks, summarized
5. Verdict against the review's purpose
6. Open questions ranked by impact, and recorded assumptions

The report template belongs to the build route. Within the order above the review deliverable's formatting is free, and the model under review always grades as current-implementation evidence, never as domain evidence — its absent underlying sources become open questions.

Cross-cutting rules, in force at every step:

- **Degraded mode** — when the user or a source is unreachable, a question that would have been asked converts, at whatever step it arises, into an open question at its impact rank with a graded hypothesis holding its place; a gap is high impact when its answer would change a state, rule, or boundary of the model, and every smaller gap becomes a recorded assumption.
- **Working notes** — Steps 1–6 produce working notes, kept in files or in the run's own reasoning, either of which satisfies their `Done when` criteria; what ships is the Step 7 report (build) or the review deliverable.

### Step 1 — Fix purpose and scope

- Name the purpose of the analysis — understand an unfamiliar domain, design or redesign a system, find service boundaries, define an API, resolve terminology, extract knowledge from legacy code, review a model — and evaluate every later modeling decision against it: a model is right for a purpose, not universally.
- Inventory the sources: requirements, specifications, business documents, user stories, meeting notes, source code, schemas, APIs, event definitions, operational procedures. Implementation artifacts are evidence of current system behaviour; the domain truth they suggest is graded as inference until corroborated.
- Write a scope statement naming the target domain, stakeholders, known constraints, and — explicitly — what is out of scope. Model what the purpose needs; the rest stays out.

**Done when:** the purpose, a scope statement with explicit out-of-scope items, and the source inventory are written down.

### Step 2 — Extract facts and vocabulary

- Read the sources and record the domain statements they contain: things that happen, decisions made, rules that constrain, information a decision needs, state transitions, responsibilities, exceptions, temporal constraints. Record each with its grade:

  ```text
  FACT: An applicant may withdraw an application before the process completes.
  SOURCE: Requirements §3.2        CONFIDENCE: high

  HYPOTHESIS: An application belongs to one active selection process.
  RATIONALE: The workflow consistently says "the current selection process".
  CONFIDENCE: medium               VALIDATION: confirm whether parallel processes exist.
  ```

- When the source is an existing system, mine it for terminology, state transitions, validation and conditional logic, transaction boundaries, and emitted or consumed events — and label the result the *current implementation model*, kept separate from the *proposed domain model* throughout. An existing abstraction earns its place in the proposed model by domain evidence, and a working implementation earns rewrite recommendations only from domain mismatches.
- Build the glossary: term, definition, examples, source context, confidence. This is the ubiquitous language of each context in the making — one meaning per term inside its context, and a change in the language is a change to the model. Hunt synonyms (different words, one concept — confirm equivalence before merging) and homonyms (one word, several concepts — keep them separate). Each homonym or unresolvable conflict is boundary evidence, carried to Step 5.
- Questions to the user ask about the domain, and the agent translates the answers into modeling hypotheses. Ask "can two applications for the same position coexist?" — a question about the business — and reserve "should Application be an aggregate root?" for your own Step 5 analysis. Seek concrete examples, counterexamples, edge cases, business decisions. Batch questions, ordered by impact: rules > boundaries > lifecycle and identity > terminology > implementation detail; a question that cannot be asked or answered follows the degraded-mode rule above.

**Done when:** every important statement carries a grade and a source; the glossary covers the terms the scenarios will use; synonym and homonym findings are recorded.

### Step 3 — Reconstruct behaviour

- Walk each important scenario end to end as `actor → command/intent → business decision → state change → domain event`, with its required information, governing rules, and exceptional paths. Concrete examples beat abstract descriptions.
- Name domain events in past tense for facts the business cares about — *Application Submitted*, *Offer Accepted* — and for each, record what caused it, what changed, who cares, and what may follow. Technical operations (*Database Updated*, *API Called*) enter only where the business itself assigns them meaning. When an event's record attributes, timestamps, or identity under duplicate delivery participate in a rule or scenario — a limit that counts occurrences qualifies — model it with [references/tactical-patterns.md § Domain Event](references/tactical-patterns.md#domain-event); a log that nothing reads does not.
- Trace every event back to the command or decision that produced it, with the rules that gate it; distinguish user intentions, business decisions, automated reactions, and technical actions.

**Done when:** each in-scope scenario is walked end to end including its exceptional paths, and every event traces to a command or decision with its gating rules.

### Step 4 — Capture rules and invariants

- Collect the statements that must remain true — the sources flag them with *must*, *only when*, *cannot*, *always*, *at most*, *exactly one*, *before*, *until*.
- Classify each: **precondition** (required before an action), **invariant** (holds continuously within a consistency boundary), **policy** (what happens in response to a situation), **calculation** (derives a value), **temporal rule** (time or ordering). A statement that genuinely fits two classes is recorded once, carrying both classifications and a note linking its faces — one entry, two faces. Name the concepts that participate in keeping each rule true — participation, not object containment, is what shapes aggregate candidates in Step 5.
- Investigate exceptions before simplifying: "cannot be edited after submission, except when…" — the exception is where the hidden rule lives.

**Done when:** every collected rule has a classification, its participating concepts, a grade, and a source.

### Step 5 — Derive concepts and boundaries

- Derive candidate concepts from the vocabulary, commands, events, rules, and state transitions. Give each a responsibility in domain terms — "represents a candidate's participation in the hiring process", where "stores application data" describes only persistence. Lifecycle words in the sources (*draft*, *submitted*, *approved*, *cancelled*) mark concepts whose state machine is worth modeling.
- Classify a candidate as Entity, Value Object, Aggregate, or Domain Service only where the pattern sharpens the model — criteria and documentation formats in [references/tactical-patterns.md](references/tactical-patterns.md). "Plain domain concept" is a legitimate, complete classification.
- Distill: classify each part of the emerging model as **core domain** (the differentiating value the purpose centers on), **supporting**, or **generic subdomain** (necessary but commodity — money, time zones, identity) — definitions in [references/strategic-patterns.md § Distillation](references/strategic-patterns.md#distillation). Analysis depth concentrates on the core; a generic subdomain gets a name, a boundary, and a note on off-the-shelf alternatives.
- Mark a boundary candidate wherever meaning, rules, lifecycle, authority, ownership, consistency needs, or rate of change shift — Step 2's homonyms and clusters of concepts that evolve for different business reasons are the strongest signals. Document each bounded-context candidate (purpose, language, owned concepts, key rules, dependencies) as a hypothesis with its evidence; existing teams, microservices, schemas, and repositories corroborate a boundary that meaning-shift evidence proposes — corroboration is all they supply. A legacy region that mixes models with no consistent boundary gets a boundary around the whole and the name *big ball of mud*: map its outside interfaces and keep modeling detail out of it ([references/strategic-patterns.md § Context-map patterns](references/strategic-patterns.md#context-map-patterns)).
- Map context relationships as the existing terrain: what each relationship exchanges (`Recruiting → supplies hired candidates → Onboarding`) and its character — upstream–downstream, mutually dependent, or free. Attach a context-mapping pattern label where its evidence criteria in [references/strategic-patterns.md](references/strategic-patterns.md#context-map-patterns) are met; a partially matching relationship stays described in plain information-flow terms, and proposals to change a relationship go to the report's next steps.

**Done when:** every candidate concept carries a domain-term responsibility, a classification (tactical where earned, plain concept otherwise), and a distillation class; and every boundary candidate names the shift that justifies it plus its evidence.

### Step 6 — Challenge the model

- **Scenario check** — walk Step 3's scenarios through the candidate model: normal flows, invalid operations, exceptions, and state transitions must all be explainable by it.
- **Rule check** — for every Step 4 rule, name where the model keeps it true. A rule that needs coordination across aggregate candidates means one of three things: the boundary is wrong, immediate consistency was assumed where the business tolerates delay, or the rule is a policy mislabeled as an invariant.
- **Language check** — model terms match the glossary, each term holds one meaning inside its context, and technical vocabulary that leaked into the model is flagged.
- **Boundary check** — each boundary answers: what meaning, rule, or responsibility changes across it, and what would get harder if the two sides shared one model — or were separated. A boundary without a stated reason stays tentative.
- **Size check** — a concept stays when it explains behaviour, protects a rule, or marks a distinction the domain recognizes; everything else comes out. The smallest explainable model beats the comprehensive speculative one.

**Done when:** every scenario, rule, term, and boundary has passed its check or the failure is recorded as a weak point or open question.

### Step 7 — Report

- Write the report following [references/report-template.md](references/report-template.md): scope, overview anchored by a domain vision statement (the core domain and its value, in about a paragraph), actors, ubiquitous language, scenarios, commands and events, rules, concepts with their distillation class, candidate model, bounded contexts, context relationships, validation results, open questions ranked by impact, assumptions, modeling decisions with alternatives, next steps.
- Diagrams (Mermaid — `flowchart` for business flows and context maps, `stateDiagram-v2` for lifecycles, `classDiagram` for concept relationships) summarize the analysis, split per capability or context, each explained by its surrounding prose.
- Keep the grades visible to the end: confidence columns, the assumptions table, the open-questions section.

**Done when:** the report contains every applicable template section; all Step 6 weak points appear under validation or open questions; and the completion criteria hold — important flows explainable by the model, terminology defined, rules identified, decisions traceable to evidence, boundaries reasoned, uncertainty visible, the whole understandable without reading the implementation.

## Red flags

| Rationalization | Reality |
|---|---|
| "The code already works this way, so the domain works this way" | implementation is evidence of system behaviour; as domain truth it grades as inference until corroborated |
| "Every concept needs its DDD stereotype" | a pattern is applied where it sharpens the model; plain domain concept is a complete classification |
| "The schema / team / service boundary shows the context boundary" | technical boundaries corroborate; shifts in meaning, rules, and responsibility decide |
| "A plausible rule fills this gap" | an ungrounded rule is an invention; the gap becomes an open question or a recorded assumption |
| "Ask the user whether X should be an entity" | users answer domain questions; translating answers into the model is the agent's job |
| "The class diagram is done, so the model is done" | a data-shape inventory explains no behaviour; scenarios, rules, and reasoned boundaries are the deliverable |
| "One canonical enterprise model will serve everyone" | a model is right for a purpose; meaning shifts between purposes are boundaries, not noise |
| "More concepts make a richer model" | every concept must explain behaviour, protect a rule, or mark a recognized distinction — the smallest useful model wins |

## Related

- [references/tactical-patterns.md](references/tactical-patterns.md) — criteria for Entity, Value Object, Domain Event, Aggregate, and Domain Service candidates, with documentation formats.
- [references/strategic-patterns.md](references/strategic-patterns.md) — DDD core definitions, context-relationship characterization, context-map pattern evidence criteria, and distillation.
- [references/report-template.md](references/report-template.md) — the report structure and the modeling-decision record format.
- `purpose-driven-software-design` — downstream: takes this skill's rules, invariants, and boundaries into code-structure decisions (rule ownership, seams, test levels).
