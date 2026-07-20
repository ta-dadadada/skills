# Multi-Tool Skill Distribution

Distributing one canonical skill to Codex, Claude Code, GitHub Copilot, and
Cursor. **The basics — frontmatter spec, directory layout, placement paths,
portability rules — are maintained in
[`meta/shiranui-hanten/references/SPEC.md`](../../meta/shiranui-hanten/references/SPEC.md);
read that first.** This file keeps what SPEC.md doesn't: per-tool extension
details, the support comparison, and a build-pipeline design for when copies
and overlays need automation.

All four tools natively support the Agent Skills standard (as of
2026-07-11). Two install targets cover everything: `.agents/skills/`
(Codex, Copilot, Cursor) and `.claude/skills/` (Claude Code).

## Tool comparison

| | Codex | Claude Code | GitHub Copilot | Cursor |
|---|---|---|---|---|
| Reads `.agents/skills/` | yes | no (uses `.claude/skills/`) | yes | yes |
| Tool-specific project path | — | `.claude/skills/` | `.github/skills/` | `.cursor/skills/` |
| Explicit invocation | yes | `/skill-name` | surface-dependent | yes |
| Symlinked skill dirs | officially supported | officially supported (v2.1.203+) | no explicit guarantee | environment-dependent |
| Proprietary metadata | `agents/openai.yaml` | frontmatter extensions | per-feature | per-feature |

Both Codex and Claude Code scan every directory level from CWD up to the
repo root, so monorepo subdirectories can carry their own scoped skills.

## Per-tool extensions (keep out of the common skill)

**Codex — `agents/openai.yaml`** inside the skill dir: display name, icons,
default prompt, `policy.allow_implicit_invocation`, tool dependencies.
Standard-external but inert for other tools, so it can coexist.

**Claude Code — frontmatter and body extensions:** `disable-model-invocation`,
Claude-form `allowed-tools`, subagent designation, `` !`command` `` dynamic
context injection (executed before the model sees the body), and
`${CLAUDE_SKILL_DIR}`. None of these work elsewhere — overlay them.

**Copilot** also reads `.claude/skills/` and `.agents/skills/`, but don't
assume it interprets Claude-specific frontmatter or dynamic expansion.
Skills complement, not replace, `copilot-instructions.md` (always-on rules)
— same split as Cursor rules vs skills: "use strict mode" is a rule;
"investigate → fix → test a dependency vulnerability" is a skill.

## Build pipeline (when automation becomes worth it)

Keep the canonical source outside any tool directory, overlay tool-specific
bits at build time:

```text
skills-repository/
├── skills/<skill-name>/          # canonical: SKILL.md, scripts/, references/, assets/
├── overlays/
│   ├── codex/<skill-name>/agents/openai.yaml
│   └── claude-code/<skill-name>/frontmatter.yaml
├── scripts/                      # validate / build / install
└── dist/                         # per-target output
```

Pipeline: `validate → normalize → apply target overlay → copy to target →
target-specific validation`. Target definitions collapse into two install
groups because three tools share one path:

```yaml
installGroups:
  common-agents:
    targets: [codex, github-copilot, cursor]
    output: ".agents/skills"
  claude:
    targets: [claude-code]
    output: ".claude/skills"
```

Symlinks suit local use; copies are more robust for distributed repos
(Windows, ZIP, external tooling) — then verify drift in CI with
`diff -ru skills/<name> .agents/skills/<name>`.

Validation items beyond the spec checks in SPEC.md / `validate_skill.py`:
referenced files exist, scripts have exec permission when needed, no
absolute paths, no product-specific variables in the common version,
MCP/command/network requirements declared in `compatibility`.

## Sources

Collected 2026-07-11.

- https://agentskills.io/specification
- https://developers.openai.com/codex/skills
- https://code.claude.com/docs/en/skills
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- https://docs.github.com/en/copilot/reference/custom-instructions-support
- https://cursor.com/docs/skills / https://cursor.com/docs/rules
