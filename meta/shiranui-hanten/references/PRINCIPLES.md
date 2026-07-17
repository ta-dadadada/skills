# Principles

The judgment behind the decisions `SKILL.md` orders. Bold terms are defined in [GLOSSARY.md](GLOSSARY.md).

## Predictability

A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same *process* every run, not producing the same output — is the root virtue; every principle below is a lever serving it.

## What a skill is

Treat a skill as a reusable package of work procedures — what to check, in what order, which tool under which condition, and what counts as done — not as an override of model capability. Skills complement MCP and tools: they standardize *when and how* to use them.

### Skill layers

| Layer | Role | Examples |
|---|---|---|
| Domain | a unit of work in a domain | bug-fix, code-review, release-notes |
| Procedure | a flow reused across domains | reproduce → diagnose → fix → verify |
| Guard | a safety rule | secret detection, dangerous-command gating |
| Ops | maintenance behavior | logging, failure reporting |

Keep each skill in one layer. A draft that spans layers is a monolith in the making — split it, and let skills reference each other instead.

## Invocation

Two choices, trading different costs:

- A **model-invoked** skill keeps its description visible, so the agent can fire it autonomously and other skills can reach it. It pays **context load** — the description sits in the window every turn.
- A **user-invoked** skill strips the description from the agent's reach: only you, typing its name, can invoke it. Zero context load, but it spends **cognitive load** — you are the index that must remember it exists.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load. When user-invoked skills multiply past what you can remember, cure the piled-up cognitive load with a **router skill**: one user-invoked skill that names the others and when to reach for each.

Mechanics vary by tool (Claude Code uses `disable-model-invocation: true`); keep such fields out of skills meant to be portable — see [SPEC.md § Portability](SPEC.md#portability).

## Writing the description

The description does two jobs — state what the skill is, and list the **branches** that should trigger it. Every word increases context load, so it earns even harder pruning than the body:

- Front-load the skill's **leading word** — the description is where it does its invocation work.
- One trigger per branch. Synonyms that rename a single branch are duplication; collapse them, keep only genuinely distinct branches.
- Cut identity that's already in the body; keep triggers, plus any "when another skill needs…" reach clause.
- Include both *what* the skill does and *when* to use it — the description is the search index the agent routes on.

## Information hierarchy

A skill mixes two content types — **steps** and **reference** — and the core decision is where each piece sits on a ladder ranked by how immediately the agent needs it:

1. **In-skill step** — an ordered action in `SKILL.md`, the primary tier. Each step ends on a **completion criterion**: make it *checkable* (the agent can tell done from not-done) and, where it matters, *exhaustive* ("every modified file accounted for", not "produce a change list") — a vague criterion invites premature completion.
2. **In-skill reference** — a definition, rule, or fact in `SKILL.md`, consulted on demand. Often a legitimately flat peer-set — a fine arrangement, not a smell.
3. **External reference** — reference pushed into a separate file (conventionally `references/`), reached by a **context pointer**, loaded only when the pointer fires.

Push too little down and the top bloats; push too much and you hide material the agent actually needs. That tension is the whole decision. **Progressive disclosure** is the move down the ladder. Branching is the cleanest disclosure test: inline what every branch needs; push behind a pointer what only some branches reach. A pointer's *wording*, not its target, decides when the agent reaches the material — name the file and the moment ("judgment: `PRINCIPLES.md` § …").

Where the ladder decides how far down a piece sits, **co-location** decides what sits beside it once there: keep a concept's definition, rules, and caveats under one heading, so reading one part brings its neighbours with it.

A demanding completion criterion drives thorough **legwork** whether the skill has steps or not — "every rule applied" binds flat reference just as "every step done" binds a sequence.

## Leading words

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while running the skill (*tight*, *red*, *fog of war*). Repeated through the text — though a strong one may be needed only once — it accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens, by recruiting priors the model already holds. It serves predictability twice: in the body it anchors execution; in the description it anchors invocation.

Hunt for passages begging to collapse into one:

- "fast, deterministic, low-overhead" → a *tight* loop — one quality restated across a phase, collapsed into a single pretrained word.
- "a loop you believe in" → the loop goes *red* on the bug, or it doesn't — a fuzzy gate converted into a binary observable state.

You win twice: fewer tokens, and a sharper hook for the agent to hang its thinking on. Assume every skill carries restatements a leading word retires.

## When to split

**Granularity** is how finely you divide skills, and each cut spends one of the two loads, so split only when the cut earns it:

- **By invocation** — split off a model-invoked skill when a distinct leading word should trigger it on its own, or another skill must reach it. The new always-loaded description costs context load; the independent reach has to be worth it.
- **By sequence** — split a run of steps when the **post-completion steps** tempt the agent to rush the one in front of it. Keeping them out of view buys more legwork on the current task.

## Pruning

- Keep each meaning in a **single source of truth**: one authoritative place, so changing behaviour is a one-place edit.
- Check every line for **relevance**: does it still bear on what the skill does?
- Hunt **no-ops** sentence by sentence, not just line by line: run the test — does this change behaviour versus the default? — and when a sentence fails, delete the whole sentence rather than trim words from it. Most prose that fails should go, not be rewritten.

## Failure modes

Use these to diagnose a draft or a misbehaving skill.

| Failure | Mechanism | Counter-move |
|---|---|---|
| **Premature completion** | attention slips from the work to *being done* | sharpen the completion criterion first (cheap, local); split by sequence only if the criterion is irreducibly fuzzy *and* you observe the rush |
| **Duplication** | same meaning in more than one place | collapse to the single source of truth |
| **Sediment** | stale layers settle; adding feels safe, removing feels risky | pruning passes on every update; delete whole sentences |
| **Sprawl** | skill too long even with every line live | disclose reference behind pointers; split by branch or sequence |
| **No-op** | a line the model obeys by default | delete it, or replace a weak leading word with a stronger one (*relentless*, not *be thorough*) |
| **Negation** | prohibition names the banned thing and makes it more available | state the target behaviour positively; keep a prohibition only as a hard guardrail you can't phrase positively, paired with what to do instead |

## Verification

Proofreading is not verification — the author reads intent into their own text. Evaluate at three layers, because the final answer alone is insufficient:

1. **Final response** — did the run produce the right deliverable?
2. **Trajectory** — did the agent take the intended process? This is where a skill's predictability lives or dies.
3. **Single step** — at each decision point, did the skill's wording produce the intended choice?

Split **offline evaluation** (prepared regression scenarios, before release) from **online evaluation** (observing real use, after). The minimum bar for any new or changed skill: one **representative task** run by a fresh executor — an agent with no authorial context — while you watch the trajectory. Every stumble or discretionary fill-in marks a wording or structure defect; feed it back into writing and pruning. For a multi-iteration loop with instruction-side metrics, hand off to the `shiranui-hansode` skill.

## Safety

- Resolve credentials at runtime and keep skills in git: skill contents can leave the environment (Agent Skills are ZDR-exempt), so a secret, token, or internal endpoint written into a skill is published.
- A code-executing skill assumes sandbox isolation and monitoring; manage its permissions and audit trail in the same lifecycle as the skill text.
- Review bundled scripts like a dependency — checklist in [SPEC.md § Security](SPEC.md#security).

---

Adapted from [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock, MIT License. The "What a skill is", "Verification", and "Safety" sections are original additions.
