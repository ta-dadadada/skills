# session-goal

> Goal-first session intake: pin a development session to one confirmed goal — one session, one goal, about one PR's worth — before any planning or code. Read the materials the user pointed to (issue URLs, local files) first, do only the light project reconnaissance the goal needs, turn every remaining gap into questions instead of guesses, keep the goal at Why/What with How left out, get the user's confirmation, then persist the goal as a Japanese statement of at most three lines in .agent-goal.md at the project root (kept out of version control) so an interrupted session's purpose survives and later transfers into the PR description. Use at the start of a development session, when the opening prompt is vague or names several candidate goals, or when mid-session drift calls for re-pinning the purpose. Not for acceptance criteria, work plans, or branching (issue-kickoff), not for design or implementation proposals, and not for snapshotting in-flight work (session-handover).

## Install

This is an [Agent Skills](https://agentskills.io) skill — a portable
`SKILL.md` folder that works with Claude Code, Codex, GitHub Copilot,
Cursor, and other [compatible agents](https://agentskills.io/clients).

With the [`skills`](https://github.com/vercel-labs/skills) CLI (installs into
every detected agent's skills directory):

```bash
npx skills add ta-dadadada/skills --skill session-goal
```

Or with [apm](https://github.com/microsoft/apm):

```bash
apm install ta-dadadada/skills/dev/session-goal
```

Or copy the folder in directly:

```bash
npx degit ta-dadadada/skills/dev/session-goal ~/.claude/skills/session-goal
```

## Files

- [SKILL.md](./SKILL.md) — the workflow (start here)
