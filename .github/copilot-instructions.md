# Copilot instructions for this repository

Write all review comments and PR summaries in Japanese. The repository
content itself is English.

## What this repository is

Agent skills, subagent configs, and prompt files for coding agents (Claude
Code, Codex, GitHub Copilot, Cursor). Distributed content is primarily
Markdown, with focused runtime scripts and tests where a skill needs them;
there is no compiled build step. The authority for skill structure and style is
`meta/shiranui-hanten/SKILL.md` and its `references/` (SPEC, PRINCIPLES,
GLOSSARY).

For project skill selection and canonical sources, follow
[AGENTS.md's Project Skills](../AGENTS.md#project-skills). Do not merge a
project-installed skill with a same-name personal copy.

## Layout

- `dev/<skill>/`, `meta/<skill>/` — one directory per skill: `SKILL.md`
  (the skill) plus `README.md` (distribution).
- `knowledge/` — distilled English reference notes; conventions in
  `knowledge/README.md`.
- `.local/` — gitignored scratch space; nothing under it may be committed
  or referenced.

## Rules to check when reviewing skills

- Frontmatter `name` equals the directory name and matches
  `^[a-z0-9]+(?:-[a-z0-9]+)*$`; `description` is at most 1024 characters
  and states both what the skill does and when to fire.
- The body follows the house pattern: title → one-paragraph thesis →
  "When to use" / "When not to use" → "Workflow" → "Red flags" table.
  Require checkable completion criteria for the skill and meaningful gates;
  per-action `Done when:` lines are optional.
- Every trigger in the description has a matching branch in the body, and
  vice versa.
- Portability: relative links that resolve, no absolute paths, no
  tool-specific syntax (`${CLAUDE_SKILL_DIR}`, backtick command injection,
  `disable-model-invocation`), standard frontmatter fields only.
- The `README.md` blockquote equals the frontmatter description verbatim.
- No secrets, tokens, or internal endpoints anywhere in a skill — skill
  contents leave the environment.
- `python3 meta/shiranui-hanten/scripts/validate_skill.py <skill-dir>`
  must pass for every touched skill.
- Runtime script changes must keep their focused automated tests passing. The
  CI workflow always validates every skill on Python 3.11, 3.12, 3.13, and
  3.14. The `dev/local-intake` unittest suite runs on those versions only for
  Python-related or CI workflow changes; see `docs/development-guide.md` for
  the change filter.

## Rules to check when reviewing knowledge files

- One topic per file, English, ending with a Sources section that carries
  origin URLs and collection dates.
- Knowledge files must not duplicate what a skill already documents; they
  link to the skill instead.

## Review focus

- Flag vague completion criteria — a `Done when:` line the executing agent
  cannot check invites premature completion.
- Flag duplicated meaning across files; each rule should have one
  authoritative home.
- Apply `meta/shiranui-hanten/references/PRINCIPLES.md` for predictability,
  permitted judgment, pruning, and change-scoped verification. Required outcomes,
  quality, procedures, and authority remain requirements even when a model
  follows them by default. Do not flag routine evidence-based choices merely
  because the request did not spell them out.
- Do not propose unrelated build tooling or non-Markdown artifacts; runtime
  code and CI must stay scoped to a skill that demonstrably needs them.
