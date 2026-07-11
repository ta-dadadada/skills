# characterization-testing

> Safety-net-first workflow for changing existing code that has no or untrusted tests: scope the observable behaviour that must survive the change, find the least invasive seam to get the code under test, write characterization tests that pin down what the code actually does today — capturing surprising or buggy behaviour as-is and reporting it instead of silently fixing it — then make the intended change with the net in place, so the failing tests are exactly the intentionally changed behaviours. Use before modifying, refactoring, or extracting legacy code that lacks tests, or when changes to an area keep breaking behaviour nobody predicted. Not for greenfield code, not for code already covered by trusted tests, and not for deciding whether current behaviour is correct — that decision belongs to the user.

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add tadaair/skills --skill characterization-testing
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install tadaair/skills/dev/characterization-testing
```

Or copy the folder in directly:

```bash
npx degit tadaair/skills/dev/characterization-testing ~/.claude/skills/characterization-testing
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
