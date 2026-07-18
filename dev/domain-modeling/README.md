# domain-modeling

> Evidence-first domain modeling workflow: fix the modeling purpose and scope, extract graded domain facts and vocabulary from the available sources, reconstruct behaviour as scenarios, commands, and domain events, capture business rules and invariants, derive candidate concepts and bounded-context candidates, challenge the model, and deliver a domain-model report that keeps evidence, inference, hypothesis, and open question distinct. Behaviour before structure; tactical DDD patterns only where they sharpen the model. Use when exploring an unfamiliar business domain, extracting a domain model from requirements or an existing codebase, defining ubiquitous language or resolving terminology conflicts, identifying business rules and invariants, discovering bounded contexts and their relationships, distilling the core domain, or reviewing an existing domain model. Not for deciding code structure — hand that to purpose-driven-software-design — and not for one-off diagram generation from an already-documented model.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill domain-modeling
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/domain-modeling
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/domain-modeling ~/.claude/skills/domain-modeling
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
- [references/tactical-patterns.md](./references/tactical-patterns.md) — Entity / Value Object / Domain Event / Aggregate / Domain Service criteria
- [references/strategic-patterns.md](./references/strategic-patterns.md) — context-map pattern evidence criteria and distillation
- [references/report-template.md](./references/report-template.md) — the report structure
