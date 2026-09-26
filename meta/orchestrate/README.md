# orchestrate

Orchestrate an explicitly requested task through up to three subagents. The
main agent decomposes the work, selects a suitable available model for each
bounded assignment, coordinates dependencies, and integrates and verifies the
results, while delegating the substantive execution.

## Use

Explicitly invoke `orchestrate` alongside the task, or ask the main agent to
delegate the work and act as orchestrator. The mode applies to the current task
and does not broaden its scope or authority. It is not for creating persistent
subagent definitions, and it does not apply when delegation is unavailable.
Explicit-only activation is an instruction in the portable skill, not a
tool-enforced activation setting.

## Install

```bash
npx skills add ta-dadadada/skills --skill orchestrate
```

```bash
apm install ta-dadadada/skills/meta/orchestrate
```

## Files

- [SKILL.md](./SKILL.md) — the complete procedure; no scripts or references.
