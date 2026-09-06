---
name: session-goal
description: >-
  Persist the goal at the start of a development session, including clear requests, or when the purpose drifts. Save an explicit goal without reconfirmation; clarify competing or ambiguous goals first. This skill saves the goal before requested implementation; it does not implement changes itself. Not for acceptance criteria, work plans, or an in-flight handover.
license: MIT
compatibility: >-
  Step 1 may use the gh CLI when a material is a GitHub issue; absent
  gh, ask the user to paste the content. Step 4 uses read-only git
  commands and edits .gitignore; in a directory git does not manage, the
  git-dependent parts are skipped.
metadata:
  author: ta-dadadada
---

# Session Goal

One session serves one goal — about one PR's worth — and the goal is the user's decision: an explicit user goal supplies that decision; the agent asks only when a consequential choice remains unresolved. The goal states Why (whose problem, what value) and What (what is different when the session succeeds); How starts only after the goal is pinned, in other skills. Incidental work — minor bug fixes, clearing blockers, refactoring, tests, docs, dependency updates — rides along in the session freely, and enters the goal only when it is itself the session's purpose. The confirmed goal is persisted outside the session so an interruption cannot erase the purpose, in words a reader who never saw the session understands.

## When to use

- Starting a development session.
- The opening prompt is vague, or names several candidate goals.
- Mid-session drift calls for re-pinning what this session is for.

## When not to use

- Acceptance criteria, work plans, landing-zone surveys, branches — that is `issue-kickoff`, run after the goal is pinned.
- Snapshotting in-flight work for a later session — that is `session-handover`.
- Sessions with nothing to pin: one-off questions, exploration with no intended change.

## Workflow

### Step 1 — Read what the user supplied

- Read every material the user pointed to before anything else: `gh issue view` for issue references, the file itself for local paths, the conversation for verbal requests. Record unreadable material; ask only when the goal depends on information unavailable from the other supplied sources.
- Light project reconnaissance is allowed exactly as far as understanding the goal requires — enough to phrase the goal and the Step 2 questions in the project's own terms. Surveying code for implementation belongs to the skills that run after this one.

**Done when:** every user-supplied material is read or recorded as unreadable, and reconnaissance stayed within what phrasing the goal required.

### Step 2 — Assess candidates and ask

- State the candidate goal(s) at the level supported by the request and materials. Why/What are a content check, not mandatory separate headings: when the requested outcome already expresses its value, use one sentence. Apply this evidence rule to commentary and questions as well as the saved file. For example, "make the export open in a spreadsheet" supports that desired outcome, not a claim that users currently suffer corrupted characters or broken columns. Omit unsupported background rather than supplying it to complete a template.
- Ask only when saving a faithful goal now would require choosing between materially different purposes, scopes, constraints, or authority boundaries supported by the request or evidence. Missing implementation detail or a hypothetical alternative is not such a choice. Preserve the user's level of scope: an unnamed component, an empty project directory, or possible additional components does not require deciding implementation coverage before saving. Defer those details to the workflow that needs them.
- Resolve factual gaps through relevant supplied evidence and focused read-only reconnaissance where useful. Batch remaining blocking questions for the user and wait before making dependent decisions. Reuse answers and authorization already given in the session.
- A prompt carrying several goals gets presented as a split: name each candidate using the supplied wording and ask which one this session takes. Keep underspecified candidates visible without inventing their background. Missing Why/What detail is a question only if it prevents choosing or faithfully saving the goal; do not append implementation-detail questions for candidates not yet selected. Running goals in parallel happens only when the user explicitly chooses it.
- Work of the incidental kind (minor bug fixes, blocker fixes, refactoring, tests, docs, dependency updates) named in the prompt is presented with its default classification — accompanying work — plus, when the prompt leaves the intent undetermined, one question confirming whether the user means it as the session's purpose itself.
- When the prompt and materials already pin a single clear goal, treat it as confirmed and continue through statement writing and persistence without another approval. No question needed does not mean no goal file needed.

**Done when:** exactly one goal — or a set the user explicitly chose to run in parallel — is stated as Why/What, and no choice needed to save it faithfully is unanswered. An explicit goal proceeds through Step 3 statement writing and Step 4 persistence even when later implementation details remain open.

### Step 3 — Write the statement; confirm only unresolved choices

- Write the goal statement to these rules: Japanese; at most 3 lines; at most 140 characters per line; the essence, stated short and plain. Official names only — the statement outlives the session, seeds the PR description, and is read by people who never saw this conversation.
- The statement carries Why/What. Agent-selected design choices and implementation plans stay out. Preserve explicit user requirements in observable form ("opens in Excel as is"). Required technologies, formats, or numeric limits remain constraints: include them in the statement when they define success, or in the Constraints section below, without treating them as optional design choices.
- Before presenting, check every factual claim in the statement — frequencies, quantities, actors — against the source's own wording; a generalization the source does not state gets corrected to the source's terms or becomes a question. Several quantity mentions may merge into one expression as long as it stays within what the source states — at or above its stated lower bound, claiming nothing beyond it.
- If the statement faithfully captures an explicit user goal or an answer already given, proceed to persistence without asking again. Confirm only a remaining choice or proposed change to purpose, scope, constraints, or authority; amend from the answer before saving.

**Done when:** the statement meets the format rules and traces to an explicit user goal or answers resolving its consequential choices.

### Step 4 — Persist outside the session

- Determine the project root (`pwd`) and whether it is git-managed (`git rev-parse --is-inside-work-tree`); take a timestamp (`date -Iseconds`) and, in a git repository, the current branch.
- Write `<project root>/.agent-goal.md` as a full overwrite:

```markdown
# Session Goal

_<ISO8601> | branch: `<branch>`_

<the confirmed statement, at most three lines>

## Constraints

<Explicit user constraints not carried in the statement; omit when empty.>
```

- In a non-git directory the header carries the timestamp alone, with the branch field left out. When the user explicitly chose parallel goals, write one statement block per goal, each within the three-line rule.

- Keep the file out of version control: read `.gitignore`, and when no line equals `.agent-goal.md`, append it once (creating `.gitignore` when absent). The file becomes tracked only on the user's explicit instruction. In a non-git directory, writing the file is enough.
- Report the written path and what happened to `.gitignore` (appended, already present, or skipped as non-git). Pass the goal and constraints to the next requested workflow; saving the goal does not complete an implementation request.

**Done when:** the file at the fixed path carries the confirmed statement and all explicit user constraints (in the statement or Constraints section), the `.gitignore` entry exists exactly once (or the directory is non-git), and the path was reported. When further work was requested, its workflow receives the saved goal and constraints.

## Red flags

| Rationalization | Reality |
|---|---|
| "Every unstated detail needs a question" | ask about unresolved consequential choices; preserve an explicit goal without reconfirming it |
| "The goal is clear, so skip intake" | clear goals still need the statement and persistence; skip redundant questions, not the file |
| "This bug fix might as well join the goal" | incidental work rides along in the session; the goal stays one PR's worth |
| "Two asks — I'll fold them into one goal" | splitting or running in parallel is the user's call; present the split and ask |
| "While I'm at it, here's the implementation idea" | the goal fixes Why/What; How begins after confirmation, in other skills |
| "The goal is clear in my head, skip the file" | an interrupted session loses its head; the file is what survives |
| "Session shorthand is fine for the statement" | the statement lands in a PR description read by strangers; official, plain words only |

## Related

- `issue-kickoff` — the next step after the goal is pinned: acceptance criteria, question gate on scope, landing-zone survey, branch, and plan.
- `session-handover` — the exit-side counterpart; `.agent-goal.md` feeds its Goal section when a session is interrupted.
- `pr-handoff` — the statement seeds the PR description on the way out.
