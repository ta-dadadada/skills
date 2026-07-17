# shiranui-hansode

> Methodology for iteratively improving agent-facing instructions (skills / slash commands / CLAUDE.md / code-gen prompts) via bias-free executor + two-sided evaluation (self-report + instruction-side metrics). Meta-skill, invoke ONLY when the user explicitly asks for an "empirical" eval of a prompt or skill, or for the Iter-0 description / body consistency check. Do NOT auto-invoke after every skill edit; this loop is operator-triggered by name.

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

## Credits

Forked from [mizchi/skills](https://github.com/mizchi/skills/tree/main/meta/empirical-prompt-tuning)
by mizchi, substantially modified for this repository's conventions, and
treated here as an independent skill under the MIT License (repository
default; see the upstream repository's README for that convention). See
[SKILL.md](./SKILL.md) for details on what was changed.
