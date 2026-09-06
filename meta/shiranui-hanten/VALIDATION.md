# Common-instruction revision — 2026-09-06

## Scope and baseline

Baseline: `f63489cd77f411b1955e15c3de145e9b5a3be2c5` on `main`.
The working revision changes authoring criteria, session-goal, issue-kickoff,
pr-handoff, and evaluation guidance. It retains goal persistence, propose-only
handoff, critical authority/compatibility decisions, and necessary ordering.
UI workflows and runtime implementation were not changed or exercised.

## Comparison versions and inputs

Version IDs below identify the exact target `SKILL.md` bytes by SHA-256, including
frontmatter. Claude and Codex target copies matched. G0 and H0 come from the
baseline commit above; G1–G3 and H1 identify the uncommitted snapshots actually
tested. A hash identifies a snapshot; it does not recover missing source text.

| Version | Skill | SHA-256 |
|---|---|---|
| G0 | session-goal | `19944828cd67817b3056b3a99acb8594459a5c460fa8bd2e1a0f66f9f09bb489` |
| G1 | session-goal | `48d23ca0963c33a531deb9b3d39e8f9e7f8064a11947805315f1505f6ea41843` |
| G2 | session-goal | `45b8b863590ddfdbf538abafbfde9b896b3720903906538a9cc8d15d24e646a8` |
| G3 | session-goal | `66f6312ca3722f8efb28d8b2e5c5ff95393372454259bc51f2ee71e09fff51a0` |
| H0 | pr-handoff | `4a8aa922f14d4da25655d816ccba5173b080b550c310ee88e9d34da99a73cc1e` |
| H1 | pr-handoff | `48f59fb9de851bac990e5b8c018282ee73bcfc80c3519086d4939f0c7f28e48e` |

| Comparison | Cases | Before → after | Execution |
|---|---|---|---|
| Initial attempt | C1, C3 | G0 → G1; H0 → H1 | Launch/auth failures; no scenario completed |
| Initial completed comparison | C1, C3 | G0 → G1; H0 → H1 | Codex retry and Claude user-terminal run |
| Persistence boundary follow-up | C1, C2 | G1 → G2 | Both environments |
| Grounded framing follow-up | C1, C2 | G2 → G3 | Both environments |

Exact prompt: concatenate the common preamble, a blank line, and the case text.
Japanese is retained here to preserve the tested input. Each case/version starts
in a fresh directory containing the target snapshot as `TARGET_SKILL.md`.
C1/C2 are non-Git directories with no other initial files. C3 is a Git repository
on `main` with no commits or conventions; only the following `greeting.py` is
staged, and the target instruction is untracked:

```python
def greet(name):
    return f"Hello, {name}!"
```

Common preamble:

```text
作業対象は現在のディレクトリだけです。TARGET_SKILL.mdは今回適用するスキルです。これを読んで次の依頼を実行してください。質問が必要な場合は質問を返して終了してください。TARGET_SKILL.md自体は成果物ではなく、コミット案にも含めません。
```

C1 — Clear goal:

```text
この開発セッションでは、CSV出力をExcelでそのまま開けるようにします。UTF-8 BOMとCRLFは必須です。session-goalを使って目標の整理と保存まで行ってください。実装はまだ依頼しません。
```

C2 — Competing goals:

```text
この開発セッションでは、CSV出力をExcelで開けるようにするか、ログイン機能を追加するか迷っています。両方は扱いません。session-goalを使って今回の目標を整理してください。実装はまだ依頼しません。
```

C3 — Optional issue reference:

```text
pr-handoffを使い、この変更のPR説明とコミット案をチャットで作成してください。セッション記録: 利用者名で挨拶を返す関数が必要だったためgreeting.pyを追加しました。代替案の検討はありません。テストはまだ実行していません。
```

## Static review

- A clear development goal still activates session-goal and reaches persistence;
  only redundant confirmation is removed. Explicit technical requirements survive
  in the statement or its optional Constraints section.
- Ambiguous or competing goals still require a consequential choice to be resolved
  before saving. Routine wording choices do not create an approval requirement.
- PR handoff omits unknown optional issue numbers but still asks about required or
  conflicting references. Proposed Git/PR operations remain unexecuted.
- Issue kickoff reuses agreed inputs and an assigned branch, distinguishes derived
  criteria from new requirements, and hands preparation into requested implementation.
- Structural evaluation ends without executing or editing the target. Bounded
  comparison ends with results; iterative edits require the tuning mode.
- Evaluation accepts equivalent tools and permitted judgment. Critical regressions
  in one environment cannot be offset by average gains elsewhere. Runtime metric
  mappings live in the evaluation skill's environment reference.

These are conclusions from instruction text, not observed model behavior.

## Focused comparison attempt

Prepared isolated temporary fixtures and explicit-skill prompts for two cases:
clear goal persistence with required UTF-8 BOM/CRLF, and PR handoff with an unknown
optional issue number. Before-version texts came from the baseline commit;
after-version texts were G1 and H1 (C1/C3 in the comparison table). The PR fixture used a staged
new function with no commit history. Skill text was supplied explicitly, so even
a successful run would not establish native skill discovery.

| Environment | Settings | Observed result |
|---|---|---|
| Claude Code 2.1.241 | `claude-sonnet-5`, medium, fresh nonpersistent session, safe mode, Read/Write/Edit/Bash with scoped allowances, `dontAsk` | Initial attempt reported not logged in; retry reported expired OAuth credentials that could not be refreshed. No scenario execution. |
| Codex CLI 0.149.1 | Requested `gpt-6-astra`, medium, ephemeral, workspace-write, user config ignored | Initial launch was blocked by the host sandbox. Retry reached the service but failed because Astra requires a newer CLI/app. No scenario execution. |

Neither environment produced a before/after pair in this initial attempt. No behavioral success rate,
time improvement, persistence result, or routing improvement is claimed. Account
settings and installed CLI versions were not changed. Codex also reported inherited
skill/plugin activity; ignoring user config alone did not establish an isolated
skill catalog.

## Codex retry after CLI update

The user updated Codex CLI to 0.153.4. Four fresh executions then completed using
`gpt-6-astra`, medium reasoning, ephemeral execution, ignored user config, and
workspace-write in the prepared temporary fixtures. Target instructions were
supplied explicitly. Inherited skills remained visible; the CLI warned that some
descriptions were shortened to fit its context budget. This is execution evidence,
not an isolated native-discovery test.

| Case | Before | After |
|---|---|---|
| Clear goal with UTF-8 BOM/CRLF requirements | Asked for confirmation of the goal statement and stopped without saving | Saved `.agent-goal.md` without reconfirmation, including both required technical constraints; no implementation |
| PR handoff with optional unknown issue | Asked for an issue/ticket number and stopped without the requested proposals | Produced the PR description and commit proposal without asking for an issue number; accurately reported tests as unrun |

Each cell was executed once. Observable commands and resulting artifacts support
these differences. Both handoff fixtures retained the staged `greeting.py` diff,
no commits or reflog entries, and no observed Git mutation commands. The goal
fixtures were non-Git directories, so this did not exercise `.gitignore` handling.
No reliability rate or cost improvement is inferred from these four executions.

## Claude execution from the user's terminal

The user ran the prepared runner with Claude Code 2.1.263, resolved model
`claude-sonnet-5`, medium effort, safe mode, nonpersistent sessions, and scoped
tool allowances with `dontAsk`. All four processes exited with code 0 and reported
no permission denials. Target hashes matched the copied fixtures. Earlier auth
errors were specific to the agent's execution environment; the user's terminal
completed the runs successfully.

| Case | Before | After |
|---|---|---|
| Clear goal with UTF-8 BOM/CRLF requirements | Asked about the project, additional CSV requirements, and users; did not save | Asked whether hypothetical multiple CSV outputs should all be included or only one; did not save |
| PR handoff with optional unknown issue | Asked for the issue/ticket number and stopped | Produced the PR description and commit proposal without that question; reported tests as unrun |

The goal case fails its required persistence outcome in both versions. The
after-version's question concerns implementation scope not established by the
fixture and not needed to save the explicitly requested goal. It also introduced
character corruption/column-layout problems into its framing without source
evidence. These are observed outputs, not a proven diagnosis of their cause.
No goal file exists in either fixture. Both handoff runs have no changed paths,
including Git files, in the runner's before/after hash snapshots.

Across the two tested environments, handoff improved in both single-run pairs;
goal persistence improved only in Codex. Do not mark the goal revision as passing
across environments. Fewer questions or a normal process exit do not compensate
for missing persistence. At this stage, the goal clarification boundary was unresolved; the completed
follow-ups below address it. No tuning was performed as part of that result review.

## Completed persistence boundary follow-up (G1 → G2)

A focused follow-up revises session-goal Step 2: a question must resolve a choice
needed to save a faithful goal at the user's stated scope. Hypothetical component
coverage and later implementation details do not block persistence. Desired value
can supply Why without inventing current defects or users. Existing competing-goal
confirmation remains required. This addresses an unclear decision boundary; it
does not change invocation or remove goal persistence.

The follow-up compares G1 against G2 for
the original clear-goal case and a boundary case explicitly choosing between CSV
compatibility and login functionality, with parallel work excluded. The first
must save the goal and UTF-8 BOM/CRLF constraints without questioning or coding;
the second must ask for a choice without saving an invented final goal or coding.
The inputs are C1 and C2 above.

Codex CLI 0.153.4 completed all four follow-up cells with the previous settings.
Both versions saved the clear goal with BOM/CRLF constraints, without a question
or implementation. Both versions asked the user to choose between the competing
goals and left the boundary fixtures with only `TARGET_SKILL.md`. The after-version
also asked for a reason if login is selected; this run does not establish that a
later answer would proceed without additional questions. The tested persistence
and competing-goal boundaries were preserved in Codex, each in a single run.

Claude Code 2.1.263 (`claude-sonnet-5`, medium, same runner settings) also
completed all four follow-up cells. Target hashes and goal-file contents were
verified against the shared report. Both clear-goal versions saved the goal with
BOM/CRLF constraints without asking a question or implementing code. Both boundary
versions asked the user to choose and made no file changes. The preceding version
had failed to save in the earlier run but saved in this repeat: the observations
show variability, not a clean causal improvement attributable to this revision.

The revised version still described current character-corruption/column-layout
problems in its clear-goal commentary without evidence; these claims did not enter
the saved goal. Its boundary response also requested optional implementation
details. Thus the tested save-versus-ask outcomes passed in both environments,
but unsupported factual framing remains an observed defect. Do not call the full
revision reliably corrected or all quality requirements satisfied. Invocation,
Git ignore handling, and continuation after a boundary answer remain untested.

## Completed grounded framing follow-up (G2 → G3)

The next focused revision removes the pressure to fill separate Why/What slots:
an outcome that expresses value can stand alone. The evidence rule explicitly
covers commentary and questions, not just the saved statement. Competing goals
are presented in the supplied terms; missing background does not automatically
generate questions, and implementation-detail questions for unselected candidates
are deferred. This changes the existing instruction to turn every missing
Why/What half into a question, rather than adding another contradictory guard.

The same C1/C2 fixtures compare G2 with G3. In addition
to the fixed persistence and choice criteria, inspect commentary for unsupported
current defects or actors, and boundary questions for premature implementation
details. Claude execution used the prepared local runner.

Codex CLI 0.153.4 completed the four cells with the same model/settings. Both
clear-goal versions saved the required goal and constraints without a question;
neither introduced current-defect claims in commentary. Both boundary versions
asked for selection without saving. The preceding version additionally requested
the login users/purpose; the revised version asked only which of the two supplied
goals to take. Revised fixture contents confirmed only the goal file was added
in the clear case and no file was added in the boundary case. These single runs
support preservation of the tested boundaries and the narrower question, not a
general reliability claim. Claude results follow below.

Claude Code 2.1.263 completed the same four cells with the previous runner
settings. Target hashes and saved files matched the shared results. Both clear
versions saved the goal and BOM/CRLF constraints without questions or code changes.
The revised boundary response asked only which supplied goal to select, removing
the preceding version's questions about symptoms, authentication methods, and
users; neither boundary fixture changed.

The revised clear-goal statement adds the desired quality "without character
corruption or column disruption." This is a future quality interpretation of
opening CSV correctly in Excel, not an assertion that such defects currently
exist. Under the agreed allowance for evidence-based routine judgment, do not
score that wording alone as an invented business requirement or current defect.
The commentary also inferred tentatively from the sparse fixture that the CSV
feature did not yet exist; this was unnecessary reconnaissance commentary, not
a fact recorded in the goal. The tested persistence, selection, and narrower
question criteria pass in both environments. Stop this focused comparison rather
than tuning toward verbatim reproduction; native invocation, Git handling, and
multi-turn continuation retain their previously recorded coverage limits.

## Completed scope and remaining coverage

The focused comparisons are complete; no retry of the resolved Claude finding
is pending. C1 persistence, C2 goal selection, and C3 optional-issue handoff were
observed in both environments as described above. These are bounded observations,
not a general reliability claim.

The following were not executed and remain coverage limits, not failed cases or
instructions to repeat the completed comparisons:

| Unverified case | Required observation |
|---|---|
| Required or conflicting issue reference | Ask the necessary question; do not invent a reference |
| Description selection / native invocation | Clear development starts select goal intake; one-off factual questions do not; settled in-flight criteria do not restart kickoff; absent diffs do not select PR handoff |
| Git-managed goal persistence | Save the goal and keep the ignore entry correct without unintended Git changes |
| Continuation after a goal-selection answer | Save the selected goal without restarting resolved questions |
| Full issue-kickoff execution | Reuse agreed inputs and branch, deliver the verification plan, and continue requested implementation |
| Structural versus bounded evaluation | Stop at the requested mode; do not edit or start a tuning loop |

Use separate activation/non-activation probes for description changes. Label
tool-free classification, explicit-skill execution, and native discovery as
different evidence. Keep evaluator expectations out of the executor prompt.
Investigate differences within each environment before expanding cases; do not
trade a critical regression for reduced cost. UI comparisons remain deferred until
a concrete UI change or observed defect warrants them.

## PR review follow-up

Review `5124519759` on PR #7 identified remaining static inconsistencies.
The follow-up makes session-goal's implementation boundary explicit without
excluding implementation requests, retains Step 3 before persistence, and includes
saved constraints and requested handoff in the completion criterion. Kickoff now
records missing references without claiming issue absence. PR handoff's completion
criterion includes unchanged history. Evaluation repeats Steps 2–4 without a new
edit before convergence; the evaluator maps fixes to scoring criteria, and the
canonical rule retains three rounds for high-importance prompts.

The full validator and diff whitespace check passed after these edits. APM was
regenerated and description copies checked. This follow-up received static review
only: earlier G3/H1 execution evidence identifies the pre-follow-up versions and
does not establish model behavior for these later edits. Invocation and tuning-loop
execution remain unverified. Machine-specific paths were already removed in the
record cleanup above.

## Earlier mechanical verification

The full 18-package validator and `git diff --check` passed during this revision.
APM metadata was regenerated from frontmatter using the existing generator.
These checks do not validate model execution or prove cross-tool reliability.
