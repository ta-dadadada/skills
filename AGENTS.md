# Repository Guidelines

## Project Structure & Module Organization

This repository distributes reusable Agent Skills rather than a compiled application. Each skill is a self-contained directory with a required `SKILL.md` and, when needed, a `README.md`, `references/`, or executable `scripts/` directory.

- `dev/`: software-development workflow skills, such as `dev/pr-handoff/`.
- `meta/`: skills for creating or improving other skills.
- `knowledge/`: distilled, reusable reference material; follow `knowledge/README.md` when adding content.
- `.local/`: ignored scratch space. Never place files intended for review or release here.

When adding or renaming a skill, keep its directory name identical to the `name` field in `SKILL.md` frontmatter and update the skill list in `docs/project-guide.md`. Keep the root `README.md` focused on readers and users, linking to that guide instead of duplicating the inventory. Contributor documentation belongs in `docs/development-guide.md`.

## Project Skills

The canonical sources for this repository's own skills are in `dev/` and `meta/`.
Selected workflows are exposed through relative directory symlinks in
`.agents/skills/` and `.claude/skills/`; keep both sets aligned. These installed
workflows support maintaining this repository, not the full distribution inventory.

When selecting one of these project-installed skills, read its symlink target's
`SKILL.md` and resolve references and scripts from that canonical directory.
If a personal installation has the same skill name, use the repository source
for work here; do not merge instructions from the personal copy. This is a
repository execution rule, not a claim that tools hide or automatically override
same-name skills. Leave personal installations unchanged unless the user asks.

- Skill creation or revision: use `meta/shiranui-hanten/SKILL.md`.
- Explicit instruction review, comparison, or tuning: use
  `meta/shiranui-hansode/SKILL.md`; do not run empirical evaluation automatically
  after every edit.
- Interrupted work: write a checkpoint with `dev/session-handover/SKILL.md`,
  then reconcile and continue with `dev/session-resume/SKILL.md` when resuming.
  Keep `.agent-session.md` out of version control.

Other project-installed skills retain their own invocation conditions; installing
a skill does not require running it on every task.

## Build, Test, and Development Commands

There is no compiled build. Validate skill packages and test runtime utilities directly:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/pr-handoff
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/* meta/*
python3 -m unittest discover -s dev/local-intake/tests -v
```

The validator checks frontmatter, names, description limits, relative links, portability warnings, and script executable bits. The `CI` workflow runs the full validator and runtime tests on `ubuntu-slim` across Python 3.11, 3.12, 3.13, and 3.14. Use `git diff --check` before committing to catch whitespace errors.

## Coding Style & Naming Conventions

Write skill bodies, references, and `knowledge/` content in concise English. Root operational documents may be Japanese. Use Markdown headings, short paragraphs, fenced command examples, and relative links. Skill directory names and frontmatter names use lowercase kebab-case, for example `hypothesis-driven-debugging`. Python utilities use four-space indentation and snake_case identifiers. For any skill creation or revision, follow `meta/shiranui-hanten/SKILL.md` instead of a generic skill generator.

## Testing Guidelines

Run the validator for every modified skill and resolve all `FAIL` results; review `WARN` output for intentional tool-specific behavior. If a script changes, run its automated tests, exercise uncovered success and failure paths manually, and preserve executable permissions. Confirm every documented command and relative link from the directory where contributors will run it.

## Commit & Pull Request Guidelines

History follows Conventional Commit-style subjects: `feat:`, `fix:`, `docs:`, `refactor:`, and `chore:`. Keep the subject imperative and focused on one change. Pull requests should explain the skill's purpose, list affected paths, summarize validation performed, and link relevant issues. Include before/after excerpts when invocation rules or agent behavior change; screenshots are only needed for visual artifacts.
