# Principles

The judgment behind the decisions `SKILL.md` orders. Bold terms are defined in [GLOSSARY.md](GLOSSARY.md).

## Predictability

**Predictability** means consistently satisfying required outcomes, quality constraints, authority boundaries, and necessary ordering across supported models and tools. Equivalent methods and evidence-based routine choices are allowed within those constraints.

Separate durable requirements from guidance intended to compensate for a model's observed weakness. Preserve requirements even when a model follows them unaided. Evaluate compensating guidance against the affected task before keeping, changing, or removing it.

Define judgment boundaries by consequence. Choosing spacing from an existing UI system is routine judgment. Inventing business rules, scope, or authority without evidence, or presenting an assumption as a confirmed fact, is a defect. Missing wording alone is not a reason to ask: ask when an unresolved decision changes the task, authority, or required outcome and available evidence or delegated discretion cannot resolve it. Record consequential assumptions as assumptions.

Preserve ordering that protects a dependency, such as establishing a behavior baseline before changing it or reviewing a design before implementing it. Independent investigation and equivalent tools need not follow an identical sequence.

## What a skill is

Treat a skill as a reusable package of work procedures — what to check, in what order, which tool under which condition, and what counts as done — not as an override of model capability. Skills complement MCP and tools: they standardize *when and how* to use them.

### Skill layers

| Layer | Role | Examples |
|---|---|---|
| Domain | a unit of work in a domain | bug-fix, code-review, release-notes |
| Procedure | a flow reused across domains | reproduce → diagnose → fix → verify |
| Guard | a safety rule | secret detection, dangerous-command gating |
| Ops | maintenance behavior | logging, failure reporting |

Give each skill a clear primary responsibility. Split when independent invocation or ownership earns the extra dependency; keep supporting quality and authority constraints with the workflow that needs them.

## Invocation

Two choices, trading different costs:

- A **model-invoked** skill keeps its description visible, so the agent can fire it autonomously and other skills can reach it. It pays **context load** — the description sits in the window every turn.
- A **user-invoked** skill strips the description from the agent's reach: only you, typing its name, can invoke it. Zero context load, but it spends **cognitive load** — you are the index that must remember it exists.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load. When user-invoked skills multiply past what you can remember, cure the piled-up cognitive load with a **router skill**: one user-invoked skill that names the others and when to reach for each.

Mechanics vary by tool (Claude Code uses `disable-model-invocation: true`); keep such fields out of skills meant to be portable — see [SPEC.md § Portability](SPEC.md#portability).

## Writing the description

The description does two jobs — state what the skill is, and list the **branches** that should trigger it. Every word increases context load, so it earns even harder pruning than the body:

- Front-load the purpose and invocation conditions. A **leading word** may help recognition, but is optional and does not replace concrete triggers.
- One trigger per branch. Synonyms that rename a single branch are duplication; collapse them, keep only genuinely distinct branches.
- Cut identity that's already in the body; keep triggers, plus any "when another skill needs…" reach clause.
- Include both *what* the skill does and *when* to use it — the description is the search index the agent routes on.

## Information hierarchy

A skill mixes two content types — **steps** and **reference** — and the core decision is where each piece sits on a ladder ranked by how immediately the agent needs it:

1. **In-skill step** — an ordered action in `SKILL.md`, the primary tier. State **completion criteria** for meaningful gates: make it *checkable* (the agent can tell done from not-done) and, where it matters, *exhaustive* ("every modified file accounted for", not "produce a change list") — a vague criterion invites premature completion.
2. **In-skill reference** — a definition, rule, or fact in `SKILL.md`, consulted on demand. Often a legitimately flat peer-set — a fine arrangement, not a smell.
3. **External reference** — reference pushed into a separate file (conventionally `references/`), reached by a **context pointer**, loaded only when the pointer fires.

Push too little down and the top bloats; push too much and you hide material the agent actually needs. That tension is the whole decision. **Progressive disclosure** is the move down the ladder. Branching is the cleanest disclosure test: inline what every branch needs; push behind a pointer what only some branches reach. A pointer's *wording*, not its target, decides when the agent reaches the material — name the file and the moment ("judgment: `PRINCIPLES.md` § …").

Where the ladder decides how far down a piece sits, **co-location** decides what sits beside it once there: keep a concept's definition, rules, and caveats under one heading, so reading one part brings its neighbours with it.

Completion criteria cover the applicable requirements, whether expressed as reference or steps. Their scope must distinguish required checks from irrelevant work and permit reuse of unchanged evidence where appropriate.

## Leading words

A **leading word** is an optional compact concept that may help an agent recognize or apply guidance. Its interpretation can vary across models; concrete outcomes and decision boundaries remain authoritative. Retain it when it helps clarity, not merely to reduce token count.

## When to split

**Granularity** is how finely you divide skills, and each cut spends one of the two loads, so split only when the cut earns it:

- **By invocation** — split off a model-invoked skill when a distinct task should trigger it on its own, or another skill must reach it. The new always-loaded description costs context load; the independent reach has to be worth it.
- **By sequence** — consider a split when an observed rush toward later work persists despite clear completion criteria. Preserve the handoff and continuation of already requested work; compare whether the split actually improves completion.

## Pruning

- Keep each meaning in a **single source of truth**: one authoritative place, so changing behaviour is a one-place edit.
- Check every line for **relevance**: does it still bear on what the skill does?
- Remove **no-ops** that add neither a requirement nor useful guidance. A model following a rule by default does not make it a no-op. Preserve user-required outcomes, quality, procedures, and authority. Assess model-compensating guidance through focused comparisons; length alone is not a defect.

## Failure modes

Use these to diagnose a draft or a misbehaving skill.

| Failure | Mechanism | Counter-move |
|---|---|---|
| **Premature completion** | attention slips from the work to *being done* | sharpen the completion criterion first (cheap, local); split by sequence only if the criterion is irreducibly fuzzy *and* you observe the rush |
| **Duplication** | same meaning in more than one place | collapse to the single source of truth |
| **Sediment** | stale layers settle; adding feels safe, removing feels risky | pruning passes on every update; delete whole sentences |
| **Sprawl** | unrelated responsibilities or irrelevant material obscure the task | disclose conditional references; split only where independent responsibilities justify it |
| **No-op** | text adds neither a requirement nor useful guidance | remove it while preserving durable requirements |
| **Unclear boundary** | a broad prohibition hides what is permitted or when confirmation is needed | name the action, scope, existing authorization, and unresolved decision; retain explicit prohibitions where precise |

## Verification

Proofreading is not verification — the author reads intent into their own text. Evaluate at three layers, because the final answer alone is insufficient:

1. **Final response** — did the run produce the right deliverable?
2. **Trajectory** — were required events, authority boundaries, and necessary ordering respected, without unnecessary questions, reads, repeated checks, or premature stopping? Accept equivalent methods.
3. **Single step** — at each decision point, did the skill's wording produce the intended choice?

Separate **offline evaluation** from **online evaluation**, and select checks for the changed behavior:

- Meaning-preserving wording, inventory, and link fixes: diff review and mechanical checks.
- Invocation changes: compare relevant activation and non-activation cases; preserve intended functions as well as exclusions.
- Decision, authority, or completion changes: compare affected cases before and after in the supported environments, using fresh executors without authorial context. Expand when differences or regressions appear.
- Script changes: run the relevant automated tests and check uncovered affected success and failure paths.

Record the checks performed and pending comparisons. Static consistency does not establish behavioral improvement. Distinguish permitted judgment from unsupported business, scope, or authority decisions and assumptions presented as facts; only the latter require correction on that basis. No fixed suite size or multi-iteration loop is required for every edit. Use `shiranui-hansode` for a multi-iteration loop only when explicitly requested.

## Safety

- Resolve credentials at runtime and keep skills in git: skill contents can leave the environment (Agent Skills are ZDR-exempt), so a secret, token, or internal endpoint written into a skill is published.
- A code-executing skill assumes sandbox isolation and monitoring; manage its permissions and audit trail in the same lifecycle as the skill text.
- Review bundled scripts like a dependency — checklist in [SPEC.md § Security](SPEC.md#security).

---

Adapted from [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock, MIT License. The "What a skill is", "Verification", and "Safety" sections are original additions.
