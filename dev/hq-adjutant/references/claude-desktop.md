# Claude Desktop overlay

This overlay maps the skill's capabilities to Claude Desktop tools. Tool names may carry host prefixes; check them against the tools you actually have. If a tool's own description contradicts this file, follow the tool and report the difference.

## Capability map

| Capability | Tool | Notes |
|---|---|---|
| Own session id (brief's `Orchestrator session:`) | `get_session` with `"self"` | read once at activation |
| Resolve a named target | `list_start_targets` | before every start in another folder |
| Start a session | `start_session`, `initiation: "user_asked"` | parameters below |
| Propose a session (card) | `start_session`, `initiation: "own_initiative"` | starts only in this session's folder; see constraint 1 |
| Start a proposal the user told you to start | `start_session` with `proposal_id` only | |
| Withdraw a stale proposal | `dismiss_task` | |
| Message a session | `SendMessage` with `to: "local_…"` | the older `send_message` also works |
| List sessions started from here | `list_sessions` with `linked: true` | rows carry `name`, `startedBy` |
| Find any session | `list_sessions` (unfiltered), `get_session` | for unlinked ledger sessions |
| Read a session's latest report | `list_events` (recent transcript, e.g. `limit: 4`) | take its last assistant message; only for unlinked sessions, on a user turn |
| Archive a session | `archive_session` | only after the user's yes in chat |
| Session report arrives | a `<side-sessions-event>` turn | carries the note text |
| End-of-turn box | `wrap_up` (recap, ask, actions); `update_plan` | see "Reply box" |
| Run the CLI and the server | Bash; `serve` with background execution | keep the process handle |

## Platform constraints

1. **No starts on note-triggered turns.** On a turn triggered by a `<side-sessions-event>`, the app refuses `start_session`. The exception is a note turn that arrives right after the user's own turn. A proposal card (`own_initiative`) cannot take `cwd`, so it would start in this HQ folder: unusable for a task that targets another repository. So, for a follow-up or queued launch on a note turn:
   1. Run `wait add --kind launch`.
   2. End the turn with a `wrap_up` ask such as `Launch T4 in <target>?` and a reply button.
   3. On the user's reply, call `start_session` with `user_asked`.

   Use a card only when the target really is this folder. Then put the card's `task_id` in the `launch` wait summary, start it with `proposal_id` when the user says so, and `dismiss_task` it when it goes stale.
2. **Named places only.** `cwd` is allowed only with `user_asked`, and only for a place the user named. Take the folder from `list_start_targets` entries that match the user's name for the target. If there is no match or more than one, ask the user. If a start is refused because the place was not named, ask the user to reply with the target's name, then start.
3. **The ~400-character note.** At turn end you see only the first ~400 characters of a session's latest report: its wrap-up recap (≤ ~300 characters), then its final message. The brief makes the HQ report line come first. Pipe the note text verbatim into `report`.
4. **Linking ends with the adjutant session.** Sessions started by an earlier adjutant session may be absent from `linked: true`. Keep their `local_…` ids in the ledger and look them up unfiltered. Their turn-end notes no longer arrive here. On a user turn, read their recent transcript with `list_events`, take the last assistant message, and pipe it verbatim into `report --session <id>`. If they are absent from every listing, they are archived or deleted, and their state is unknown.
5. **No polling.** No loops, no `sleep`, no scheduled tasks or `/loop`, no watch monitors. The app wakes this session when a started session ends its turn, so `notify_when_idle` and `wake_when_done` are unnecessary.
6. **Quote approvals; archive on yes.** Forward approvals by quoting the user's words. `archive_session` shows its own approval prompt in most modes, but that prompt does not replace the user's yes in chat. Get the yes first, per session.

## `start_session` parameters

- `context: "fresh"`.
- `prompt`: the brief, verbatim.
- `background`: required, at least 80 characters. Give the HQ engagement's goal and how this task fits it, with no secrets.
- `cwd`: resolved per constraint 2. Omit it for this folder.
- `use_worktree: true` for repository work that ends in a branch or PR, so the user's checkout is untouched. Use `false` only when the user wants the work done in the folder as it is, for example a documents folder.
- `name`: `t<n>-<slug>`, `[a-z0-9-]`, at most 24 characters.
- `title`: under 60 characters.
- `permission_mode`: omit it to inherit, or give a lower mode. Never request a higher one.
- Leave model, effort, and output style at the user's defaults unless the user asked otherwise, so the session behaves like one the user started there. A worktree session may lack the main checkout's untracked local instruction files and memory; `hq-subordinate` reads them from the main checkout, so name the main checkout's path in the brief's Context when it differs from the target name.
- Never set `target: "cloud"`, `"ssh"`, `host`, or `environment`; they are out of scope. Use `preset` only for a local preset the user named.
- The result returns the session id. Run `launch T<n> --session <id> --name <name> --cwd <folder>` next.

## Messaging

- `SendMessage` to the `local_…` id. The first line must be self-contained (templates in [brief-template.md](brief-template.md)).
- Desktop sessions return no read receipt. A session in a different permission mode may hold the message for its user's approval. So "sent" does not mean "acted on": the session's next report confirms it.

## Reply box

- `wrap_up` recap, ask, and button labels: in the HQ language. The recap is at most ~300 characters, in the same order as the reply, and starts with the waiting count (for `ja`: `あなた待ち: <n>件`).
- `ask`: one decision, at most 100 characters, for example `Approve W4–W6 as listed?`. List the items themselves, with exact operations, in the closing message. The user may answer per item in text.
- `actions`: at most two buttons. A clicked label is the user's words: quote it, together with the item ids it answered.
- `update_plan` may track this turn's own steps. It does not replace the ledger.

## Server and permissions

- Start `serve --port <N>` with Bash's background execution, keep the handle, and give the user the printed URL. Background processes may not survive the adjutant session's end. That is why activation checks the recorded port once.
- Every CLI call shares the fixed prefix `python3 <abs>/hq.py`. Once per HQ, tell the user they can allowlist that prefix as a Bash permission rule, so updates do not prompt. Do not edit settings yourself unless the user asks. Run each call as its own command: compound commands can fall outside a prefix rule.
