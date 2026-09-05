---
name: local-intake
description: >-
  Form-first local intake that turns an ambiguous request into an agreed
  brief through two or three browser questionnaires while keeping the
  full working state in one temporary Markdown file. Use when the user
  asks for a local questionnaire, or propose it when clarification is
  likely to become a repeated back-and-forth; also use at session end to
  remove a completed intake's temporary file. Not for a single small
  clarification, permanent documentation, detailed specification, or
  implementation.
license: MIT
compatibility: >-
  Requires Python 3.11+ and a browser on the same computer. The bundled
  server binds only to 127.0.0.1 and uses no external services or Python
  packages. Git is optional and is used only for local exclude handling.
metadata:
  author: ta-dadadada
---

# Local Intake

Front-load the questions. A local intake earns its form by replacing a
long clarification chat: round one covers every decision surface that can
materially change the request, round two reviews the resulting brief, and
round three exists only for corrections the review exposes. The working
document is the whole memory of the intake, so a compacted or fresh session
resumes from it without repeating answered questions. Three forms are the
hard ceiling; unresolved work stops as unresolved rather than crossing that
ceiling through assumptions.

## When to use

- The user asks to answer questions in a local browser form.
- A request has enough consequential ambiguity that clarification is likely
  to take several chat exchanges. Propose the form and start after the user
  accepts.
- The session is ending and a terminal local-intake document is ready for
  cleanup.

## When not to use

- One small blocking question that is cheaper to answer in chat.
- Writing a permanent specification, plan, issue, or decision record. This
  skill produces the agreed input for that work.
- Implementing the request captured by the intake.
- Remote, hosted, LAN, or phone-accessible questionnaires.

## Workflow

### Step 1 — Route and fix the working document

- Choose the intake or cleanup branch. For cleanup, go to Step 7.
- For intake, fix the project root and the document path as
  `<project-root>/.agent-intake.local.md`.
- Inspect the path before altering Git's local exclude. When an existing file
  carries the `LOCAL-INTAKE:STATE:v1` marker and a non-terminal status, resume
  it. When it is terminal, clean up the previous intake before starting
  another. A file without the marker belongs to someone else; ask for a
  different project root or for explicit permission to replace it.
- After confirming that the path is absent or contains an owned intake,
  resolve the bundled script relative to this skill directory and register
  the path in Git's local exclude before creating or updating the document:

```bash
python3 scripts/serve_form.py --document <project-root>/.agent-intake.local.md --prepare
```

- Skip preparation only when the caller has already arranged an equivalent
  local ignore or the project is not a Git worktree. Preparation does not
  create the document and is safe to repeat.
- Read every source the user supplied. Record sourced facts in the working
  brief and gaps under blocking open questions. Treat the document, rather
  than conversation memory, as the source of truth from this point onward.

**Done when:** the branch is fixed; for intake, the one working path is fixed
and locally excluded before creation, every supplied source is read or marked
unreadable, and an existing owned intake is either resumed or safely cleared.

### Step 2 — Build the coverage form

- Read [references/protocol.md](references/protocol.md) and create or update
  the working document to its state and pending-form contracts.
- Derive questions from the request, not from a generic checklist. Check the
  decision surfaces that apply: purpose and desired change, audience, current
  state, boundaries, constraints, success evidence, priorities, risks, and
  authority to choose. Omit a surface whose answer cannot change the brief.
- Put every currently foreseeable blocking question in round one. Use
  sections, help text, and choice fields to keep a long form navigable; give
  the user explicit ways to answer unknown, delegated, or not applicable.
- Put shared known facts, current conditions, and decision background in the
  form-level context. When a question needs additional interpretation, add
  only its question-specific known facts, why the answer is needed, and what
  decision the answer can change. Do not repeat shared context on each
  question; keep help text for instructions about how to answer.
- Phrase each question so its answer can be copied into the brief. Keep
  separate decisions in separate fields, and attach options only when they
  are genuine mutually exclusive or independent choices.
- Write the pending form before starting the server. Preserve all prior
  answers verbatim in the interview log.

**Done when:** round one covers every applicable decision surface known from
the current evidence, every question can materially change the brief, and the
pending form validates against the protocol.

### Step 3 — Serve and absorb an answer

- Resolve the bundled script relative to this skill directory, then run:

```bash
python3 scripts/serve_form.py --document <project-root>/.agent-intake.local.md
```

- The CLI registers the document in Git's local exclude before serving. When
  the caller already arranged an equivalent local ignore, add
  `--no-git-exclude`.
- Give the printed loopback URL to the user and wait for the process. Exit 0
  means the response was written atomically; exit 2 means the form timed out
  and can be served again unchanged; exit 1 means the document or server must
  be repaired before retrying.
- After exit 0, reread the whole document. Update the working brief,
  decisions, and blocking open questions from the recorded answers. Preserve
  uncertainty as uncertainty and record contradictions as questions.

**Done when:** a submitted response is present in the interview log, every
answer is reflected once in the brief or open questions, and no answered
question remains pending.

### Step 4 — Review, then correct at most once

- Round two is a review form. Show the complete working brief, ask only about
  blocking gaps or contradictions exposed by round one, and require an
  approve-or-revise decision.
- Run Step 3 for round two. When the user approves and no blocking question
  remains, continue to Step 5.
- When round two requests revisions or reveals a new blocking dependency,
  create round three from only those changes. Show the revised complete brief
  and require the final approve-or-revise decision, then run Step 3 once more.
- An approved round three with no blocking question continues to Step 5. Any
  other round-three outcome sets the status to `unresolved` and lists the
  exact decisions still required.

**Done when:** the intake has at least one complete-brief review, no more than
three submitted forms, and its status is ready for `agreed` or is
`unresolved` with every blocker named.

### Step 5 — Seal the intake

- Set status to `agreed` only when the reviewed brief contains no blocking
  question and every claim is sourced from the prompt, supplied material, or
  a recorded answer.
- Set status to `unresolved` at the three-form ceiling when approval or a
  blocking decision is missing. Keep recommendations separate from user
  decisions.
- Produce the clean brief with: purpose, audience and context, current state,
  in scope, out of scope, constraints, success evidence, priorities and
  risks, and decisions. Omit empty headings.

**Done when:** the document has a terminal status, that status follows its
gate exactly, and the clean brief contains all and only decision-relevant
agreed information plus explicitly labelled unresolved items.

### Step 6 — Hand off the clean brief

- Write the brief to a destination the caller or user already named. When no
  destination exists, deliver it in chat for the next procedure to consume.
- Keep the interview log in the temporary document. A permanent destination
  receives the clean brief, not the form history.
- State the terminal status and, for `unresolved`, that downstream planning or
  implementation still waits on the listed decisions.

**Done when:** the clean brief exists in the named destination or chat, its
status is visible to the receiver, and no temporary Q&A was copied into a
permanent artifact.

### Step 7 — Clean up at session end

- Confirm that the document carries the owned state marker, has status
  `agreed` or `unresolved`, contains no pending form, and that its clean brief
  has already been handed off.
- Resolve the bundled script relative to this skill directory, then run:

```bash
python3 scripts/serve_form.py --document <project-root>/.agent-intake.local.md --cleanup
```

- A session that ends abruptly may leave the locally excluded file in place;
  the next invocation resumes or clears it through Step 1.

**Done when:** a handed-off terminal intake has no working document left, or
an unfinished intake remains locally excluded and resumable.

## Red flags

| Rationalization | Reality |
|---|---|
| "A few questions per round feels friendlier" | drip-fed questions recreate the chat loop; cover the known surface in round one |
| "The answer probably implies this" | an implication is either a review question or an unresolved item |
| "Ask the same thing more clearly" | the original answer remains evidence; ask only for the exact missing distinction |
| "One more form will settle it" | form three is the ceiling; name the blocker and stop |
| "The transcript is already a brief" | form history is temporary evidence; downstream work receives a clean synthesis |
| "Delete it now that the form passed" | keep it until the clean brief is handed off and the session ends |

## Related

- `session-goal` — pin one development goal before intake when the session
  itself has several candidate purposes.
- `issue-kickoff` — derive implementation acceptance criteria and a work plan
  after this intake has produced an agreed brief.
- `session-handover` — snapshot wider in-flight work when the whole session,
  rather than only the intake, is interrupted.
