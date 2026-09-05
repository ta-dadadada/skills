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
  "When to use" / "When not to use" → "Workflow" with every step ending on
  a bold `Done when:` line → "Red flags" table.
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
  CI workflow validates every skill and runs the `dev/local-intake` unittest
  suite on Python 3.11, 3.12, 3.13, and 3.14.

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
- Flag prose that merely restates a model's default behaviour (a no-op
  instruction) rather than changing it.
- Do not propose unrelated build tooling or non-Markdown artifacts; runtime
  code and CI must stay scoped to a skill that demonstrably needs them.
