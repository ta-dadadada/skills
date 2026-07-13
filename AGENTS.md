# Repository Guidelines

## Project Structure & Module Organization

This repository distributes reusable Agent Skills rather than a compiled application. Each skill is a self-contained directory with a required `SKILL.md` and, when needed, a `README.md`, `references/`, or executable `scripts/` directory.

- `dev/`: software-development workflow skills, such as `dev/pr-handoff/`.
- `meta/`: skills for creating or improving other skills.
- `knowledge/`: distilled, reusable reference material; follow `knowledge/README.md` when adding content.
- `.local/`: ignored scratch space. Never place files intended for review or release here.

When adding or renaming a skill, keep its directory name identical to the `name` field in `SKILL.md` frontmatter and update the skill list in the root `README.md`.

## Build, Test, and Development Commands

There is no build system or application runtime. Validate changed skill packages directly:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/pr-handoff
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/* meta/*
```

The validator checks frontmatter, names, description limits, relative links, portability warnings, and script executable bits. Use `git diff --check` before committing to catch whitespace errors.

## Coding Style & Naming Conventions

Write skill bodies, references, and `knowledge/` content in concise English. Root operational documents may be Japanese. Use Markdown headings, short paragraphs, fenced command examples, and relative links. Skill directory names and frontmatter names use lowercase kebab-case, for example `hypothesis-driven-debugging`. Python utilities use four-space indentation and snake_case identifiers. For any skill creation or revision, follow `meta/shiranui-hanten/SKILL.md` instead of a generic skill generator.

## Testing Guidelines

Run the validator for every modified skill and resolve all `FAIL` results; review `WARN` output for intentional tool-specific behavior. If a script changes, exercise its success and failure paths manually and preserve executable permissions. Confirm every documented command and relative link from the directory where contributors will run it.

## Commit & Pull Request Guidelines

History follows Conventional Commit-style subjects: `feat:`, `fix:`, `docs:`, `refactor:`, and `chore:`. Keep the subject imperative and focused on one change. Pull requests should explain the skill's purpose, list affected paths, summarize validation performed, and link relevant issues. Include before/after excerpts when invocation rules or agent behavior change; screenshots are only needed for visual artifacts.
