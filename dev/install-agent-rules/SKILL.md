---
name: install-agent-rules
description: >-
  Install, update, preview, or uninstall bundled Claude Code rules when
  explicitly requested. Select a rule from the manifest and run the script
  for diffing, conflict detection, planning, and applying the unchanged plan.
  All destination and installation-record operations belong to the script;
  never edit them directly. Not for routine coding, design review, arbitrary
  file installation, or semantic merging of project instructions. Local edits
  and unmanaged files are preserved on conflicting updates or removals.
license: MIT
compatibility: Python 3.11+ on macOS or Linux; local filesystem access. Current destination adapter is Claude Code rules only.
metadata:
  author: ta-dadadada
---

# Install Agent Rules

Manage the rules listed in [the manifest](assets/manifest.json) through [the installer](scripts/install_rules.py). The agent selects the requested rule, operation, and scope, invokes the script, and explains the result. The script owns all destination inspection, diffing, conflict detection, placement, removal, and installation-record updates.

## When to use

- Explicitly asked to install, update, or uninstall a bundled rule in a project or user scope.
- Asked to preview those operations or inspect an installation conflict.

## When not to use

- Routine coding, software design, or design review without a rules-management request.
- Installing arbitrary files, another tool's rules, or altering the rule text to fit a project.

## Workflow

1. **Select rule, operation, and scope.** Run `list`. When the user has not identified a rule (including bare skill invocation), present every returned ID with a short description in the user’s language and ask which to install or update. Wait for the selection before planning. When a rule was specified, resolve it directly. Use `install` for introduction or update, and `uninstall` only when removal is requested. Use the requested project root, or the current project when "this project" identifies it. Use `--user` only for explicitly requested user-wide scope. Ask only when the selection cannot be inferred. Locate the installer relative to this skill's canonical directory; it finds its own assets without requiring the distribution repository.
2. **Plan.** Run `plan` with the selected rule, operation, and an absolute project path or `--user`. Read its JSON action, reason, destination, diff, and plan ID. Planning writes nothing. A preview-only request ends with this result.
3. **Apply eligible plans.** For an authorized operation, run `apply` with the identical selection and exact returned plan ID when the action is `install`, `update`, `recover`, `uninstall`, or `cleanup`. The original operation request authorizes these changes; no additional confirmation is required. `unchanged` needs no apply. For a conflict or error, explain the script's reason and stop dependent work. For `stale_plan`, replan and reassess; never reuse the old ID or retry indefinitely.
4. **Report.** State the actual destination and result, including unresolved conflicts/errors. Claude Code loads installed rules automatically. For Codex, tell the user to reference the installed rule from the applicable project or user AGENTS.md, or remove that reference after uninstalling. Use the returned destination in the example. For other agents, mention their supported instruction entry point when known. Leave these edits to the user. Do not claim a running Claude session has loaded or unloaded the rule. Do not claim semantic conflicts with other instructions were checked.

From this skill directory:

```bash
python3 scripts/install_rules.py list
python3 scripts/install_rules.py plan --rule software-design --project /absolute/project
python3 scripts/install_rules.py apply --rule software-design --project /absolute/project --plan-id RETURNED_ID
```

For removal, add `--operation uninstall` to both `plan` and `apply`. For explicitly requested user scope, replace `--project /absolute/project` with `--user` in both commands. Read [the installer contract](references/installer-contract.md) when handling conflicts, failures, or questions about management behavior.

**Done when:** the script reports applied, removed, or unchanged; a requested preview has been delivered; or a blocking conflict/error has been reported. No destination patch by the agent is part of completion.

## Red flags

- Editing, copying, deleting, merging, or moving destination rules or installer state directly, including shell workarounds.
- Modifying the bundled asset, manifest, or installer to bypass a conflict in this installation task.
- Treating a plan ID as authorization for another rule, operation, target, or changed bundle.
- Applying uninstall automatically because a local rule differs.

## Related

- [Software design rules](assets/software-design.md) — criteria for software structure.
- [Project documentation rules](assets/project-documentation.md) — guidance on placing and maintaining project information.
- `purpose-driven-software-design` — design/review workflow using the same distributed criteria; not required for installation.
