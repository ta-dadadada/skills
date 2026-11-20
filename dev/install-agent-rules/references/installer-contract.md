# Installer Contract

The standalone skill package contains a Python installer, manifest, and rule assets. No network, third-party Python packages, distribution repository, or other skill is required at installation time. Supports Python 3.11+ on macOS/Linux. Target roots must already exist.

## Scope and files

- `list`: enumerate the manifest's rule IDs and descriptions without inspecting a destination.
- `--rule ID`: select one manifest entry per operation.
- `--project ROOT`: target `ROOT/.claude/rules/<filename>`.
- `--user`: target `~/.claude/rules/<filename>` using the process user's home.
- State: `.claude/.agent-rules-<id>.json`, containing last installed and pending SHA-256 hashes, schema version 2. Version 1 records remain readable. Version 2 identifies installs using the current destination name.
- Lock: `.claude/.agent-rules-<id>.lock`, persistent and protected by an OS advisory lock. Its presence does not mean an operation is running. Never delete it during use.

The root is resolved to its physical directory. Descendant `.claude`, `rules`, target, state, and lock symlinks are refused; special files are refused. Other rule IDs and project files are untouched. The bundled software-design rule has no `paths` selector and applies throughout the chosen scope. Installing this skill alone does not install its rules. The script does not enable Claude Code, configure other agents, or verify live instruction loading.

## Plan and apply

`plan` reads the bundle, target and state, and emits JSON with a unified diff and deterministic `plan_id`. It creates no directories or files. The identifier binds the operation, rule ID, filename, source bytes, root identity, target and state snapshots. `apply` takes the exact ID with the same options. No agent-written plan file is needed.

The default operation, `install`, covers both first installation and updates:

| Action | Meaning | Apply |
| --- | --- | --- |
| `install` | No rule and no state | Install and record baseline |
| `update` | Rule equals the recorded baseline and bundle differs | Replace and update baseline |
| `unchanged` | Rule already equals bundle | No writes; an unmanaged equal file stays unmanaged |
| `recover` | Interrupted write; rule equals recorded old or pending content, and bundle equals pending hash | Complete interrupted installation |
| `conflict` | Local edits, unmanaged different content, removed managed file, or incompatible interrupted write | Refuse |

With `--operation uninstall`:

| Action | Meaning | Apply |
| --- | --- | --- |
| `uninstall` | Rule equals the recorded installed baseline | Delete that rule and its record |
| `cleanup` | Recorded rule is already absent | Delete only its leftover record |
| `unchanged` | Neither rule nor state exists | No writes |
| `conflict` | Modified/unmanaged rule or pending installation | Refuse removal |

Uninstall compares against the installed baseline, so a newer bundled version does not prevent removal of an unchanged older version. Locks and containing directories remain; unrelated files are never recursively removed. A rule absent after interrupted uninstall can be cleaned up by planning uninstall again. Complete any pending install before uninstalling.

An unmanaged equal file is not silently adopted; a later different bundle conflicts. There is no force, adoption, or automatic merge command. Never delete state to evade detection. Conflict resolution belongs to a separate user action; an agent executing this skill does not alter conflicting files. Replan after the user resolves them.

Output is JSON for operational outcomes/errors. CLI syntax errors and `--help` use argparse text. Exit codes: 0 eligible plan/applied/removed/unchanged; 2 conflict, stale plan, busy installer, or syntax error; 1 invalid manifest/state/path, unsupported platform, or I/O error. Invalid records fail closed without reconstructing ownership history.

## Writes and recovery

Apply rechecks under a per-rule advisory lock, records pending install intent atomically, replaces the target using a same-directory temporary file, verifies bytes, then atomically completes the record. Existing file permissions are preserved. Write failures retain pending intent when already recorded; replan with the same bundle to recover. A completed replacement plus pending metadata can recover without rewriting the rule. Process kills may leave temporary files; the agent must not treat them as rules or alter state manually.

This is not a two-file transaction. Pending state makes install interruptions detectable and recoverable; target-first deletion makes uninstall interruption recoverable through `cleanup`. Cooperative installers serialize, but unrelated editors do not honor the lock. Changes before the final target check are detected; arbitrary external writes in the tiny check/replace window cannot be prevented by advisory locking. Avoid simultaneous editing during apply. Local filesystems are supported; hostile filesystem mutation and network-filesystem lock/durability semantics are outside the guarantee.

Diffs detect conflicts for the selected file/baseline, not semantic contradictions with CLAUDE.md or other instructions.

## Add another distribution

Add a UTF-8 Markdown asset and an entry in `assets/manifest.json` with `asset`, `filename`, and `description`. The rule ID uses lowercase kebab-case; assets and destination names are single Markdown filenames. Each destination filename must be unique. No per-rule Python branch is needed; content, state, locks, and plans remain isolated by rule ID. One command processes one rule, so multi-rule work is explicitly sequential rather than an implicit batch transaction.

Treat IDs and destination filenames as stable after release. Renaming destinations or dropping old IDs requires a separate migration policy; retain the old entry while users still need to uninstall it. The current extension point is additional Claude Code Markdown rules. Supporting another tool or multi-file packages requires an explicit destination/transaction design, not arbitrary commands in the manifest.
