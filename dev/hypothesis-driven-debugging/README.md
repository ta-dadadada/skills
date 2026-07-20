# hypothesis-driven-debugging

> Hypothesis-first debugging workflow for defects whose cause is unknown: reproduce and capture the failure, localize it to a candidate region, form falsifiable hypotheses ranked by evidence, confirm or refute each by observation (instrumentation, debugger, bisect) — one variable at a time, with refuted hypotheses recorded so they are not retried — fix the confirmed root cause minimally, then verify by re-running the original reproduction and lock it in with a regression test. Use when investigating a failing test, wrong output, crash, or regression whose cause is not yet established, or when a supposed fix did not hold and the defect has resurfaced. Not for changes whose cause is already demonstrated, not for performance tuning, and not for live-incident mitigation where restoring service precedes diagnosis.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill hypothesis-driven-debugging
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/hypothesis-driven-debugging
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/hypothesis-driven-debugging ~/.claude/skills/hypothesis-driven-debugging
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
