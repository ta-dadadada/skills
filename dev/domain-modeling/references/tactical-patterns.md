# Tactical pattern criteria

Classification criteria for Steps 3 and 5 of [SKILL.md](../SKILL.md), following Eric Evans's *Domain-Driven Design Reference*. A candidate concept receives a tactical classification when it meets the criteria below; otherwise it stays a plain domain concept, which is a complete answer.

## Entity

An Entity represents a thread of continuity and identity, going through a lifecycle, though its attributes may change. A concept is an Entity candidate when:

- its identity matters across time — the business tracks *this one* through changes, and must distinguish it from others even when their attributes match;
- its attributes may change while it remains the same conceptual thing — the business must match it across representations even when attributes differ.

The model must define what it means to be the same thing: name the means of identification (an external identifier, or one created by and for the system) — mistaken identity corrupts data. Stay alert to requirements that call for matching objects by attributes; they mark where the identity definition is still unsettled.

Document: identity (what "the same one" means and how it is established), lifecycle, important state transitions, behaviour.

## Value Object

Value Objects are the objects that describe things. A concept is a Value Object candidate when:

- the business cares only about its attributes and logic — identity is irrelevant, the value alone defines it;
- it is immutable, and its operations are side-effect-free functions;
- validation or domain behaviour belongs with the value.

Model meaningful domain concepts — `Money`, `EmailAddress`, `DateRange`, `EmploymentPeriod` — where the domain gives the value rules or behaviour; a primitive with neither stays a primitive.

## Domain Event

Something happened that domain experts care about — a full-fledged part of the model, distinct from system events that reflect activity within the software (a system event may carry or respond to a domain event, which is what earns technical operations a place only when the business assigns them meaning). When modeling an event in depth, record:

- immutability — an event is a record of something in the past;
- a timestamp for when the event occurred (and, where entry lags occurrence, a second timestamp for when it entered the system, with who entered it);
- the identities of the entities involved — which, when needed, also serve as the event's own identity, so duplicate deliveries can be recognized as the same event.

Model the domain's activity as a series of such discrete events: they make explicit the causes of state changes that an entity's current state alone cannot explain.

## Aggregate

Aggregates come from consistency requirements — Step 4's invariants and their participating concepts — with object containment playing no part. For each candidate answer:

1. Which invariant must be protected?
2. Which objects must change atomically to protect it?
3. What is the smallest boundary that maintains the invariant?
4. Can everything outside the boundary be referenced by identity?

One entity is the root; external references go to the root only, and enforcement of the aggregate's invariants is the root's responsibility. Consistency rules apply synchronously within the boundary and asynchronously across boundaries — a rule the business needs enforced synchronously across two candidate aggregates is Step 6's signal to reconsider the boundaries, and such reconsideration often surfaces a missed domain insight.

Small aggregates are the default; each enlargement must be paid for by an invariant that needs it. Database foreign keys, UI screen composition, object nesting, and CRUD transaction convenience are shapes of the current implementation — an aggregate boundary drawn from them needs an invariant to back it.

Documentation format:

```markdown
### Application

Root: Application

Responsibilities:
- control the application lifecycle
- prevent invalid transitions

Invariants:
- a submitted application cannot be submitted again
- a completed application cannot return to an active state

Contained concepts:
- ApplicationStatus

External references (by identity):
- PositionId
- ApplicantId
```

## Domain Service

Sometimes, it just isn't a thing. A Domain Service candidate is important domain behaviour — a significant process or transformation — that:

- belongs naturally to no single Entity or Value Object, where forcing it onto one would distort that object or add a meaningless artificial one;
- represents an operation the domain itself names;
- is expressed in domain language.

Behaviour that does have a natural home goes to that home; a service that collects unrelated logic is a catch-all, and each piece gets re-homed by these criteria.

## Repository

A Repository is a software concern, secondary to domain analysis: note one only for an Aggregate Root whose retrieval or persistence the analysis must mention, and leave the rest to design.

---

Pattern definitions adapted from Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) (2015), Creative Commons Attribution 4.0 (CC BY 4.0).
