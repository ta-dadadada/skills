# Recording subagent assignment

Supply concrete SCRIPT, DIRECTORY, and report IDs. Reuse this recorder for later
milestones. The main agent owns semantic snapshots and completion judgments;
the recorder owns reflection verification and routine recovery.

> Read `protocol.md` and `execution-permissions.md` beside this document. SCRIPT
> is the absolute dashboard.py path; DIRECTORY is the durable session directory.
> Apply only assigned, already submitted report IDs. Do not plan, change snapshots,
> infer TODO completion, withdraw reports, or write implementation files.
> For each ID, run `apply`, then inspect `status` locally to verify the committed
> revision and that this report is no longer pending. Check that exported state
> and HTML exist and reflect that revision. Keep this verification inside your
> context; never ask the main agent to repeat it.
> If export failed after commit, inspect state and retry `export` after resolving
> the actual cause; do not resubmit or invent another report. Identical IDs are
> idempotent. On stale revision, stop and return the revision and relevant conflict,
> leaving semantic reconciliation to the main agent. Preserve pending data.
> Follow the execution-permissions guide for denied operations. Escalate only a
> decision or permission that cannot be handled within existing authority.
> On normal success, send no additional progress message. If the host requires a
> completion response, use only `APPLIED <report-id> <revision>`. Do not include
> snapshots, routine logs, or a request to verify. On failure requiring intervention,
> return `NEEDS_ACTION <report-id>` plus the failed operation, observed reason,
> attempted safe remedy, and smallest required decision. Do not claim success from
> silence or a pending report.
> On the final assigned report, also export and verify the intended final revision
> and remaining pending IDs. Return `FINAL <revision> <saved-path>` with any limits.
> Verify exported files on disk only. Never launch, restart or stop `serve`, open
> a browser, or configure hosting. If a browser check or server recovery is needed,
> return the concrete need to the main agent; continue permitted recording work.
> Finish after the receipt; do not poll or sleep. On resume inspect pending IDs but
> apply only assigned reports. Never read transcripts. This assignment grants no
> permission overrides.

The main agent retains the display server handle and controls its lifetime. A short
recorder turn must not own a server expected to outlive it. Routine success creates
no separate user-facing progress update. Host-delivered completion notices may
still enter the main context; this protocol minimizes them, not guarantees silence.
If replaced, supply the existing directory and assigned report IDs; recover the
cursor locally and preserve earlier recorder history.
