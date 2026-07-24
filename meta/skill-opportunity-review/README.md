# skill-opportunity-review

> Propose-only, four-verdict audit of a finished work session for durable skill opportunities: reconstruct the session's goal, decisions, corrections, failures, and verification; keep only lessons carrying reusable execution value, not mere knowledge; walk a preservation ladder that prefers improving an existing skill over creating a new one, and documentation over a new skill; then deliver in chat exactly one verdict per candidate — improve an existing skill, new skill candidate, document or memo, or no proposal — each backed by session evidence, creating and modifying nothing. Use near the end of a session that involved long trial-and-error, a novel problem solved, a significant design decision, or friction with an existing skill, or when the user asks whether the session yielded anything worth preserving. Not for routine sessions without such a signal, not for writing the PR story (pr-handoff), not for snapshotting in-flight work (session-handover), and not for creating or editing skills (shiranui-hanten).

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill skill-opportunity-review
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/meta/skill-opportunity-review
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/meta/skill-opportunity-review ~/.claude/skills/skill-opportunity-review
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
