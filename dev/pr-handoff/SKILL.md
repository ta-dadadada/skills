---
name: pr-handoff
description: >-
  Propose-only wrap-up of an implementation session: read the repo's diff
  and the session's own record, separate what the diff proves from what
  the session shows was intended, ask the user about anything neither
  source answers, then deliver in chat a PR description (implementation
  summary, decisions with their reasons, notes) plus a logical commit
  split with Conventional-Commits messages as ready-to-run git commands —
  executing none of them. Use at the end of an implementation session,
  before opening a PR, when the current diff needs a reviewable
  explanation, when the session's decisions should be captured for
  reviewers, or when a logical commit plan is needed before committing.
  Not for doing the implementation itself, not for actually
  staging/committing/pushing or creating the PR, not without an existing
  diff to describe, and not for rewriting existing history.
license: MIT
metadata:
  author: tadaair
---

# PR Handoff

A handoff mixes two kinds of knowledge that must never blur: the diff is the only source of facts — what changed, in which files — and the session's own record is the only source of intent — why it changed, what was weighed and rejected. Anything found in neither becomes a question to the user, never a guess dressed as a summary. The skill proposes text and commands in chat and executes nothing: git state after the handoff equals git state before it. The handoff is done when the PR description and the commit plan sit together in one chat message.

## When to use

- At the end of an implementation session, before opening a PR.
- Turning the current diff into an explanation a reviewer can work from.
- Capturing the session's design decisions for reviewers before they evaporate with the context.
- Needing a logical commit split before committing.

## When not to use

- The implementation work itself — this skill describes a change, it does not make one.
- Executing git operations or creating/sending the PR — this skill only proposes.
- No diff exists — a generic PR template is not this skill's job.
- Summarizing text unrelated to the repository.
- Rewriting existing commit history.

## Workflow

### Step 1 — Inventory the diff (facts)

- Read the full change set: staged, unstaged, and untracked (`git status`, `git diff`, `git diff --staged`). When the PR will also cover work already committed on the branch, include the branch diff against its base/default branch.
- Read the nearby commit history for the message style the repo actually uses.
- Locate the repo's conventions that bind the output: PR template, CONTRIBUTING, commitlint or similar config, CLAUDE.md rules about commits and PRs.
- Everything recorded here is fact: what changed, in which files. Nothing in this step says why.

**Done when:** the full change set is enumerated with nothing outside it, and the repo's PR/commit conventions — or their confirmed absence — are recorded.

### Step 2 — Recover the intent

- From the current session's conversation, plans, working notes, memory, and recorded test/verification runs, collect: why the change was made, which alternatives were weighed and rejected, what was deliberately left out, which tests actually ran and with what results, and related issue/ticket numbers.
- Label every item with its source: fact-from-diff, intent-from-session, or repo-record. The label decides where the item may appear later.
- A session that holds no such record — a fresh session, a compacted context — yields a shorter list, not an invented one.
- Discard stale session items that predate the current diff: they describe other work and do not attach to these changes.

**Done when:** every summary and decision candidate carries a source label, and everything confirmable from no source is listed as an open gap.

### Step 3 — Close the gaps (question gate)

- Check the Step 2 gaps against what an accurate handoff needs: the change's purpose, why the chosen approach won, rejected alternatives, compatibility/migration decisions, deliberate non-goals, known limitations, issue numbers, and test results not witnessed in the session.
- If any of these is missing, ask the user those questions now, batched, and stop: no draft PR description or commit plan is shown until the answers arrive — a finished-looking draft invites rubber-stamping the guesses inside it.
- Ask only what blocks accuracy; with no blocking gaps, proceed without asking.

**Done when:** either every blocking gap has a user answer, or no blocking gaps existed.

### Step 4 — Compose the PR description

- Use the repo's PR template when Step 1 found one. Otherwise use this structure:

```markdown
# PR Description

## Implementation Summary
What changed and how behaviour differs after — meaning-level, not a file
list, not a code walkthrough. Only what the diff contains.

## Decisions
Each design decision or trade-off with its reason, drawn only from
labelled sources. When none were recorded, keep the section with the
single line "No design decisions were recorded beyond the implementation
itself." — the section proves the check happened.

## Notes
Known limitations, migration/compatibility notes, deliberate non-goals,
tests that ran with their results, verification that could not run,
reviewer attention points. Omit the whole section when nothing applies.
```

**Done when:** every Implementation Summary line traces to the diff, every Decision to a labelled source or a user answer, tests appear only with witnessed results, and Notes is either substantive or absent.

### Step 5 — Propose the commit split

- Partition the change set into commits by purpose and dependency: each commit reviewable alone, the sequence buildable in order, tests and docs travelling with the change they verify or describe, no unrelated changes sharing a commit, no mechanical file-per-commit split.
- Every authored change lands in exactly one commit — intra-file splits are the only exception. Generated artifacts in the work tree (build output, caches, bytecode) stay out of the plan and get a Note instead.
- Messages follow the repo's convention from Step 1 when one exists, else Conventional Commits: `type(scope): subject`, with the body in a second `-m`. Issue numbers appear only when confirmed in Step 2 or 3.
- Commands use explicit paths — `git add <paths>`, never `git add .` or `-A`. When one file genuinely belongs to two commits, prefer redrawing the commit boundary to whole files when the history reads as well; otherwise emit `git add -p <file>`, name which hunks to take, and flag that it needs interactive selection.
- Present each commit in this shape:

````markdown
### Commit 1
Add the retry policy to the HTTP client.

```sh
git add src/client/retry.ts src/client/http.ts
git commit -m "feat(client): add exponential-backoff retry policy" -m "Retries idempotent requests up to three times; callers opt out via RetryPolicy.none."
```
````

**Done when:** every authored file appears in exactly one commit (or a flagged `-p` split), generated artifacts are excluded with a Note, the sequence builds in order, each message follows the convention, and the commands are copy-runnable against the current work tree.

### Step 6 — Deliver in chat

- Put the PR description and the commit plan into one chat message, verbatim and complete.
- Create no files for the deliverable, unless the repo's own conventions require an artifact file.
- Execute no git command: `git status` after the skill equals `git status` before it.

**Done when:** the single message holds both artifacts, and the work tree and index are untouched.

## Red flags

| Rationalization | Reality |
|---|---|
| "The diff makes the reason obvious" | a reason read off the diff is a guess; reasons come from the session or the user |
| "Fill the Decisions section so it doesn't look empty" | an empty check result is a result; invented decisions poison the review |
| "The session mentioned X earlier" | session items that predate the current diff describe other work; only intent tied to these changes counts |
| "The tests presumably pass" | only witnessed runs with results go in; everything else is listed as not run |
| "Should be backward compatible" | unverified compatibility is a Note saying "not verified", not a guarantee |
| "One commit per file is simple" | files are storage units, not change units; split by purpose and dependency |
| "Squash the leftovers into the last commit" | a commit of unrelated leftovers is unreviewable; every change belongs to a purpose |
| "Draft the PR description first, ask later" | a finished-looking draft gets rubber-stamped; questions come before the artifact |
| "Just run the git commands, it's faster" | the deliverable is the proposal; executing it takes decisions that belong to the user |
| "Invent a plausible issue number format" | an unconfirmed reference points reviewers at the wrong work; omit it |
