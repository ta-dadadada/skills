# Common-instruction revision — 2026-09-06

## Scope and baseline

Baseline: `f63489cd77f411b1955e15c3de145e9b5a3be2c5` on `main`.
The working revision changes authoring criteria, session-goal, issue-kickoff,
pr-handoff, and evaluation guidance. It retains goal persistence, propose-only
handoff, critical authority/compatibility decisions, and necessary ordering.
UI workflows and runtime implementation were not changed or exercised.

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
after-version texts came from the working revision. The PR fixture used a staged
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
for missing persistence. The goal clarification boundary remains an unresolved
finding for a focused revision and repeat comparison; no tuning was performed
as part of reviewing these results.

## Pending cases and criteria

A focused follow-up revises session-goal Step 2: a question must resolve a choice
needed to save a faithful goal at the user's stated scope. Hypothetical component
coverage and later implementation details do not block persistence. Desired value
can supply Why without inventing current defects or users. Existing competing-goal
confirmation remains required. This addresses an unclear decision boundary; it
does not change invocation or remove goal persistence.

The follow-up compares the preceding working version against this revision for
the original clear-goal case and a boundary case explicitly choosing between CSV
compatibility and login functionality, with parallel work excluded. The first
must save the goal and UTF-8 BOM/CRLF constraints without questioning or coding;
the second must ask for a choice without saving an invented final goal or coding.
Fresh fixtures and a Claude runner are prepared under
`/private/tmp/skills-goal-followup-20260906`.

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

### Grounded candidate framing follow-up

The next focused revision removes the pressure to fill separate Why/What slots:
an outcome that expresses value can stand alone. The evidence rule explicitly
covers commentary and questions, not just the saved statement. Competing goals
are presented in the supplied terms; missing background does not automatically
generate questions, and implementation-detail questions for unselected candidates
are deferred. This changes the existing instruction to turn every missing
Why/What half into a question, rather than adding another contradictory guard.

The same clear-goal and competing-goal fixtures compare the preceding revision
with this version under `/private/tmp/skills-goal-grounding-20260906`. In addition
to the fixed persistence and choice criteria, inspect commentary for unsupported
current defects or actors, and boundary questions for premature implementation
details. Claude execution uses the prepared local runner; results are pending.

Codex CLI 0.153.4 completed the four cells with the same model/settings. Both
clear-goal versions saved the required goal and constraints without a question;
neither introduced current-defect claims in commentary. Both boundary versions
asked for selection without saving. The preceding version additionally requested
the login users/purpose; the revised version asked only which of the two supplied
goals to take. Revised fixture contents confirmed only the goal file was added
in the clear case and no file was added in the boundary case. These single runs
support preservation of the tested boundaries and the narrower question, not a
general reliability claim. Claude framing behavior remains to be checked.

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

Repeat the goal case after resolving the Claude finding; add
the relevant boundary checks below rather than a fixed full-suite run. Record
resolved model, tool version, reasoning settings, permissions, loaded instructions,
fixture, target-text revision/hash, outputs, and metric sources for each pair.

| Case | Required observation |
|---|---|
| Clear goal, explicit technical constraints | No goal reconfirmation; saved goal and constraints; no implementation for an intake-only request |
| Competing goals | A necessary choice is asked; no invented agreement or saved final goal |
| PR handoff, optional unknown issue | Complete description and commit proposal without an issue-number question; work tree/index/history unchanged |
| Required or conflicting issue reference | Ask the necessary question; do not invent a reference |
| Description selection | Clear development starts still select goal intake; one-off factual questions do not; settled in-flight criteria do not restart kickoff; absent diffs do not select PR handoff |
| Structural versus bounded evaluation | Stop at the requested mode; do not edit or start a tuning loop |

Use separate activation/non-activation probes for description changes. Label
tool-free classification, explicit-skill execution, and native discovery as
different evidence. Keep evaluator expectations out of the executor prompt.
Investigate differences within each environment before expanding cases; do not
trade a critical regression for reduced cost. UI comparisons remain deferred until
a concrete UI change or observed defect warrants them.

## Mechanical verification

The full 18-package validator and `git diff --check` passed during this revision.
APM metadata was regenerated from frontmatter using the existing generator.
These checks do not validate model execution or prove cross-tool reliability.
