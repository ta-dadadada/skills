---
name: shiranui-hanten
description: >-
  Workflow for creating a new agent skill or updating an existing one
  (SKILL.md packages): requirements → invocation → structure → writing →
  pruning → validation → placement. Use when asked to create, write,
  restructure, review, or update a skill; use INSTEAD of any built-in
  skill-creator. Not for one-off prompts, CLAUDE.md edits, or subagent
  configs.
license: MIT
metadata:
  author: ta-dadadada
---

# Shiranui Hanten

A skill is a reusable package of task requirements and work procedures. **Predictability** means consistently meeting the required outcomes, quality constraints, authority boundaries, and necessary ordering while allowing equivalent methods and routine judgment. Judgment lives in [references/PRINCIPLES.md](references/PRINCIPLES.md), definitions in [references/GLOSSARY.md](references/GLOSSARY.md), format and distribution rules in [references/SPEC.md](references/SPEC.md).

## When to use

- Creating a new skill from scratch.
- Updating, restructuring, or reviewing an existing skill.

## When not to use

- One-off prompts — nothing reusable to standardize.
- CLAUDE.md, subagent, or rules files — different formats with different loading semantics.
- Running a multi-iteration tuning loop by itself — hand off to `shiranui-hansode`.

## Workflow

### Step 0 — Route

- Decide the branch: create, update, or review only.
- For updates and reviews, read the target `SKILL.md` and references relevant to the affected requirements. Expand to full linked-file review when the impact cannot be bounded. Diagnose against the failure-modes table (judgment: [PRINCIPLES.md § Failure modes](references/PRINCIPLES.md#failure-modes)) and write findings with evidence and unexamined scope.
- For review-only work, deliver those findings and limitations. Editing, empirical execution, and placement require their own requested scope; this branch ends here.
- Re-enter at the earliest step whose output the change touches: description problem → Step 2; missing or misplaced content → Step 3; wording → Step 4.

**Done when:** the branch is chosen and, for updates or reviews, scoped findings exist; review-only work ends with their delivery.

### Step 1 — Requirements

- State the job in one sentence: what task, what deliverable, executed by whom.
- Identify the skill's primary responsibility — domain / procedure / guard / ops (judgment: [PRINCIPLES.md § What a skill is](references/PRINCIPLES.md#what-a-skill-is)). Consider a split when responsibilities need independent invocation or ownership.
- Write the skill-level completion criterion: how the executing agent knows the task the skill drives is done.
- Separate required outcomes, quality, authority, and necessary ordering from recommended methods and permitted judgment. Preserve explicit user constraints, including technical constraints. A skill's design-only or propose-only completion defines its handoff, not completion of broader work already requested.

**Done when:** job sentence, layer, and a checkable completion criterion are written down.

### Step 2 — Invocation & description

- Choose model-invoked or user-invoked (judgment: [PRINCIPLES.md § Invocation](references/PRINCIPLES.md#invocation)).
- Draft the description: purpose and invocation conditions first, including consequential exclusions and delivery boundaries, within 1024 chars ([SPEC.md § Frontmatter](references/SPEC.md#frontmatter)). Shortening wording does not authorize changing triggers or removing existing functions.

**Done when:** the description identifies when to use the skill and agrees with the body's supported routes and boundaries.

### Step 3 — Structure

- Give every planned piece of content one home on the three-tier ladder: in-skill step, in-skill reference, or external reference under `references/` (judgment: [PRINCIPLES.md § Information hierarchy](references/PRINCIPLES.md#information-hierarchy)).
- Apply the branching test: inline what every branch needs; push behind a pointer what only some branches reach.
- Consider splits for independent invocation or ownership, or an observed sequencing problem that clearer completion criteria cannot resolve. Weigh the added dependency and maintenance cost ([PRINCIPLES.md § When to split](references/PRINCIPLES.md#when-to-split)).

**Done when:** a section list exists in which every section has exactly one home.

### Step 4 — Writing

- Follow the body pattern: title → thesis → when to use / when not to use → workflow → red flags → related.
- State checkable completion criteria for the skill and meaningful decision or handoff gates. Use per-step `Done when:` lines where they prevent omission or define a necessary dependency, rather than requiring the format for every action.
- State the target behaviour clearly. Retain explicit prohibitions where they express scope or authority precisely.
- Keep the skill portable: relative paths, standard frontmatter only, tool-specific syntax left to overlays ([SPEC.md § Portability](references/SPEC.md#portability)).

**Done when:** required outcomes and gates are checkable, permitted judgment is clear, and every pointer names an existing file and section.

### Step 5 — Pruning

- Review affected text for obsolete guidance and duplication, preserving required outcomes, quality, workflow, and authority even when a model already follows them. Treat model-compensating guidance as a hypothesis to evaluate, not a requirement to delete by default (judgment: [PRINCIPLES.md § Pruning](references/PRINCIPLES.md#pruning)).
- Secrets check: skill contents can leave the environment, so credentials, tokens, and internal endpoints stay out of every file ([PRINCIPLES.md § Safety](references/PRINCIPLES.md#safety)).

**Done when:** the affected text preserves required guarantees, identified duplication or obsolete guidance is resolved, and the secrets check is clean.

### Step 6 — Validation & verification

- Mechanical: run `python3 scripts/validate_skill.py <skill-dir>` — all checks green.
- Static: every trigger in the description has a matching branch in the body, and vice versa.
- Choose further checks by changed behavior, following [PRINCIPLES.md § Verification](references/PRINCIPLES.md#verification). Use focused comparisons for invocation or decision changes; expand where failures or differences appear. Keep static findings, recorded prior runs, and current execution evidence distinct. A multi-iteration `shiranui-hansode` loop runs only when explicitly requested.

**Done when:** the validator passes, description and body agree, and the report states relevant checks, their results, and any pending behavioral comparison without claiming untested effects.

### Step 7 — Placement

- Put the canonical source at `<category>/<skill-name>/` in this repository; frontmatter `name` equals the directory name.
- Install where the consuming tools read skills — `.agents/skills/` and `.claude/skills/`, by copy or symlink ([SPEC.md § Placement](references/SPEC.md#placement)).

**Done when:** `name` matches the directory and the skill is reachable at each consuming tool's path.

## Red flags

| Rationalization | Reality |
|---|---|
| "The body makes it obvious" | at routing time the model sees only the description; triggers live there |
| "Keep this paragraph just in case" | sediment — delete whole sentences |
| "I reread it and it's clear" | static clarity is not execution evidence; compare affected behavior when that is the claim |
| "More skills always clarify the work" | split only when independent responsibility or an observed workflow problem earns the dependency cost |
| "The model does this already" | required outcomes and boundaries remain requirements; assess compensating guidance separately |
| "It reads well, ship it" | premature completion — Step 6 was not run |

## Related

- [references/PRINCIPLES.md](references/PRINCIPLES.md) — the judgment; [references/GLOSSARY.md](references/GLOSSARY.md) — the definitions; [references/SPEC.md](references/SPEC.md) — the format, portability, placement, and security rules. This file only orders the work.
- `shiranui-hansode` — the multi-iteration version of Step 6.
