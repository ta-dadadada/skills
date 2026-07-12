# Knowledge Base

Distilled, reusable reference material extracted from research notes and
collected resources. Raw research dumps stay in `.local/` (gitignored); this
directory holds only the systematized versions worth keeping and reusing —
for example as source material when authoring skills in this repository.

## Conventions

- One topic per file. Merge overlapping material instead of keeping parallel
  reports.
- English, per repository convention.
- Every file ends with a **Sources** section listing origin URLs and the date
  the material was collected. Facts that decay (star counts, deprecation
  dates, tool support matrices) carry an as-of date — re-verify before
  relying on them.
- Do not duplicate what a skill in this repository already documents; link to
  it instead (e.g. `meta/skill-creation/references/SPEC.md` for the Agent
  Skills format).

## Index

### agent-skills/

| File | Contents |
|---|---|
| [design-principles.md](./agent-skills/design-principles.md) | How to design agent skills: skill as a procedure package, layering, context engineering, tool design |
| [evaluation.md](./agent-skills/evaluation.md) | Evaluating agents and skills: three-layer evaluation, offline/online, trajectory tests, ACI |
| [security-and-operations.md](./agent-skills/security-and-operations.md) | Sandboxing, permissions, supply-chain risk of third-party skills, observability, cost |
| [multi-tool-distribution.md](./agent-skills/multi-tool-distribution.md) | Distributing one skill to Codex / Claude Code / Copilot / Cursor: tool extensions, overlay build pipeline |
| [reference-catalog.md](./agent-skills/reference-catalog.md) | Curated catalog of external skill/agent repositories and primary documentation |

### software-design/

| File | Contents |
|---|---|
| [minodriven-design.md](./software-design/minodriven-design.md) | MinoDriven (仙塲大也)'s software design philosophy: changeability, purpose-driven structuring, constraints, AI-era application |

### prompts/

| File | Contents |
|---|---|
| [pre-launch-audit.md](./prompts/pre-launch-audit.md) | Comprehensive pre-launch application audit prompt (security, concurrency, reliability, a11y, UI) |
