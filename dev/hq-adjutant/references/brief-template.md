# Brief and session messages

## Brief

The first line is the marker, character for character. The `hq-subordinate` skill keys on it, em dashes included. Fill the sections in this order:

```
HQ brief — task T<n> — follow the hq-subordinate skill
Orchestrator session: <this session's own id>
Goal: <why this task exists, one or two sentences>
Target: <folder or repository, exactly as the user named it>
Deliverable: <what exists when finished: branch with change X, PR, document at path, research note>
Done when: <the user-confirmed checkable criteria, one per line if several>
Authority: pre-authorized: <operations the user explicitly agreed, or "none">; everything else that commits, pushes,
  opens/merges a PR, or sends/publishes externally needs approval via the orchestrator.
Conduct: the user's and this target's usual rules apply as in a session the user started there; language <HQ language> where those rules set none.
Context: <only what the session cannot rediscover cheaply: decisions, related tasks and their branches, pitfalls>
Report: end each turn with the HQ report format.
```

Rules:

- **Fields come from the ledger, not from memory.** Goal, Target, Deliverable, Done when, and Authority must match the task's confirmed ledger fields. If they differ, fix the ledger or re-confirm with the user first.
- **Authority lists operations, not intentions.** Write `push branch feat/x to origin`, not `may push`. Leave out anything the user did not explicitly agree to.
- **Conduct is fixed text** apart from the language code, which is the ledger's HQ language. Do not restate the user's or the project's rules in the brief: the session loads them from their own files, and a copy would drift. Write the brief's free text (Goal, Deliverable, Done when, Context) in that language too; the field labels and the marker line stay as shown.
- **Context stays small.** Name sibling tasks only when they matter: their task ids, targets, and branches, and which of them this task depends on. Never include credentials, tokens, or internal endpoints.
- The template has no line for messaging the orchestrator mid-turn. The session's turn end is its only reporting channel.

## Session messages

The first line must stand on its own, because the receiving session may preview only that line. Templates below show the fixed tokens (`HQ T<n>`, `approval W<k>`, the status-line keywords) in English; write the rest in the HQ language.

**Forwarding an approval.** Quote the user verbatim; the quote is what makes the approval valid:

```
HQ T<n> approval W<k>: the user approved <exact operation>.
User's words: "<verbatim>"
This covers only <exact operation>. Report with the HQ format when done.
```

**Forwarding a decision or review answer.** Same shape: `HQ T<n> decision W<k>: …`, followed by the user's verbatim words.

**Asking for a re-report** (when the `report` receipt came back with `parsed: false`):

```
HQ T<n>: your last turn had no HQ report line. End your next turn with it first:
HQ T<n> <working|waiting-user|blocked|done>: <result>. Needs: <…>. Artifacts: <…>.
```

**Raising a done-criteria gap:**

```
HQ T<n>: not yet done. <criterion> lacks evidence: <what is missing>. Provide it or report blocked.
```
