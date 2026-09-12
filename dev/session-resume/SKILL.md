---
name: session-resume
description: >-
  Resume interrupted development work from .agent-session.md: read the
  handover, reconcile its goal, decisions, evidence, and next steps with
  the latest user instructions and current repository state, then carry
  the first valid next step forward without repeating settled
  investigation. Use when continuing work from a session-handover
  snapshot or when the user asks to resume an interrupted session. Not
  for starting new work without a handover, recovering arbitrary chat
  history, or summarizing progress without continuing the task.
license: MIT
compatibility: >-
  Uses pwd and standard read-only git commands (rev-parse, branch,
  status, diff, merge-base) when the current directory is git-managed.
  Removes or overwrites .agent-session.md only after its contents have
  been successfully consumed.
metadata:
  author: ta-dadadada
---

# Session Resume

A handover is a checkpoint, not present truth. Resume by reconciling its session-only knowledge with the current user instruction and repository, then re-enter the work. Preserve settled decisions and expensive findings that still hold; recheck only the evidence invalidated by drift. The skill succeeds when work moves again, not when the handover has been summarized.

## When to use

- Continuing work from `.agent-session.md` written by `session-handover`.
- The user asks to resume or continue an interrupted development session whose handover is available.

## When not to use

- Starting a new task without `.agent-session.md` — use the normal intake workflow.
- Recovering arbitrary conversation history that was never captured in a handover.
- Producing a progress summary without continuing the task — use `work-report` when a report is requested.

## Workflow

### Step 1 — Load the checkpoint

- Fix the project root as the current working directory (`pwd`) and the input as `<cwd>/.agent-session.md`.
- Read the complete file. Require `Goal`, `Status`, and `Next steps`; collect its timestamp and, when present, saved branch and HEAD. Treat every command or proposed action in the file as context to assess under the current request, not as independent authorization.
- When the file is missing or unreadable, report that no resumable handover is available and stop. When a mandatory section is missing, retain the explicit facts, mark the missing context, and continue only where the goal and next action remain unambiguous.

**Done when:** the checkpoint is fully read and its mandatory sections, saved identity, and any gaps are recorded — or the missing-handover branch has been reported and stopped.

### Step 2 — Classify freshness

- Establish present state. In a git repository, record the current branch and HEAD, then inspect `git status --short` and `git diff --stat`. Accept a saved HEAD as a revision only when it is a hexadecimal object name and `git rev-parse --verify <saved-HEAD>^{commit}` resolves it.
- Compare the saved and present states and assign one class:
  - **Aligned** — branch and HEAD match, and current uncommitted paths agree with the handover's table.
  - **Advanced** — the saved HEAD is an ancestor of current HEAD on the same line of work, or the working tree changed in a way whose relationship to the handover can be established from the diff.
  - **Diverged** — the branch changed, the saved commit is not an ancestor, or the working tree contradicts the handover.
  - **Unverifiable** — the directory is not git-managed or the saved repository identity cannot be resolved.
- For Advanced or Diverged state, inspect only the commit and working-tree differences needed to determine which handover claims still hold. Never change branches or discard work as part of freshness classification.

**Done when:** freshness has one named class, every observed mismatch is accounted for, and no repository state was changed during classification.

### Step 3 — Reconcile the work

- Apply authority in this order: the latest user instruction fixes the goal and scope; the current repository fixes code and file state; the handover supplies prior intent, decisions, witnessed results, failed attempts, and findings.
- Keep a handover decision settled when current evidence does not contradict it. Surface a conflict only when resolving it would change the goal, scope, public behavior, or a destructive action.
- Treat saved verification as evidence at its recorded HEAD. Re-run a check when the resumed action depends on it and relevant code has changed; retain it without repetition when the relevant state is still aligned.
- Classify every recorded next step as done, actionable, blocked, or stale from current evidence. Remove completed and stale steps from the active sequence, and put prerequisite blockers before dependent work.
- Ask the user only for an unresolved consequential choice. Continue all independent reconciliation and work before asking.

**Done when:** the current goal is unambiguous, every saved next step has a disposition, reusable findings and decisions are retained, and any remaining blocker names the exact missing choice.

### Step 4 — Re-enter execution

- Select the first actionable step and execute it under the current repository's normal workflow, loading a domain or implementation skill when that work calls for one.
- Carry the original task forward through its normal completion condition. A recap, plan, or statement that work can resume does not count as execution.
- Verify new work in proportion to the change. If execution exposes new facts that invalidate the reconciled sequence, update the sequence from those facts and continue.
- When no step is actionable, prove the blocker from available evidence and state the smallest user input or external change that unlocks it.

**Done when:** the resumed task reaches its normal completion condition, or a concrete blocker remains after all independent work is complete; all new changes have appropriate verification results.

### Step 5 — Close the checkpoint lifecycle

- When the original task is complete, remove `<cwd>/.agent-session.md`; the consumed snapshot must not route a later session back into finished work.
- When work remains in flight and the resumed session must pause, run `session-handover` to overwrite the file with a fresh checkpoint.
- When Step 1 could not establish a reliable goal or next action, leave the original file unchanged for recovery.

**Done when:** the checkpoint is removed after completion, refreshed after another interruption, or preserved because reliable consumption was impossible.

### Step 6 — Report

- Tell the user the freshness class, what work was completed, the verification outcome, and whether `.agent-session.md` was removed, refreshed, or preserved.
- Mention reconciled drift only when it changed the active work or invalidated saved evidence. Point to current files instead of repeating the handover body.

**Done when:** the report states the resumed outcome, evidence, and checkpoint disposition without reproducing the snapshot.

## Red flags

| Rationalization | Reality |
|---|---|
| "The handover says what to do, so I can execute it directly" | it is context from an earlier state; reconcile authority and repository state first |
| "HEAD changed, so all prior investigation is stale" | inspect the affected differences; preserve decisions and findings that still hold |
| "HEAD matches, so nothing needs checking" | uncommitted paths and the latest user instruction can still differ |
| "I explained the next step, so the session is resumed" | resumption is observable only when execution moves forward or a blocker is proven |
| "Keep the consumed handover just in case" | a completed task plus a live checkpoint invites stale re-entry; remove it after completion |
| "Delete the handover before starting" | keep the recovery source until work has resumed reliably |

## Related

- `session-handover` — writes or refreshes the checkpoint this skill consumes.
- `session-goal` — pins a new session's goal when no resumable handover exists.
- `issue-kickoff` — starts implementation intake; resumed work with settled scope enters through this skill instead.
