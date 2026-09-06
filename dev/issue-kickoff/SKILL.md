---
name: issue-kickoff
description: >-
  Prepare acceptance criteria, a working branch, and a verification plan when starting implementation from an issue, ticket, or verbal request. Reuse agreed goals and criteria. Not for implementation itself, deep design, or resuming work with agreed acceptance criteria.
license: MIT
compatibility: >-
  Step 1 may use the gh CLI when the work source is a GitHub issue;
  absent gh, paste the issue content into the conversation.
metadata:
  author: ta-dadadada
---

# Issue Kickoff

What counts as done is agreed before any code is written. Reuse agreed goals, constraints, and criteria. Ask about unresolved business, scope, authority, or compatibility decisions; evidence-based routine choices stay within the agent's discretion. Scope is fixed by naming both what is in and what is explicitly out. The branch and the plan trace back to the issue. This skill ends with the branch and verification plan. For an implementation request, continue into the relevant implementation workflow with those inputs; do not treat this preparation as completion of the user's task.

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
- Restate the requirement in your own words. Record the issue's metadata: number, labels, related issues or PRs — or record that no issue reference was supplied or found. Missing references do not establish that no issue exists; ask only if a required reference or conflict blocks the work.
- Separate the actual requirement from background noise in the source material.

**Done when:** the requirement is restated in the skill's own words and the issue metadata (number, links) is recorded — or the lack of a supplied or discovered reference is recorded without asserting that no issue exists.

### Step 2 — Derive acceptance criteria

- Convert the requirement into checkable acceptance criteria, written as observable behaviour. Label each as stated by the user/source, derived from that evidence, or proposed as a new requirement. Reuse agreed criteria rather than requiring another approval.
- Write an explicit out-of-scope list — what this work will not do.

**Done when:** every criterion is checkable, labelled as stated, evidence-derived, or newly proposed, and an explicit out-of-scope list exists.

### Step 3 — Question gate

- Batch unresolved choices about business behavior, scope, authority, or compatibility that available evidence and delegated discretion cannot resolve. Include newly proposed requirements that would change the agreed outcome. Wait before making dependent decisions; do not present those choices as settled in a final plan. Evidence-derived criteria and routine implementation choices need no separate approval. Continue independent reconnaissance while answers are pending.
- Non-blocking questions get noted in the plan instead of asked.

**Done when:** every blocking ambiguity has a user answer, or none existed.

### Step 4 — Survey the landing zone

- Identify where the change lands: the files it will touch, the existing patterns and conventions to follow, and the tests it affects.
- This is reconnaissance, not design — when the survey surfaces a decision that needs real design work, flag `purpose-driven-software-design` for that part of the plan rather than resolving it here.

**Done when:** the entry files and the conventions to follow are named, and any needed design work is flagged in the plan.

### Step 5 — Branch and plan

- Reuse a working branch already assigned to this task. Otherwise create one following the repository's naming convention (`git switch -c`), including an evidenced issue number when the work ties to one; an optional missing number does not block preparation.
- Deliver the work plan in chat: ordered steps, with each acceptance criterion mapped to the verification step that will confirm it.

**Done when:** the assigned branch is reused or a branch following the repo's convention exists (issue number included when known and applicable), and the delivered plan maps every acceptance criterion to a verification step.

## Red flags

| Rationalization | Reality |
|---|---|
| "The issue title says enough" | the real requirement is usually in the body and linked discussion, not the title |
| "A missing detail must become a question" | distinguish evidence-based routine choices from unresolved business, scope, authority, or compatibility decisions |
| "Criteria can firm up as I go" | a moving target has nothing to verify against |
| "Out-of-scope is obvious, no need to write it" | an unstated non-goal is exactly where scope creep enters |
| "Start on main, branch later" | the branch comes before the code, not after |
| "Might as well settle the design while I'm surveying" | this step is reconnaissance; design judgment is `purpose-driven-software-design`'s job |

## Related

- `pr-handoff` — the exit-side counterpart to this entry-side skill.
- `purpose-driven-software-design` — hand off here when the survey surfaces a real design decision.
