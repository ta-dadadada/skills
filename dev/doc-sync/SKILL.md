---
name: doc-sync
description: >-
  Diff-driven documentation reconciliation before wrapping up an
  implementation: inventory the change set's externally observable
  deltas (commands, flags, APIs, config keys, env vars, setup steps,
  behaviour), inventory the repository's documentation surface (READMEs,
  docs/, agent instruction files like CLAUDE.md, docstrings on changed
  public APIs, config examples, specs, templates), cross-check every
  delta against that surface, then update what the diff contradicts or
  leaves incomplete — matching the surrounding document's style — and
  report items needing a judgment call instead of guessing. Use before
  finishing an implementation session or before pr-handoff, after any
  change that alters commands, APIs, configuration, setup steps, or
  user-visible behaviour. Not for writing new documentation from
  scratch, not for doc-only sessions, and not for release-notes
  generation beyond what the repo's own conventions require.
license: MIT
metadata:
  author: ta-dadadada
---

# Doc Sync

The documentation surface is inventoried by searching the repository, not recalled from memory ("usually the README and..."). Every verdict traces to what the diff proves: a description the diff contradicts gets fixed, but a description the diff cannot settle — tone, an announcement's wording, the reasoning behind a design choice — is not rewritten on a guess; it goes back to the user. "Checked, no impact" is itself a deliverable, reported distinctly from a silent skip.

## When to use

- Before finishing an implementation session, or before running `pr-handoff`.
- After any change that alters commands, APIs, configuration, setup steps, or user-visible behaviour.

## When not to use

- Writing new documentation from scratch.
- A session whose only work is documentation.
- Generating release notes beyond what the repository's own conventions require.

## Workflow

### Step 1 — Inventory the diff's observable deltas

- From the change set (staged, unstaged, branch diff), list every externally observable delta: new, changed, or removed commands, flags, public APIs, config keys, environment variables, dependencies, file layout, setup steps, and behaviour.
- A change confined to internal implementation is recorded as having no observable delta.

**Done when:** the delta list is written, or the change is recorded as having no externally observable delta.

### Step 2 — Inventory the documentation surface

- Search the repository for its documentation surface rather than assuming where it lives: root and subdirectory READMEs, `docs/`, a CHANGELOG (only when the repo's convention requires a per-PR entry), agent instruction files such as CLAUDE.md, docstrings and comments on changed public APIs, config examples (`.env.example` and similar), schema/spec files, templates, and help text.

**Done when:** the documentation surface is listed with paths, discovered by searching the repository rather than assumed.

### Step 3 — Cross-check

- For every delta against every relevant document, reach a verdict: **contradicted** (the diff made the description wrong), **incomplete** (a new item of a kind the surface already documents is missing from it), or **unaffected**.
- Search the documentation surface for the identifiers the diff touched — command names, flags, paths, keys — to catch mentions that a manual read would miss.
- A delta that no document mentions anywhere resolves to unaffected across the whole surface; documenting it from scratch stays outside this skill.

**Done when:** every delta has a verdict against every relevant document, backed by an identifier search across the surface.

### Step 4 — Update or escalate

- Fix every contradicted or incomplete finding, matching the surrounding document's style, language, and level of detail.
- Leave alone anything the diff cannot settle on its own — unclear document intent, user-facing announcement copy, a tone or judgment call — and route it to the report as a question instead of guessing.
- A provable fix applies even when it sits beside an escalated item; note the resulting transient inconsistency in the escalation entry. A heading and its body take one shared verdict — update both or escalate both.
- Stay inside the delta's scope: an unrelated section that could use a tidy-up is out of scope for this pass.

**Done when:** every contradicted or incomplete finding is either an applied edit in the surrounding style or an escalated item with the reason it needs a judgment call.

### Step 5 — Report the reconciliation

- Report in three categories: documentation updated (what and why), documentation checked and found unaffected, and items left for the user's judgment.
- This report becomes the input to `pr-handoff`.

**Done when:** the report lists updated, checked-and-unaffected, and escalated items — all three categories, even when empty.

## Red flags

| Rationalization | Reality |
|---|---|
| "The README is the only thing that matters" | the documentation surface is discovered by searching; docstrings, config examples, and agent instruction files are part of it too |
| "This doc probably isn't related" | unaffected is a verdict earned by an identifier search, not an assumption |
| "While I'm here, this old section could use a rewrite" | anything outside the delta's scope is separate work |
| "The intent here is unclear but I'll take a guess" | a rewrite the diff cannot prove is a guess; escalate it as a question instead |
| "The CHANGELOG gets an entry every time" | only when the repo's own convention requires one — confirmed in Step 2 |
| "Nothing needed changing, so nothing to report" | checked-and-unaffected is a real finding, distinct from a silent skip; report all three categories |

## Related

- `pr-handoff` — consumes this skill's report as an input; doc-sync runs first, pr-handoff after.
