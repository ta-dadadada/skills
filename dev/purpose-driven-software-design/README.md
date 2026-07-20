# purpose-driven-software-design

> Purpose-first design workflow for software changes that involve a design decision — introducing or relocating a rule, responsibility, state transition, dependency, abstraction, or axis of variation — not for every behaviour change: clarify whose problem the change solves, pin ambiguous domain terms, discover the existing design and the evidenced axes of change (Follow / Adapt / Avoid), give every rule an authoritative owner, choose the smallest sound extensible structure — open along evidenced axes, closed against hypothetical ones — map each behaviour to the cheapest test level, review changeability. Applies to APIs, event handlers, batch jobs, CLIs, frontend, and domain logic alike. Use when deciding where data and logic belong, when a new variation keeps forcing edits to the same core code, when introducing or resisting an abstraction or commonization, or when reviewing a change for changeability. Not for purely mechanical changes, nor required for small local changes that fit the existing design as is.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill purpose-driven-software-design
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/purpose-driven-software-design
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/purpose-driven-software-design ~/.claude/skills/purpose-driven-software-design
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
