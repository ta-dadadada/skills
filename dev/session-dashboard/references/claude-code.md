# Claude Code adapter

## Required path

Start a custom or general-purpose background subagent with
[the recorder assignment](recorder.md). Retain its ID. Use the installed version's
subagent continuation/message facility to deliver later submitted report IDs.
Current documentation describes `SendMessage` resuming completed subagents;
check the actual available tool contract. Explore/Plan one-shot agents are not
suitable recorders. Agent Teams is not required.

A resumed recorder applies only assigned reports and owns reflection verification.
Use a minimal completion receipt; the main agent does not reread status or the page.
Surface only failures needing a decision. See [execution permissions](execution-permissions.md).
Run each documented command separately: compound shell commands can exceed
a narrowly granted command permission even when each dashboard operation is allowed. A
user-cancelled recorder must not be secretly resumed; explicitly create an allowed
replacement if the user still wants the dashboard, or report the stopped state.
Use a supervised background shell process for `serve`; preserve its handle and
open the printed loopback URL. Do not assume subprocesses survive session exit.

## Sandbox refusal

Distinguish Bash permission denial from filesystem/network sandbox refusal using
the returned error. Use the sandbox-provided temporary directory for disposable
files, and the project session directory for durable files. Read-only skill scripts
need not write beside their canonical source.

If a necessary operation cannot run sandboxed, use the installed Bash tool's
`dangerouslyDisableSandbox` retry only when exposed and allowed; it goes through
the host permission flow. If `allowUnsandboxedCommands` is false, do not toggle it
or change exclusions to defeat the restriction. Return the blocked operation and
continue unaffected work. Background permission handling depends on the host; if
it cannot prompt, forward one concrete request to the foreground owner rather than
relaunching the same failing recorder.

Official sandbox guidance checked 2026-09-28:
[Sandboxing](https://code.claude.com/docs/en/sandboxing).

## Optional automatic observations

A Claude Code settings overlay can attach command hooks to `SubagentStart` and
`SubagentStop`. A tool-specific skill wrapper may register session hooks as well;
keep those fields out of the portable SKILL.md. Each command runs the absolute
script path with `--directory` set to this session directory and command `hook`.
Quote paths using the actual host shell and merge handlers with existing settings.
Limit them to the activated session, using the runtime's session-ID check.

Only IDs, type, start/response-stop and receipt time are recorded. Built-in internal
agents may also emit stop events; display them as observations, not assigned work.
A stop hook is not necessarily the delivered report. Main-agent snapshots supply
assignment, results and acceptance. Hooks must never spawn a recorder or ask an
agent to continue. No hook may grant permissions or answer human requests.

## Evidence boundary

Document the tested version and host. If background work, continuation, hooks or
permissions are missing, retain the durable report and state the exact limitation.
Do not describe fixture events as real host observations.

Official sources consulted 2026-09-27:
- [Subagents and resumption](https://code.claude.com/docs/en/sub-agents)
- [Hook lifecycle](https://code.claude.com/docs/en/hooks)
- [Skill hooks and portability](https://code.claude.com/docs/en/skills)
