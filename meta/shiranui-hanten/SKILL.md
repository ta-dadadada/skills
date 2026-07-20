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
  author: tadaair
---

# Shiranui Hanten

A skill is a reusable package of work procedures — what to check, in what order, which tool under which condition, and what counts as done — not an override of model capability. The root virtue is **predictability**: the agent takes the same *process* every run. Every step below serves it. Judgment lives in [references/PRINCIPLES.md](references/PRINCIPLES.md), definitions in [references/GLOSSARY.md](references/GLOSSARY.md), format and distribution rules in [references/SPEC.md](references/SPEC.md).

## When to use

- Creating a new skill from scratch.
- Updating, restructuring, or reviewing an existing skill.

## When not to use

- One-off prompts — nothing reusable to standardize.
- CLAUDE.md, subagent, or rules files — different formats with different loading semantics.
- Running a multi-iteration tuning loop by itself — hand off to `shiranui-hansode`.

## Workflow

### Step 0 — Route

- Decide the branch: create new, or update existing.
- For updates: read the target `SKILL.md` and every file it points to, in full. Diagnose against the failure-modes table (judgment: [PRINCIPLES.md § Failure modes](references/PRINCIPLES.md#failure-modes)) and write a findings list.
- Re-enter at the earliest step whose output the change touches: description problem → Step 2; missing or misplaced content → Step 3; wording → Step 4.

**Done when:** the branch is chosen and, for updates, a findings list exists.

### Step 1 — Requirements

- State the job in one sentence: what task, what deliverable, executed by whom.
- Classify the skill's layer — domain / procedure / guard / ops (judgment: [PRINCIPLES.md § What a skill is](references/PRINCIPLES.md#what-a-skill-is)). A draft spanning layers is a split candidate; carry it to Step 3.
- Write the skill-level completion criterion: how the executing agent knows the task the skill drives is done.

**Done when:** job sentence, layer, and a checkable completion criterion are written down.

### Step 2 — Invocation & description

- Choose model-invoked or user-invoked (judgment: [PRINCIPLES.md § Invocation](references/PRINCIPLES.md#invocation)).
- Draft the description: leading word first, one trigger per branch, both *what* it does and *when* to use it, within 1024 chars ([SPEC.md § Frontmatter](references/SPEC.md#frontmatter)).

**Done when:** the description opens on a leading word and its triggers map 1:1 onto the branches the body will carry.

### Step 3 — Structure

- Give every planned piece of content one home on the three-tier ladder: in-skill step, in-skill reference, or external reference under `references/` (judgment: [PRINCIPLES.md § Information hierarchy](references/PRINCIPLES.md#information-hierarchy)).
- Apply the branching test: inline what every branch needs; push behind a pointer what only some branches reach.
- Decide splits — a distinct leading word or a rush-inducing sequence becomes its own skill ([PRINCIPLES.md § When to split](references/PRINCIPLES.md#when-to-split)).

**Done when:** a section list exists in which every section has exactly one home.

### Step 4 — Writing

- Follow the body pattern: title → thesis → when to use / when not to use → workflow → red flags → related.
- End every workflow step on a `Done when:` line; make the criterion set checkable and exhaustive.
- State instructions as positives — say the target behaviour, not the banned one.
- Keep the skill portable: relative paths, standard frontmatter only, tool-specific syntax left to overlays ([SPEC.md § Portability](references/SPEC.md#portability)).

**Done when:** every step has a checkable criterion and every pointer names an existing file and section.

### Step 5 — Pruning

- Pass sentence by sentence over every file: delete no-ops whole, collapse duplication back to its single source of truth, rewrite negations as positive instructions (judgment: [PRINCIPLES.md § Pruning](references/PRINCIPLES.md#pruning)).
- Secrets check: skill contents can leave the environment, so credentials, tokens, and internal endpoints stay out of every file ([PRINCIPLES.md § Safety](references/PRINCIPLES.md#safety)).

**Done when:** a full pass yields zero further edits and the secrets check is clean.

### Step 6 — Validation & verification

- Mechanical: run `python3 scripts/validate_skill.py <skill-dir>` — all checks green.
- Static: every trigger in the description has a matching branch in the body, and vice versa.
- Empirical: have a fresh executor — an agent with no authorial context — run one representative task, and watch the trajectory, not just the final answer (judgment: [PRINCIPLES.md § Verification](references/PRINCIPLES.md#verification)). Feed each stumble back into Step 4 or 5. For a multi-iteration loop, hand off to `shiranui-hansode`.

**Done when:** the validator passes, description and body agree, and one representative run follows the intended process without discretionary fill-ins.

### Step 7 — Placement

- Put the canonical source at `<category>/<skill-name>/` in this repository; frontmatter `name` equals the directory name.
- Install where the consuming tools read skills — `.agents/skills/` and `.claude/skills/`, by copy or symlink ([SPEC.md § Placement](references/SPEC.md#placement)).

**Done when:** `name` matches the directory and the skill is reachable at each consuming tool's path.

## Red flags

| Rationalization | Reality |
|---|---|
| "The body makes it obvious" | at routing time the model sees only the description; triggers live there |
| "Keep this paragraph just in case" | sediment — delete whole sentences |
| "I reread it and it's clear" | author bias; only a fresh executor's run counts |
| "One skill can cover creation, evaluation, and deployment" | sprawl — split by leading word or sequence |
| "Add 'don't do X'" | negation plants X; state the positive |
| "It reads well, ship it" | premature completion — Step 6 was not run |

## Related

- [references/PRINCIPLES.md](references/PRINCIPLES.md) — the judgment; [references/GLOSSARY.md](references/GLOSSARY.md) — the definitions; [references/SPEC.md](references/SPEC.md) — the format, portability, placement, and security rules. This file only orders the work.
- `shiranui-hansode` — the multi-iteration version of Step 6.
