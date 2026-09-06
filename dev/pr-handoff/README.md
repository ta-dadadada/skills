# pr-handoff

> Propose a PR description and logical commit plan for an existing diff at implementation handoff, before opening a PR, or when preparing changes and session decisions for review. Does not stage, commit, push, create a PR, or rewrite history.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill pr-handoff
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/pr-handoff
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/pr-handoff ~/.claude/skills/pr-handoff
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
