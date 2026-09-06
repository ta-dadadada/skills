# Executor environments

Read this when selecting a launcher or capturing execution metrics. The common
skill owns the requirements, scoring, and stopping rules; this reference maps
available runtime evidence into that contract. Verify options against the
installed tool's help rather than assuming a particular release supports them.

## Shared run record

Record the tool/version, resolved model identifier, reasoning settings, target
revision, fixture, available tools, permissions, loaded instructions, and limits.
Use fresh sessions without authorial history or earlier variant results. Keep
each run's writable fixture separate and preserve identical inputs across a pair.
Capture artifacts, user-facing questions, observable tool actions, final output,
and errors. Do not require private reasoning traces.

Keep native tool-call counts separate from normalized operation counts. A single
shell call may contain several reads or checks; classify observable operations
as read/search, write, verification, or other and record the counting rule. When
the trace cannot support that classification, report N/A rather than inventing it.
Measure elapsed time with a monotonic clock or a documented runtime field, naming
the source. Network retries, permission failures, and unavailable tools are
environment findings, not automatically instruction defects.

## Claude Code

Use a fresh supported agent or noninteractive CLI session. Inspect the installed
CLI help for JSON output, model/effort selection, tool permissions, and control
of inherited customizations. Record the model actually selected and any denied
operations. Avoid treating a permission denial as a question caused by the skill.

Some agent launchers expose `tool_uses` and `duration_ms` in usage metadata.
Preserve these as native metrics only when returned. Otherwise use observable
tool-use events and elapsed wall time; neither field is required to run an eval.
Explicitly record whether user/project skills and instructions were loaded.

## Codex

Use a fresh supported agent or CLI execution with an isolated working directory
and the appropriate sandbox. Inspect installed help for event output, model and
reasoning settings, ephemeral execution, and configuration controls. Keep the
sandbox and available tools consistent across variants.

Capture emitted command/tool events and final artifacts. Do not assume Claude
metadata fields exist or count an orchestration wrapper as equivalent to one
underlying operation. Record inherited skills and instructions when observable;
unknown context is a comparison limit, not an assertion of isolation.

## Scope and unavailable environments

A tool-free description-selection probe measures classification only. An
explicitly supplied skill tests execution after selection, not native discovery.
Label these separately from an installed-skill end-to-end trial.

When authentication, launch, or tracing is unavailable, record the failure and
complete independent checks. Do not change account settings or broaden runtime
permissions merely to make a result look complete. A missing comparison stays
pending; it is not a pass, failure of the instruction, or zero-cost execution.
