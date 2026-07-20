---
name: session-goal
description: >-
  Goal-first session intake: pin a development session to one confirmed
  goal — one session, one goal, about one PR's worth — before any
  planning or code. Read the materials the user pointed to (issue URLs,
  local files) first, do only the light project reconnaissance the goal
  needs, turn every remaining gap into questions instead of guesses,
  keep the goal at Why/What with How left out, get the user's
  confirmation, then persist the goal as a Japanese statement of at most
  three lines in .agent-goal.md at the project root (kept out of version
  control) so an interrupted session's purpose survives and later
  transfers into the PR description. Use at the start of a development
  session, when the opening prompt is vague or names several candidate
  goals, or when mid-session drift calls for re-pinning the purpose. Not
  for acceptance criteria, work plans, or branching (issue-kickoff), not
  for design or implementation proposals, and not for snapshotting
  in-flight work (session-handover).
license: MIT
compatibility: >-
  Step 1 may use the gh CLI when a material is a GitHub issue; absent
  gh, ask the user to paste the content. Step 4 uses read-only git
  commands and edits .gitignore; in a directory git does not manage, the
  git-dependent parts are skipped.
metadata:
  author: tadaair
---

# Session Goal

One session serves one goal — about one PR's worth — and the goal is the user's decision: the agent supplies assessments, candidate framings, and questions, and the user picks. The goal states Why (whose problem, what value) and What (what is different when the session succeeds); How starts only after the goal is pinned, in other skills. Incidental work — minor bug fixes, clearing blockers, refactoring, tests, docs, dependency updates — rides along in the session freely, and enters the goal only when it is itself the session's purpose. The confirmed goal is persisted outside the session so an interruption cannot erase the purpose, in words a reader who never saw the session understands.

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

- Read every material the user pointed to before anything else: `gh issue view` for issue references, the file itself for local paths, the conversation for verbal requests. A material that cannot be read is recorded as unread and joins the Step 2 questions.
- Light project reconnaissance is allowed exactly as far as understanding the goal requires — enough to phrase the goal and the Step 2 questions in the project's own terms. Surveying code for implementation belongs to the skills that run after this one.

**Done when:** every user-supplied material is read or recorded as unreadable, and reconnaissance stayed within what phrasing the goal required.

### Step 2 — Assess candidates and ask

- State the candidate goal(s) from the prompt and materials as Why and What, in plain language. Where the information runs out, the sentence stops — the gap becomes a question.
- Ask the user every blocking question, individually numbered, before guessing and before investigating deeper; the reconnaissance budget of Step 1 is already spent. Present assessments and options for the user to decide on, and wait for the answers.
- A prompt carrying several goals gets presented as a split: name each candidate, ask which one this session takes. Every candidate stays in the split however underspecified it is — its missing Why/What halves point at the numbered questions. Running goals in parallel happens only when the user explicitly chooses it.
- Work of the incidental kind (minor bug fixes, blocker fixes, refactoring, tests, docs, dependency updates) named in the prompt is presented with its default classification — accompanying work — plus, when the prompt leaves the intent undetermined, one question confirming whether the user means it as the session's purpose itself.
- When the prompt and materials already pin a single clear goal, this step is a pass-through: no questions invented for form's sake.

**Done when:** exactly one goal — or a set the user explicitly chose to run in parallel — is stated as Why/What, and no blocking question is unanswered.

### Step 3 — Write and confirm the statement

- Write the goal statement to these rules: Japanese; at most 3 lines; at most 140 characters per line; the essence, stated short and plain. Official names only — the statement outlives the session, seeds the PR description, and is read by people who never saw this conversation.
- The statement carries Why/What. Design choices, file names to touch, and implementation approach stay out. A requirement the sources state from the user's viewpoint stays in the What in its observable form ("opens in Excel as is"); naming a mechanism or technology — an encoding, a library, a retry count — makes it How and keeps it out.
- Before presenting, check every factual claim in the statement — frequencies, quantities, actors — against the source's own wording; a generalization the source does not state gets corrected to the source's terms or becomes a question. Several quantity mentions may merge into one expression as long as it stays within what the source states — at or above its stated lower bound, claiming nothing beyond it.
- Show the statement to the user and get confirmation; amend until confirmed — the goal is decided by the user, held by the agent.

**Done when:** the statement meets every format rule and the user has confirmed it.

### Step 4 — Persist outside the session

- Determine the project root (`pwd`) and whether it is git-managed (`git rev-parse --is-inside-work-tree`); take a timestamp (`date -Iseconds`) and, in a git repository, the current branch.
- Write `<project root>/.agent-goal.md` as a full overwrite:

```markdown
# Session Goal

_<ISO8601> | branch: `<branch>`_

<the confirmed statement, at most three lines>
```

- In a non-git directory the header carries the timestamp alone, with the branch field left out. When the user explicitly chose parallel goals, write one statement block per goal, each within the three-line rule.

- Keep the file out of version control: read `.gitignore`, and when no line equals `.agent-goal.md`, append it once (creating `.gitignore` when absent). The file becomes tracked only on the user's explicit instruction. In a non-git directory, writing the file is enough.
- Report the written path and what happened to `.gitignore` (appended, already present, or skipped as non-git).

**Done when:** the file at the fixed path carries the confirmed statement, the `.gitignore` entry exists exactly once (or the directory is non-git), and the path was reported.

## Red flags

| Rationalization | Reality |
|---|---|
| "The prompt implies it well enough" | a gap is a question to the user; a session built on a guessed goal is the most expensive rework there is |
| "Digging further will answer it" | reconnaissance serves phrasing the goal; what it leaves open goes to the user first |
| "This bug fix might as well join the goal" | incidental work rides along in the session; the goal stays one PR's worth |
| "Two asks — I'll fold them into one goal" | splitting or running in parallel is the user's call; present the split and ask |
| "While I'm at it, here's the implementation idea" | the goal fixes Why/What; How begins after confirmation, in other skills |
| "The goal is clear in my head, skip the file" | an interrupted session loses its head; the file is what survives |
| "Session shorthand is fine for the statement" | the statement lands in a PR description read by strangers; official, plain words only |

## Related

- `issue-kickoff` — the next step after the goal is pinned: acceptance criteria, question gate on scope, landing-zone survey, branch, and plan.
- `session-handover` — the exit-side counterpart; `.agent-goal.md` feeds its Goal section when a session is interrupted.
- `pr-handoff` — the statement seeds the PR description on the way out.
