---
name: skill-opportunity-review
description: >-
  Propose-only, four-verdict audit of a finished work session for durable
  skill opportunities: reconstruct the session's goal, decisions,
  corrections, failures, and verification; keep only lessons carrying
  reusable execution value, not mere knowledge; walk a preservation
  ladder that prefers improving an existing skill over creating a new
  one, and documentation over a new skill; then deliver in chat exactly one
  verdict per candidate — improve an existing skill, new skill
  candidate, document or memo, or no proposal — each backed by session
  evidence, creating and modifying nothing. Use near the end of a
  session that involved long trial-and-error, a novel problem solved, a
  significant design decision, or friction with an existing skill, or
  when the user asks whether the session yielded anything worth
  preserving. Not for routine sessions without such a signal, not for
  writing the PR story (pr-handoff), not for snapshotting in-flight work
  (session-handover), and not for creating or editing skills
  (shiranui-hanten).
license: MIT
metadata:
  author: tadaair
---

# Skill Opportunity Review

A skill is justified by **reusable execution value**, not by the existence of knowledge gained in the session. A lesson earns skill form only when it would improve a future agent run in a concrete way: sharper judgment at a decision point, a missed step prevented, an investigation made cheaper, a recurring failure blocked, verification standardized, or a critical specialist constraint reliably applied. Everything else — however hard-won — belongs in documentation, a memo, or nowhere. **No proposal** is a first-class verdict: a session that yields nothing skill-worthy ends with that conclusion stated plainly, not with a candidate invented to have something to show. The whole review is propose-only — verdicts land in chat, and no skill file is created or modified.

## When to use

- Near the end of a session that involved long trial-and-error, a novel problem solved, a significant design decision, or friction with an existing skill.
- The user asks whether the session yielded anything worth preserving as a skill.

## When not to use

- Routine sessions without such a signal — this review is not a per-session ritual.
- Wrapping up the change itself for review — that is `pr-handoff`: it records what was done; this skill judges what is worth keeping for future runs.
- Snapshotting in-flight work for a later session — that is `session-handover`.
- Creating or editing a skill — that is `shiranui-hanten`, which takes over after the user accepts a verdict from this review.

## Workflow

### Step 1 — Reconstruct the session

- Gather from the session and its surroundings: the user's stated goal; the work actually performed; decisions adopted and rejected, with reasons; corrections the user issued; failures, rework, and misunderstandings; verification that actually ran; external sources consulted; available memory or work records; and the name and description of every plausibly overlapping installed skill — those whose triggers or responsibilities sit near the session's work — expanding toward the full inventory only when overlap cannot otherwise be ruled out (Steps 3 and 4 judge against this).
- Organize into: Goal / Work performed / Decisions / Corrections / Failures encountered or avoided / Verification / Reusable lessons — a structured reconstruction, not a conversation summary.
- Weight what the session's own trial and error produced over generalities known before it started.

**Done when:** facts, judgments, and guesses are kept distinct, and every reconstruction entry traces to a concrete session event.

### Step 2 — Extract candidate lessons

- A candidate is a lesson with procedural shape. Qualifying forms: a reproducible multi-step workflow; a decision procedure with conditions and branches; a check that prevents a recurring failure; a completion or verification criterion; a blast-radius assessment method for a class of change; a practical procedure spanning multiple tools; a critical specialist-domain constraint; a gap this session exposed in an existing skill.
- Gate every candidate on two questions: which session event produced it, and which future execution improvement it buys. An artifact, a bare fact, a one-off command, a fix to one specific file, a restatement of official documentation, or a problem that occurred once with no evidence it recurs — all fail the gate. Overlap with existing skills is judged at rung 1, not here. A project-specific lesson passes the gate — overriding the exclusion list above — when preserving it would change a future run in this project; rung 3, not this gate, decides its destination.
- A fact restated in imperative mood is not thereby a check. It qualifies as a check only when the session shows the workflow step where an agent skipped or would skip it — a firing condition plus an observable pass/fail, beyond the fact itself. Canonical boundary: "CSV for Excel needs a BOM and CRLF" is a fact; "at contract time, name the consuming program and verify the output opens in it as-is" is the check it becomes when the session shows an agent skipping that step and being corrected.
- Recurrence evidence takes any of three forms: the problem repeated within the session; the same lesson appears independently elsewhere (another project, another skill's rules); or the situation class recurs by its nature (every retry path, every migration). The situation recurring is not enough — the same non-obvious decision, failure mode, or verification burden must also recur.

**Done when:** every surviving candidate names its producing session event and its future execution improvement, and everything that failed the gate is excluded.

### Step 3 — Walk the preservation ladder

For each candidate, take the rungs in order and stop at the first that fits — the order is what keeps the skill set free of duplicates and fragments. Throughout the ladder and Step 4, when a skill's body is unreadable, judge from its name and description and say so in the verdict:

1. **Already covered** by an existing skill → verdict *no proposal* for this candidate; before ruling coverage, read the covering skill's body, and cite the skill and section (when only its name and description are readable, cite those and say so). Covered means the content is reachable when needed: a skill whose trigger would fire in the situation the lesson addresses already carries it. Content sitting in a skill that would stay silent there leaves the candidate uncovered.
2. **Fits as an improvement** to an existing skill — a criterion, check, or red flag its workflow lacks → verdict *improve existing skill*.
3. **Project-specific** → verdict *document or memo*, pointed at the project's own docs.
4. **General knowledge without procedural shape** → verdict *document or memo* (note, ADR, knowledge base).
5. **Independent new skill** — only when every rung above rejected it → verdict *new skill candidate*, carried to Step 4's bar.

When no candidate remains after the ladder and Step 4, the session-level verdict is *no proposal* — a conclusion about the whole review, distinct from the per-candidate *no proposal* of rung 1.

**Done when:** every candidate sits on exactly one rung, and each new-skill candidate records why rungs 1–4 rejected it.

### Step 4 — Evaluate surviving candidates

- Assess each candidate against every criterion, grounded in Step 1 evidence:

| Criterion | Question |
|---|---|
| Reusability | usable in other sessions and other changes? |
| Procedural value | improves execution or judgment, not just knowledge? |
| Distinctness | free of duplication with other skills — and, for a new-skill candidate, a responsibility clearly separate from every existing one? |
| Evidence | effectiveness shown by a session event — a failure, a correction, a decision that worked? |
| Stability | unlikely to go stale quickly? |
| Trigger clarity | the moment to fire it can be stated crisply? |
| Verification | correct execution of the skill is checkable? |
| Scope | one coherent purpose, neither sprawling nor sliver-thin? |
| Maintenance cost | worth keeping current? |

- A *new skill candidate* must additionally clear every bar: awkward as an addition to any existing skill; a clear trigger; multiple steps or decision criteria; verifiable success; survives removal of this session's file names and proper nouns; concretely improves a future agent run.
- **Specialist exception** — for a candidate already on rung 5, weakness on general reusability alone is forgiven when all of these hold (the exception relaxes only the Reusability criterion; a ladder placement on rungs 1–4 stands): getting it wrong causes major outage, security failure, or data loss; correct judgment requires several specialist constraints at once; general coding skills cannot carry it; work in that domain will recur; the knowledge is stable or has a clear update source; skill form would substantially cut investigation or verification gaps. Framework syntax fails this bar; Terraform replace/destroy prediction, DB-migration safety judgment, authz-boundary review, idempotency and consistency checks in distributed work, or API-compatibility and consumer-migration assessment may clear it when the stated conditions hold.
- A candidate that fails is dropped and its verdict downgraded along the ladder — never rescued by softening a criterion.

**Done when:** every candidate has a per-criterion assessment citing session evidence, every surviving new-skill candidate clears the full bar, and every failure is downgraded or dropped.

### Step 5 — Deliver the verdict

- Report in chat under the heading `# Skill Opportunity Review`, with a `## Recommendation` carrying one verdict per surviving candidate, plus one line for each rung-1 candidate naming it and the covering skill and section — and, when nothing survived, the single conclusion that this session yields no proposal, with a short `## Assessment` naming each rejected candidate and the gate or rung that dropped it, one clause each; in that case rung-1 candidates appear in the Assessment only, not twice.
- Candidates landing on the same existing skill merge into one *improve* verdict listing all suggested changes.
- The report carries the verdicts with their evidence cited inline as session events; the Step 1–4 working notes stay out of it.
- An *improve existing skill* verdict carries: the skill name; the opportunity; why it belongs there rather than in a new skill; the suggested change (criteria, checks, or red flags to add); and the session evidence.
- A *new skill candidate* verdict stops short of detailed design and carries: a provisional name; purpose; when to use; why a separate skill, including why rungs 1–4 rejected it; the reusable workflow in outline; session evidence; risks (overlap, over-narrowness, staleness, thin evidence); and a High / Medium / Low confidence. Keep each verdict proportional — no drafted skill body, full workflow, or frontmatter.
- A *document or memo* verdict names the lesson and the destination (project doc, ADR, note, knowledge base).
- When at least one verdict is proposed, close with the handoff: implementation of any accepted verdict goes to `shiranui-hanten` — this review changes nothing itself. A no-proposal session closes on that conclusion alone.

**Done when:** the report follows this format, every claim of reusability or effectiveness cites a session event, and no skill was created or modified.

## Red flags

| Rationalization | Reality |
|---|---|
| "It worked this session, so make it a skill" | one success shows neither reusability nor causation |
| "It's valuable knowledge, so make it a skill" | knowledge may belong in docs; a skill needs execution value |
| "Smaller skills are easier to invoke" | sliver skills multiply trigger collisions and maintenance |
| "It's a bit different from the existing skill" | if an improvement absorbs it naturally, no new skill |
| "It's specialized, so make it a skill" | specialism needs a repeatable procedure, stakes, and a trigger too |
| "I don't want to forget it" | memos and docs also remember |
| "I was asked for candidates, so produce one" | with no qualified candidate, *no proposal* is the correct deliverable |
| "It might be useful someday" | hypothetical reuse cannot fund real maintenance |
| "The session was long, so it must hold value" | effort spent and reusable value are independent |
| "Strip the proper nouns and it generalizes" | surface anonymization does not create genuine generality |

## Related

- `shiranui-hanten` — creates or updates the skill once the user accepts a verdict; this review only proposes.
- `shiranui-hansode` — the empirical tuning loop for a skill that exists; friction it surfaces can feed this review.
- `pr-handoff` — the session's *changes* packaged for reviewers; this skill audits the session's *lessons* for future runs.
- `session-handover` — the exit for interrupted work; this review runs at the end of finished work.
