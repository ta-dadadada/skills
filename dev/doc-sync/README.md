# doc-sync

> Diff-driven documentation reconciliation before wrapping up an implementation: inventory the change set's externally observable deltas (commands, flags, APIs, config keys, env vars, setup steps, behaviour), inventory the repository's documentation surface (READMEs, docs/, agent instruction files like CLAUDE.md, docstrings on changed public APIs, config examples, specs, templates), cross-check every delta against that surface, then update what the diff contradicts or leaves incomplete — matching the surrounding document's style — and report items needing a judgment call instead of guessing. Use before finishing an implementation session or before pr-handoff, after any change that alters commands, APIs, configuration, setup steps, or user-visible behaviour. Not for writing new documentation from scratch, not for doc-only sessions, and not for release-notes generation beyond what the repo's own conventions require.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add tadaair/skills --skill doc-sync
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install tadaair/skills/dev/doc-sync
```

Or copy the folder in directly:

```bash
npx degit tadaair/skills/dev/doc-sync ~/.claude/skills/doc-sync
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
