# Glossary

One entry per term. `SKILL.md` orders the work, [`PRINCIPLES.md`](PRINCIPLES.md) explains the judgment, this file defines the vocabulary.

## Foundation

- **Predictability** — consistent satisfaction of required outcomes, quality, authority boundaries, and necessary ordering, allowing equivalent methods and routine judgment.
- **Skill** — a reusable package of work procedures: what to check, in what order, which tool under which condition, and what counts as done. It complements MCP and tools rather than replacing them; it is not an override of model capability.
- **Skill layers** — four roles a skill can play: **domain** (a unit of work: bug-fix, code-review, release-notes), **procedure** (a flow reused across domains: reproduce → diagnose → fix → verify), **guard** (a safety rule: secret detection, dangerous-command gating), **ops** (maintenance behavior: logging, failure reporting).

## Invocation

- **Invocation** — how a skill gets reached: by the model on its own, or by the user typing its name.
- **Model-invoked** — a skill whose description stays visible to the agent, so it can fire autonomously and other skills can reach it. Pays context load.
- **User-invoked** — a skill whose description is stripped from the agent's reach; only the user typing its name fires it. Zero context load, but pays cognitive load.
- **Description** — the frontmatter field that is both the skill's summary and the search index the agent routes on. For a model-invoked skill it must say what the skill does *and* when to use it.
- **Context pointer** — a reference naming out-of-context material; its wording, not its target, decides when and how reliably the agent reaches it.
- **Context load** — the cost a model-invoked skill imposes: its description sits in the context window every turn.
- **Cognitive load** — the human cost of user-invoked skills: you are the index that must remember they exist.
- **Router skill** — one user-invoked skill that names other user-invoked skills and when to reach for each, consolidating cognitive load into a single entry point.
- **Granularity** — how finely skills divide. Each cut spends context load or cognitive load, so split only when the cut earns it.

## Information hierarchy

- **Information hierarchy** — a ladder ranking content by how immediately the agent needs it: in-skill step → in-skill reference → external reference.
- **Steps** — actions in `SKILL.md`, ordered where dependencies require it; completion criteria identify meaningful gates.
- **Reference** — a definition, rule, or fact consulted on demand rather than executed in order.
- **External reference** — reference pushed out of `SKILL.md` into a separate file, reached by a context pointer, loaded only when the pointer fires.
- **Progressive disclosure** — moving content down the ladder — out of `SKILL.md` into a linked file — so the top stays legible.
- **Co-location** — keeping a concept's definition, rules, and caveats under one heading, so reading one part brings its neighbours with it.
- **Sprawl** — unrelated responsibilities or irrelevant material that obscure the task; length alone does not establish it.

## Steering

- **Branch** — a distinct way the skill is used; different runs take different paths through it. Inline what every branch needs; put behind a pointer what only some branches reach.
- **Leading word** — an optional compact concept supporting recognition or execution; concrete requirements remain authoritative across models.
- **Completion criterion** — the condition that tells the agent a step (or the whole task) is done. Must be *checkable* (done vs not-done is decidable) and, where it matters, *exhaustive*.
- **Legwork** — the digging the agent does within the work. Raised by demanding completion criteria.
- **Post-completion steps** — the steps still ahead of the current one; their visibility tempts the agent to rush.
- **Premature completion** — ending a step before it's genuinely done, attention slipping to *being done*. Countered by sharper criteria first, splitting second.
- **Negation** — wording that prohibits behavior; retain it where it states scope or authority precisely, and clarify permitted actions where needed.

## Pruning

- **Pruning** — the discipline of keeping every file lean: relevance checks, no-op hunts, duplicate collapse.
- **Single source of truth** — one authoritative place per meaning, so changing behaviour is a one-place edit.
- **Duplication** — the same meaning in more than one place; costs maintenance and tokens, and inflates the meaning's apparent rank.
- **Relevance** — whether a line still bears on what the skill does.
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky. The default fate of an unpruned skill.
- **No-op** — text adding neither a requirement nor useful guidance. A requirement remains necessary even when a model follows it by default.

## Verification

- **Three-layer evaluation** — judging a skill at three levels: final response, trajectory, and single step. The final answer alone is insufficient.
- **Trajectory** — the sequence of actions and decisions the agent took during a run. The layer where a skill's predictability lives or dies.
- **Offline evaluation** — running the skill against prepared scenarios (regression, expected-output) before release.
- **Online evaluation** — observing real runs of the skill after release.
- **Representative task** — a realistic task a fresh executor runs to check affected behavior; select it according to the change rather than requiring it for every edit.

---

Adapted from [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock, MIT License. The Foundation and Verification sections are original additions.
