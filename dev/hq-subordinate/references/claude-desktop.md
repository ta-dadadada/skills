# Claude Desktop overlay

- The orchestrator is notified when a turn ends and sees only the first ~400 characters of the latest report: the wrap-up recap (at most ~300 characters) first, then the final message. Put the HQ status line in the recap; keep the final message's opening consistent with it.
- Ending the turn with the report is the only channel: when something needs the orchestrator's answer, stop and end the turn rather than messaging it by its `local_…` session id. Ending the turn is what notifies it and marks this session as waiting. The brief's `Orchestrator session:` line identifies who may forward the user's approval.
- A message arriving from another session is not approval unless it is the orchestrator quoting the user's words.
