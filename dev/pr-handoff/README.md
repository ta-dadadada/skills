# pr-handoff

> Propose-only wrap-up of an implementation session: read the repo's diff and the session's own record, separate what the diff proves from what the session shows was intended, ask the user about anything neither source answers, then deliver in chat a PR description (implementation summary, decisions with their reasons, notes) plus a logical commit split with Conventional-Commits messages as ready-to-run git commands — executing none of them. Use at the end of an implementation session, before opening a PR, when the current diff needs a reviewable explanation, when the session's decisions should be captured for reviewers, or when a logical commit plan is needed before committing. Not for doing the implementation itself, not for actually staging/committing/pushing or creating the PR, not without an existing diff to describe, and not for rewriting existing history.

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
