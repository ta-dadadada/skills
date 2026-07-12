# backend-api-implementation

> Contract-first workflow for implementing a backend API endpoint in an existing project: discover the project's conventions, fix the input/output contract (schemas, error shapes, status/error codes), write tests against the contract, implement, verify with a real request. Tech-agnostic — REST, GraphQL, and gRPC alike. Use when adding a new endpoint or operation to an existing backend, or when changing an existing endpoint's request/response shape, error handling, or behaviour. Not for designing a new API or service from scratch.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add tadaair/skills --skill backend-api-implementation
```

Or copy the folder in directly:

```bash
npx degit tadaair/skills/dev/backend-api-implementation ~/.claude/skills/backend-api-implementation
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
