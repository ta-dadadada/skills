# Strategic pattern criteria

Definitions and evidence criteria for Step 5 (boundaries, context relationships, distillation) and Step 7 (report) of [SKILL.md](../SKILL.md), following Eric Evans's *Domain-Driven Design Reference*. DDD in three points: focus on the core domain; explore models in a creative collaboration of domain practitioners and software practitioners; speak a ubiquitous language within an explicitly bounded context.

## Core definitions

- **Domain** — a sphere of knowledge, influence, or activity; the subject area to which the user applies the program.
- **Model** — a system of abstractions that describes selected aspects of a domain and can be used to solve problems related to that domain.
- **Ubiquitous language** — a language structured around the domain model and used by all team members within a bounded context to connect all the activities of the team with the software. A change in the language is a change to the model.
- **Context** — the setting in which a word or statement appears that determines its meaning; statements about a model can only be understood in a context.
- **Bounded context** — a description of a boundary (typically a subsystem, or the work of a particular team) within which a particular model is defined and applicable.

## Context relationships

The context map records the existing terrain — the relationships as they are; proposals to change them belong in the report's next steps. Characterize each relationship before reaching for a pattern label:

- **Upstream–downstream** — the upstream group's actions affect the downstream group's success, while the downstream's actions barely affect the upstream.
- **Mutually dependent** — both contexts must be delivered for either to be considered a success.
- **Free** — development in this context succeeds regardless of what happens in the others.

## Context-map patterns

Attach a pattern label when its evidence is present; a relationship the evidence only partially characterizes stays described in plain information-flow terms.

| Pattern | Relationship | Evidence that warrants the label |
|---|---|---|
| Partnership | mutually dependent | the two contexts succeed or fail together; coordinated planning and jointly managed integration |
| Shared Kernel | intimate interdependency | an explicitly bounded subset of the model (and its code or database design) that both teams agree not to change without consulting the other |
| Customer/Supplier | upstream–downstream | downstream priorities factor into upstream planning; negotiated and budgeted tasks for downstream requirements, often jointly developed acceptance tests |
| Conformist | upstream–downstream | the downstream adheres to the upstream model as is — its vocabulary mirrors the upstream's, with no translation layer |
| Anticorruption Layer | upstream–downstream | an isolating layer on the downstream side that translates the upstream system's model into the downstream's own domain model |
| Open-host Service | provider upstream of many | one protocol, opened as a set of services, serving all integrators — with one-off translators only for idiosyncratic consumers |
| Published Language | any translation point | a well-documented shared language (industry interchange standard, documented schema) as the medium of communication, translated into and out of |
| Separate Ways | free | no significant relationship between the two sets of functionality — no integration at all |
| Big Ball of Mud | boundary around a mess | models mixed and boundaries inconsistent inside a region; definitions and rules ambiguous or contradictory |

**Big Ball of Mud in analysis** — when a legacy region mixes models with no consistent boundary, draw a boundary around the entire mess and designate it a big ball of mud: sophisticated modeling stops at that boundary, the region is mapped by its interfaces to the outside, and the report says so. Stay alert to such regions sprawling into neighbouring contexts.

## Distillation

Not all parts of a model are equally valuable; distillation directs the modeling effort.

- **Core domain** — the part of the model that is the real business differentiator, the reason the system is worth building. Make the core small; give it the deepest analysis. Classify each part of the emerging model as **core**, **supporting** (necessary, specific to this business, but not differentiating), or **generic**.
- **Generic subdomains** — cohesive subdomains that are not the motivation for the project (money, time zones, identity/access, accounting basics). Model them without any trace of the project's specialties; note where an off-the-shelf or published model would do.
- **Domain vision statement** — a short (about one page) description of the core domain and the value it brings, ignoring whatever does not distinguish this model from others. In the report it anchors the domain overview.
- **Highlighted core** — the core elements flagged so a reader can tell effortlessly what is in or out of the core; in the report, the distillation column of the concepts table and the marked elements of the candidate model.

---

Pattern definitions adapted from Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) (2015), Creative Commons Attribution 4.0 (CC BY 4.0).
