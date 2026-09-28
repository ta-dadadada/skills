# Execution permissions and bounded recovery

Use this guide after an actual denial, or when known host restrictions affect a
planned operation. Task authorization and environment permission are separate.
An environment refusal is not a task defect and does not cancel unrelated work.

1. Identify the operation and denied resource from the result: file write, cache,
   network host, local bind, process launch, or command permission. Missing Python,
   port-in-use, invalid JSON and stale revisions require their own fixes; do not
   classify every nonzero exit as a sandbox refusal.
2. Use an already permitted equivalent when it preserves the boundary: direct
   disposable caches/temp files to host-approved locations; keep durable journal
   and snapshots in the agreed writable project directory. Resolve symlinks when
   diagnosing paths. Run the read-only script with an absolute path and explicit
   writable `--directory`; do not copy or rewrite the skill merely to execute it.
3. If essential access remains unavailable, use the host's supported permission
   request for that exact operation, path or destination. State why it is needed.
   Existing user authorization avoids asking the same intent question again, but
   does not override the host permission decision. Follow the applicable adapter.
4. Retry after a material change such as an allowed path or granted permission.
   Do not loop on the same refusal, disguise a command, switch tools to bypass
   enforcement, alter global permission settings, or expand a loopback server to
   a public bind. Run separately authorized commands separately; do not hide a
   prohibited operation in a wrapper.
5. If denied or unsupported, retain pending reports and continue independent work.
   Recording can proceed without a live server if storage is permitted. If storage
   is blocked, retain the report in an already approved durable location, record
   that it is not reflected, and request only the necessary access. Never invent
   a successful save. Report the operation, reason, safe remedy tried, and remaining
   limit once per unchanged incident.

The recorder handles recording/export denials locally. The main agent handles its
own server launch and user-only approvals. Escalate only what needs that owner's
judgment; successful routine recovery produces only the normal compact receipt.
