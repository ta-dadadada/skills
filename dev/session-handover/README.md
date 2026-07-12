# session-handover

> Session-handover snapshot for interrupted work: extract what only this session's conversation and work can supply — the goal, observable status, verified checks with commands and results, the intent behind uncommitted changes, agreed decisions, failed attempts, hard-won findings, and the next concrete actions — and overwrite .agent-session.md at the project root (gitignored) so the next worker, human or AI, resumes from that file alone without redoing the session's investigation. Use when pausing or ending a session with work still in flight, when handing in-progress work to another person or agent, or when session context is about to be lost. Not for wrapping up a finished change for review (that is pr-handoff), not for permanent documentation, and not for continuous note-taking — it runs once, at the point of interruption.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add tadaair/skills --skill session-handover
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install tadaair/skills/dev/session-handover
```

Or copy the folder in directly:

```bash
npx degit tadaair/skills/dev/session-handover ~/.claude/skills/session-handover
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
