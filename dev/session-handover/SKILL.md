---
name: session-handover
description: >-
  Session-handover snapshot for interrupted work: extract what only this
  session's conversation and work can supply — the goal, observable
  status, verified checks with commands and results, the intent behind
  uncommitted changes, agreed decisions, failed attempts, hard-won
  findings, and the next concrete actions — and overwrite
  .agent-session.md at the project root (gitignored) so the next worker,
  human or AI, resumes from that file alone without redoing the
  session's investigation. Use when pausing or ending a session with
  work still in flight, when handing in-progress work to another person
  or agent, or when session context is about to be lost. Not for
  wrapping up a finished change for review (that is pr-handoff), not for
  permanent documentation, and not for continuous note-taking — it runs
  once, at the point of interruption.
license: MIT
compatibility: >-
  Steps 1, 2, and 4 use pwd, date, and read-only git commands
  (rev-parse, branch --show-current, status --short, diff --stat); in a
  directory git does not manage, the git-dependent parts are skipped.
metadata:
  author: ta-dadadada
---

# Session Handover

Every line in a handover is judged by one test: **would the next worker's actions change without it?** The file carries only what this session's conversation and work can supply — the why, the agreed decisions, the witnessed results, the failed attempts, the findings that were expensive to dig up. Anything recoverable from code, git, or docs in minutes stays out, shrinking to a `path:line` pointer at most. Because the file spends the next worker's context, completeness and compression are a single quality bar, not a trade-off: 80 lines is the budget. One fixed file, fully overwritten each run — the repository itself is the history.

## When to use

- Pausing or ending a session while work is still in flight.
- Handing in-progress work to another person or agent.
- Session context is about to be lost (compaction, window limits).

## When not to use

- Wrapping up a finished change for review — that is `pr-handoff`'s job.
- Permanent documentation (design docs, ADRs, READMEs) — a handover is disposable by design.
- Continuous note-taking during the session — this skill runs once, at the point of interruption.

## Workflow

### Step 1 — Fix the environment

- Get the working directory (`pwd`); the output target is `<cwd>/.agent-session.md`, always.
- Determine whether the directory is git-managed (`git rev-parse --is-inside-work-tree`); when it is not, skip every git-dependent part below (Step 2, Step 4, and the header's branch/HEAD fields).
- Take an ISO8601 timestamp (`date -Iseconds`).

**Done when:** the target path, the git-or-not verdict, and the timestamp are fixed.

### Step 2 — Collect the git context (git repositories only)

- Record the current branch (`git branch --show-current`) and short HEAD (`git rev-parse --short HEAD`) for the header — the next worker judges freshness and drift from these.
- Use `git status --short` and `git diff --stat` to corroborate the uncommitted-changes section; the raw output itself stays out of the file.

**Done when:** branch and HEAD are recorded and the uncommitted change set is corroborated — or the directory is non-git and this step was skipped.

### Step 3 — Extract the session's core and write the file

- Select content by origin: only information that exists in this session's conversation and tool results qualifies. Worth writing: the purpose and the design decisions the user directed or agreed to, with their reasons; checks that actually ran, with command and result; attempts that failed, with what was tried and what happened; facts that took real digging, reduced to a conclusion plus `path:line`; constraints the next worker would otherwise trip over.
- Point instead of transcribe for everything reconstructible from the repository: file structures, function lists, diff contents, and `git log`/`git status` output stay out — the header's branch/HEAD stands in for them.
- Leave out speculation, cause hypotheses, future proposals, and external URLs that never appeared in the session; something that still needs investigating becomes a "verify X" entry under Next steps ("tried A, failed with B" is an observation and belongs in Pitfalls).
- State progress as observable facts — "10 of 12 vitest cases pass; `test_foo` and `test_bar` fail" — and use official names, never session-local nicknames or codenames.
- Write the file with a full overwrite, following this template. Goal, Status, and Next steps are mandatory; every other section is omitted entirely when empty rather than filled with "none":

```markdown
# Agent Session Handover

_<ISO8601> | branch: `<branch>` | HEAD: `<short-hash>`_
<!-- non-git directory: _<ISO8601>_ only -->

## Goal

<The top-level goal and why it matters. 1-3 sentences, written for a
reader with zero context.>

## Status

<How far the work has progressed and what remains, in observable facts.>

Verified:

- `<command>` → <pass/fail with counts> (at HEAD `<hash>`)
<!-- omit the whole "Verified:" block when nothing was run; the HEAD
     marker lets the next worker decide whether to re-run -->

## Uncommitted changes

| File | Intent / completeness (only what the diff cannot show) |
| --- | --- |
| `path/to/file` | <what the change is for; done, or how far along> |

## Next steps

1. <An action executable without further judgment: the command to run,
   or the `path:line` to edit plus the completion condition>
2. <The one after>

## Decisions (do not reopen)

- <A direction the user agreed to: content and reason in one line>

## Pitfalls & already investigated

- <A constraint or precondition the next worker would trip over>
- <A failed approach: what was tried, what happened>
- <An expensive finding: the conclusion, as `path:line`>

## References

- <Pointers only, to issues/PRs/specs/docs that appeared in the session>
```

**Done when:** the file matches the template with the three mandatory sections filled with observable facts, every remaining line passes the would-their-actions-change test, empty sections are absent, and the total stays within 80 lines.

### Step 4 — Keep the file out of version control (git repositories only)

- Read `<cwd>/.gitignore`; when a line already equals `.agent-session.md` (ignoring surrounding whitespace), leave the file untouched.
- Otherwise append `.agent-session.md` as one line at the end, inserting a newline first when the file lacks a trailing one; when no `.gitignore` exists, create it with that single line.

**Done when:** `.gitignore` contains the entry exactly once — or the directory is non-git and this step was skipped.

### Step 5 — Report

- Tell the user, briefly: the written path and its line count; what happened to `.gitignore` (appended, already present, or skipped as non-git); which sections were included and which omitted.
- The file body itself stays out of the chat — the user can read the file directly.

**Done when:** the report carries those three items and the file content is not repeated in chat.

## Red flags

| Rationalization | Reality |
|---|---|
| "Write everything down so nothing is lost" | the file spends the next worker's context; a line earns its place only by changing their actions |
| "Mostly done, I'll just say that" | vague progress transfers nothing; state what passes, what fails, and the counts |
| "Keep the previous handover as history" | the repository is the history; the handover is a snapshot, fully overwritten |
| "Add my hypothesis about the cause" | untested hypotheses send the next worker down your guess; put "verify X" in Next steps instead |
| "Copy the diff so it's self-contained" | the diff is one `git diff` away; only the intent behind it is session-knowledge |
| "Fill the empty section with 'none'" | an omitted section says the same thing in zero lines |
| "The codename we used is convenient" | the next reader was not in this session; official names only |
| "80 lines is too tight for this session" | the budget is the quality bar — cut by the would-their-actions-change test until it fits |

## Related

- `session-resume` — reconciles and consumes the checkpoint when interrupted work continues.
- `pr-handoff` — the exit for *finished* work heading to review; this skill is the exit for *interrupted* work heading to another session.
