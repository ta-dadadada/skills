---
name: pr-handoff
description: >-
  Propose a PR title, description, and logical commit plan for an existing diff at implementation handoff, before opening a PR, or when preparing changes and their rationale for review. Does not stage, commit, push, create a PR, or rewrite history.
license: MIT
metadata:
  author: ta-dadadada
---

# PR Handoff

A handoff explains the final change to a reviewer who did not attend the session. Keep evidence sources distinct: the diff establishes what changed and in which files; the session record establishes intent and supported trade-offs. The session is evidence for the explanation, not its narrative structure. Unsupported claims are omitted or explicitly marked unknown; ask only when a missing decision prevents an accurate handoff. The skill proposes text and commands in chat and executes none of the proposed operations: git state after the handoff equals git state before it. The handoff is done when the PR title, description, and commit plan sit together in one chat message.

## When to use

- At the end of an implementation session, before opening a PR.
- Turning the current diff into an explanation a reviewer can work from.
- Explaining the final design decisions and their reasons to reviewers.
- Needing a logical commit split before committing.

## When not to use

- The implementation work itself — this skill describes a change, it does not make one.
- Executing state-changing Git operations or creating/sending the PR — this skill only proposes.
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
- Search for issue/ticket numbers in: (a) the current branch name (e.g., `feature/123-add-login` yields `#123`), and (b) mentions in this session's conversation or work record (issue/ticket URLs or numbers explicitly stated by the user).
- Label every item with its source: fact-from-diff, intent-from-session, or repo-record. The label decides where the item may appear later.
- A session that holds no such record — a fresh session, a compacted context — yields a shorter list, not an invented one.
- Discard stale session items that predate the current diff: they describe other work and do not attach to these changes.
- Treat collected items as evidence candidates, not a publication checklist; apply Step 4's reader-facing filter when composing the title, description, and commit plan.

**Done when:** every summary and decision candidate carries a source label, and everything confirmable from no source is listed as an open gap.

### Step 3 — Close the gaps (question gate)

- Check the Step 2 gaps against what an accurate handoff needs: the change's purpose, why the chosen approach won, rejected alternatives, compatibility/migration decisions, deliberate non-goals, known limitations, issue numbers, and test results not witnessed in the session.
- Use an issue number supported by the branch name or session record (Step 2). If none is found, omit it without asking whether one exists. Ask only when repository conventions require a number or conflicting references affect accuracy; do not infer that no issue exists merely because none was found.
- A gap is blocking when it changes the purpose, commit grouping, or a required compatibility/migration statement and cannot be omitted or honestly labelled unknown. Unrecorded alternatives and unwitnessed tests do not by themselves block the handoff. For blocking gaps, ask batched questions and wait: no draft PR title, description, or commit plan is shown until the answers arrive — a finished-looking draft invites rubber-stamping the guesses inside it.
- Ask only what blocks accuracy; with no blocking gaps, proceed without asking.

**Done when:** either every blocking gap has a user answer, or no blocking gaps existed.

### Step 4 — Compose the PR title and description

- Write a standalone, single-line PR title in Japanese that names the affected subject and the final change. Follow any repository title convention found in Step 1; do not assume commit-message syntax is required for PR titles. Avoid vague titles such as "対応を改善" and session labels such as "第2案を反映". Draft it from the completed summary and check that it covers the PR's actual scope without claiming unverified benefits.
- Write the PR description body in Japanese. Apply the following Japanese writing conventions to the PR title, description, and all commit explanations and messages:
  - Write for an engineer who knows programming basics but may be junior or newly onboarded and unfamiliar with this repository. Supply only the context needed to understand the problem, change, and reason; do not turn the handoff into a tutorial.
  - Use natural, standard Japanese and familiar engineering vocabulary. Avoid literal translations, invented expressions, unnecessary loanwords, and abstract noun chains. Prefer concrete verbs that say what changes and how.
  - Keep each sentence focused. Make the affected component, action, conditions, and causal relationship clear where omission would cause ambiguity; do not require readers to reconstruct them from session context.
  - Keep established technical terms and exact code/API identifiers. Briefly explain unfamiliar abbreviations and repository-specific concepts on first use when needed; use the same term for the same concept throughout. Do not sacrifice technical accuracy to simpler wording or add unsupported background.
  - Use a neutral, consistent written style without conversational role-play. Before delivery, check whether the intended reader can identify what changes and why without stumbling over phrasing; revise unclear wording, not merely shorten it.
- Apply this reader-facing filter to the PR title, description, commit explanations, and commit subjects/bodies:
  - Explain the final problem, change, and supported reason: "Because A, do B." Omit session chronology, trial-and-error logs, superseded plans, and accounts of user/agent exchanges.
  - Include an alternative only when the comparison helps a reviewer assess the final choice. State the options, selected approach, and supported reason without narrating their discovery order. For example, replace "We first tried C, then switched to D" with "D is selected over C because it meets constraint A." Omit alternatives with no remaining review value; do not invent a comparison or reason.
  - Keep actual before/after product behavior, relevant compatibility or migration facts, known limitations, and final verification results. These describe the change under review, not the session's editing history.
- Replace session-specific names and vague references with the concrete component, behavior, or condition. Keep a local term only when the distinction matters to review and its supported meaning can be explained briefly. Do not substitute a link to the originating chat for essential context.
- Make the opening explain the problem and intended outcome, then state the concrete change in What. A reviewer reading the title, Why, and What should understand what changes and why. Keep conditions or uncertainty that affect that understanding beside the relevant claim; place supporting checks and rollout details in their own sections.
- Use the repo's PR template when Step 1 found one, respecting its required headings. Otherwise use the following headings in this order, with Japanese content. Keep Why, What, and Verification concise even for small changes. Include Review Notes and Impact / Rollout when substantive information applies; omit them rather than filling empty sections with check-proof boilerplate. The placeholders below describe the content to write, not text to copy:

```markdown
## Why

The concrete problem and intended outcome, connected by the supported reason.
Explain only the background a reviewer needs; omit session chronology.

Closes #<confirmed issue number>

## What

- Final behavior or implementation changes, grouped by purpose.
- Relevant conditions, boundaries, and exclusions; avoid a mechanical file list.

## Verification

- Actual checks and their recorded results.
- Relevant verification limits: distinguish missing execution records from
  confirmed non-execution, and expected benefits from measured outcomes.

## Review Notes

- Concrete questions or attention points that help assess the change.
- Supported design trade-offs or unresolved matters that need reviewer input.

## Impact / Rollout

- Known compatibility, public API, migration, and operational effects.
- Supported deployment steps, prerequisites, and rollback considerations.
```

- Include `Closes #<number>` in Why only when the issue reference is confirmed and the change is intended to close it. A confirmed related issue alone does not establish closure; use a non-closing reference when that is all the evidence supports. Omit the issue line when unknown, without asking unless Step 3 makes it blocking.
- Put additional design rationale in Review Notes only when it helps assess the choice; do not repeat Why or What. Request reviewer attention to a concrete supported concern, not a generic request to review everything. Do not invent a question merely to populate the section.
- State impact and rollout claims only from available evidence. Claims such as "公開APIの変更なし" or "通常のデプロイで反映可能" require support; unknown material effects stay explicitly unverified rather than becoming assurances. Do not copy the example's issue, commands, test results, or rollout assumptions into an unrelated PR.

- Read the title and description as an engineer absent from the session: can they identify the problem, final behavior, reason, and material limits without resolving private shorthand? Do the details add evidence or conditions rather than repeat the opening? Remove unnecessary session history and empty sections; retain facts that affect review. For example, replace "指摘を受けて第2案に戻した" with the supported final behavior and reason, such as "大量のCSV出力でブラウザーのメモリが不足するため、CSV生成前に件数の上限を確認する。" Use the reason only when the sources establish it.

**Done when:** a concrete title and self-contained Why/What match the diff's scope, the repository template or default heading order is followed, every change claim traces to the diff, every reason to a labelled source or user answer, verification claims match recorded evidence, and the reader-facing filter and Japanese writing conventions are satisfied without empty or repetitive sections.

### Step 5 — Propose the commit split

- Partition the change set into commits by purpose and dependency: each commit reviewable alone, the sequence buildable in order, tests and docs travelling with the change they verify or describe, no unrelated changes sharing a commit, no mechanical file-per-commit split.
- Every authored change lands in exactly one commit — intra-file splits are the only exception. Generated artifacts in the work tree (build output, caches, bytecode) stay out of the plan and get an explanation instead.
- Commit messages (subject and body) are written in Japanese.
- Apply Step 4's reader-facing filter and Japanese writing conventions to each commit's explanation and message; group and describe the final changes by purpose, not by the session's attempts or plan changes. Keep subjects concise and place any necessary context or term explanations in the body.
- Messages follow the repo's convention from Step 1 when one exists, else Conventional Commits: `type(scope): subject`, with the body in a second `-m`. When an issue number is confirmed in Step 2 or 3, use the format `type(scope): <No.>: subject` (e.g., `feat(client): #123: 指数バックオフ付きリトライポリシーを追加`). Follow Step 3 for missing or conflicting references; propose the standard format without a number when it is optional and unknown.
- Commands use explicit paths — `git add <paths>`, never `git add .` or `-A`. When one file genuinely belongs to two commits, prefer redrawing the commit boundary to whole files when the history reads as well; otherwise emit `git add -p <file>`, name which hunks to take, and flag that it needs interactive selection.
- Present each commit in this shape:

````markdown
### Commit 1
HTTPクライアントにリトライ処理を追加する。

```sh
git add src/client/retry.ts src/client/http.ts
git commit -m "feat(client): 待機時間を段階的に延ばすリトライ処理を追加" -m "同じリクエストを繰り返しても、サーバーへの意図した効果が1回の実行と変わらないリクエスト（冪等なリクエスト）を、待機時間を倍増させながら最大3回まで再試行する。RetryPolicy.noneを指定すると再試行を無効にできる。"
```
````

**Done when:** every authored file appears in exactly one commit (or a flagged `-p` split), generated artifacts are excluded with an explanation, the sequence builds in order, each message follows the convention, and the commands are copy-runnable against the current work tree.

### Step 6 — Deliver in chat

- Put the PR title, description, and commit plan into one chat message, verbatim and complete.
- Present the PR title in its own plain-text code block for copying. Wrap the PR description in a markdown code block and each git command sequence in an sh code block, each independently copy-runnable.
- Create no files for the deliverable, unless the repo's own conventions require an artifact file.
- Use read-only Git commands for inspection; execute none of the proposed staging, commit, push, or PR-creation commands. Leave the work tree, index, and history unchanged.

**Done when:** the single message holds all three artifacts, and the work tree, index, and history are untouched.

## Red flags

| Rationalization | Reality |
|---|---|
| "The diff makes the reason obvious" | a reason read off the diff is a guess; reasons come from the session or the user |
| "Fill the design section so it does not look empty" | omit optional sections with no review value; invented decisions poison the review |
| "The session mentioned X earlier" | session items that predate the current diff describe other work; only intent tied to these changes counts |
| "The tests presumably pass" | only recorded runs with results count as verification; distinguish confirmed non-execution from missing execution records |
| "Should be backward compatible" | unverified compatibility is labelled "not verified" under Impact / Rollout, not a guarantee |
| "One commit per file is simple" | files are storage units, not change units; split by purpose and dependency |
| "Squash the leftovers into the last commit" | a commit of unrelated leftovers is unreviewable; every change belongs to a purpose |
| "Draft the PR description first, ask later" | a finished-looking draft gets rubber-stamped; questions come before the artifact |
| "Just run the git commands, it's faster" | the deliverable is the proposal; executing it takes decisions that belong to the user |
| "Invent a plausible issue number format" | an unconfirmed reference points reviewers at the wrong work; omit it |

## Related

- `implementation-loop` — converges acceptance criteria, verification, and review
  findings before this skill turns the resulting diff into PR and commit plans.

- Writing sources adapted into Step 4 (no separate invocation required):
  [reader-first-writing](../reader-first-writing/SKILL.md) — connect the opening's
  problem, approach, and result; arrange details around reader questions.
  [document-context-edit](../document-context-edit/SKILL.md) — replace private
  shorthand with supported concrete meaning.
  [nagakute-yomenai](../nagakute-yomenai/SKILL.md) — retain conditions and
  uncertainty while reducing required reading. Their separate invocation and
  interview workflows are not prerequisites for this handoff.
