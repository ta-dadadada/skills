# session-resume

> Resume interrupted development work from .agent-session.md: read the handover, reconcile its goal, decisions, evidence, and next steps with the latest user instructions and current repository state, then carry the first valid next step forward without repeating settled investigation. Use when continuing work from a session-handover snapshot or when the user asks to resume an interrupted session. Not for starting new work without a handover, recovering arbitrary chat history, or summarizing progress without continuing the task.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill session-resume
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/session-resume
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/session-resume ~/.claude/skills/session-resume
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
