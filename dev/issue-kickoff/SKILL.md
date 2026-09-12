---
name: issue-kickoff
description: >-
  Intake workflow for starting an implementation session from an issue
  or task request: read the issue and its linked context, restate the
  requirement, derive checkable acceptance criteria with an explicit
  out-of-scope list, ask the user about anything ambiguous before any
  code, survey the code the change will land in, then create the working
  branch (issue number in the name when the work ties to one) and
  deliver a work plan mapping each acceptance criterion to a
  verification step. Use at the start of an implementation session, when
  handed an issue, ticket, or verbal task to implement, or when the
  scope feels ambiguous before coding. Not for the implementation
  itself, not for deep design decisions (hand those to
  purpose-driven-software-design), and not for resuming work already
  underway with agreed criteria.
license: MIT
compatibility: >-
  Step 1 may use the gh CLI when the work source is a GitHub issue;
  absent gh, paste the issue content into the conversation.
metadata:
  author: ta-dadadada
---

# Issue Kickoff

What counts as done is agreed before any code is written. Ambiguity is never filled by guessing — it becomes a question to the user, the same question-gate discipline `pr-handoff` applies on the way out. Scope is fixed by naming both what is in and what is explicitly out. The branch and the plan trace back to the issue. This skill's own execution stops at creating the branch — the implementation itself is other work.

## When to use

- Starting an implementation session.
- Handed an issue, ticket, or verbal task to implement.
- The scope feels ambiguous before coding starts.

## When not to use

- The implementation itself — this skill only prepares for it.
- Deep design decisions — hand those to `purpose-driven-software-design`.
- Resuming work already underway with acceptance criteria already agreed.

## Workflow

### Step 1 — Read the source of work

- Read the issue body, any linked discussion, and referenced code — `gh issue view` for a GitHub issue, or the conversation itself for a verbal request — plus the minimal look at the code needed to phrase the Step 3 questions; the full landing-zone survey stays in Step 4.
- A linked reference that cannot be read (no gh, nothing pasted) is recorded as unread; when the work's independence from it cannot be established, it joins the question gate.
- Restate the requirement in your own words. Record the issue's metadata: number, labels, related issues or PRs — or note explicitly that no tracked issue exists.
- Separate the actual requirement from background noise in the source material.

**Done when:** the requirement is restated in the skill's own words and the issue metadata (number, links) is recorded — or the absence of a tracked issue is noted.

### Step 2 — Derive acceptance criteria

- Convert the requirement into checkable acceptance criteria, written as observable behaviour. Label each with its source: stated in the issue, or proposed by you.
- Write an explicit out-of-scope list — what this work will not do.

**Done when:** every criterion is checkable, labelled with its source (stated in the issue, or proposed), and an explicit out-of-scope list exists.

### Step 3 — Question gate

- Batch every ambiguity that would change the implementation into individually numbered questions for the user, put the proposed-label criteria to them as one consolidated confirm-or-amend item alongside, and stop until the answers arrive. A plan that already looks finished invites rubber-stamping guesses instead of correcting them, so nothing plan-shaped is produced yet.
- Non-blocking questions get noted in the plan instead of asked.

**Done when:** every blocking ambiguity has a user answer, or none existed.

### Step 4 — Survey the landing zone

- Identify where the change lands: the files it will touch, the existing patterns and conventions to follow, and the tests it affects.
- This is reconnaissance, not design — when the survey surfaces a decision that needs real design work, flag `purpose-driven-software-design` for that part of the plan rather than resolving it here.

**Done when:** the entry files and the conventions to follow are named, and any needed design work is flagged in the plan.

### Step 5 — Branch and plan

- Create the working branch following the repository's naming convention (`git switch -c`), including the issue number in the name when the work ties to one.
- Deliver the work plan in chat: ordered steps, with each acceptance criterion mapped to the verification step that will confirm it.

**Done when:** the branch exists and follows the repo's convention (issue number included when one exists), and the delivered plan maps every acceptance criterion to a verification step.

## Red flags

| Rationalization | Reality |
|---|---|
| "The issue title says enough" | the real requirement is usually in the body and linked discussion, not the title |
| "It probably means this" | a guess belongs at the question gate; code written on an unconfirmed guess doubles the rework |
| "Criteria can firm up as I go" | a moving target has nothing to verify against |
| "Out-of-scope is obvious, no need to write it" | an unstated non-goal is exactly where scope creep enters |
| "Start on main, branch later" | the branch comes before the code, not after |
| "Might as well settle the design while I'm surveying" | this step is reconnaissance; design judgment is `purpose-driven-software-design`'s job |

## Related

- `implementation-loop` — consumes the agreed acceptance criteria, scope,
  verification mapping, and working branch, then coordinates implementation to
  convergence without redefining this intake.
- `pr-handoff` — the exit-side counterpart after implementation has converged.
- `purpose-driven-software-design` — hand off here when the survey surfaces a real design decision.
