# issue-kickoff

> Intake workflow for starting an implementation session from an issue or task request: read the issue and its linked context, restate the requirement, derive checkable acceptance criteria with an explicit out-of-scope list, ask the user about anything ambiguous before any code, survey the code the change will land in, then create the working branch (issue number in the name when the work ties to one) and deliver a work plan mapping each acceptance criterion to a verification step. Use at the start of an implementation session, when handed an issue, ticket, or verbal task to implement, or when the scope feels ambiguous before coding. Not for the implementation itself, not for deep design decisions (hand those to purpose-driven-software-design), and not for resuming work already underway with agreed criteria.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill issue-kickoff
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/issue-kickoff
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/issue-kickoff ~/.claude/skills/issue-kickoff
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
