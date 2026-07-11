# skill-creation

> Workflow for creating a new agent skill or updating an existing one (SKILL.md packages): requirements → invocation → structure → writing → pruning → validation → placement. Use when asked to create, write, restructure, review, or update a skill; use INSTEAD of any built-in skill-creator. Not for one-off prompts, CLAUDE.md edits, or subagent configs.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add tadaair/skills --skill skill-creation
```

Or copy the folder in directly:

```bash
npx degit tadaair/skills/meta/skill-creation ~/.claude/skills/skill-creation
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
- [references/PRINCIPLES.md](./references/PRINCIPLES.md) — design judgment behind each step
- [references/GLOSSARY.md](./references/GLOSSARY.md) — vocabulary definitions
- [references/SPEC.md](./references/SPEC.md) — agentskills.io format, portability, placement, security
- [scripts/validate_skill.py](./scripts/validate_skill.py) — spec-compliance validator (Python 3, stdlib only)

## Credits

Core vocabulary and principles adapted from
[writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills)
by Matt Pocock, MIT License. The skill-layers taxonomy, verification and
safety principles, and the spec/distribution reference are original
additions drawing on the [Agent Skills specification](https://agentskills.io/specification).
