# shiranui-hansode

> Evaluate agent instructions when the user explicitly requests a structural review, empirical comparison, or iterative tuning. Compare outcomes, required boundaries, and observed execution across the selected environments. Not an automatic follow-up to skill edits.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill shiranui-hansode
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/meta/shiranui-hansode
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/meta/shiranui-hansode ~/.claude/skills/shiranui-hansode
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
- [references/executor-environments.md](./references/executor-environments.md) — environment-specific execution and metric capture

## Credits

Forked from [mizchi/skills](https://github.com/mizchi/skills/tree/main/meta/empirical-prompt-tuning)
by mizchi, substantially modified for this repository's conventions, and
treated here as an independent skill under the MIT License (repository
default; see the upstream repository's README for that convention). See
[SKILL.md](./SKILL.md) for details on what was changed.
