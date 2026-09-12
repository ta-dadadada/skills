# implementation-loop

> Convergence loop for implementing an already agreed change one acceptance criterion at a time: re-observe the repository, select one pending criterion, route its implementation through the relevant specialist workflow, prefer deterministic verification, review the result, continue independent work around blocked criteria, reopen criteria on findings, and finish with global verification plus an independent fresh-context full-diff review. Use after issue-kickoff or equivalent intake when settled criteria, dependencies, blockers, or review feedback require coordination across implementation cycles. Not for deriving scope or criteria, supplying domain-specific implementation methods, PR/commit planning, or a small direct change whose normal implementation workflow already provides a sufficient convergence path.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill implementation-loop
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/implementation-loop
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/implementation-loop ~/.claude/skills/implementation-loop
```

## Files

- [SKILL.md](SKILL.md) — the workflow.
- [VALIDATION.md](VALIDATION.md) — requirements, design decisions, and validation evidence.
