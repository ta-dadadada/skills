# terraform-implementation

> Blast-radius-first workflow for implementing a change in an existing Terraform codebase: discover the project's conventions (layout, state boundaries, naming, pinning, checks), predict every touched resource's plan action (create / update in-place / replace / destroy) before writing code, implement following those conventions, verify with fmt + validate + the project's configured linters, hand off the diff with the prediction. terraform plan runs only when explicitly instructed. Provider-agnostic. Use when adding, changing, renaming/moving, or removing resources, data sources, modules, variables, or outputs in existing Terraform code. Not for designing a new stack from scratch (backend, state layout, directory strategy) or for operating infrastructure (apply, destroy, state surgery).

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add tadaair/skills --skill terraform-implementation
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install tadaair/skills/dev/terraform-implementation
```

Or copy the folder in directly:

```bash
npx degit tadaair/skills/dev/terraform-implementation ~/.claude/skills/terraform-implementation
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
