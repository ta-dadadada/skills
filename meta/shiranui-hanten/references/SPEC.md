# Spec & Distribution

The Agent Skills open standard ([agentskills.io/specification](https://agentskills.io/specification)) is supported natively by Claude Code, Codex, GitHub Copilot, and Cursor. Write to the standard; treat tool-specific features as per-tool overlays.

## Frontmatter

| Field | Required | Constraint |
|---|---|---|
| `name` | yes | 1–64 chars, `^[a-z0-9]+(?:-[a-z0-9]+)*$`, must equal the skill directory name |
| `description` | yes | 1–1024 chars; states what the skill does *and* when to use it |
| `license` | no | license name or file reference |
| `compatibility` | no | ≤500 chars; required commands, network access, OS assumptions |
| `metadata` | no | arbitrary string key–value pairs |
| `allowed-tools` | no | experimental; support varies by client |

## Directory layout

Only `SKILL.md` is required. Conventional auxiliary directories:

```
my-skill/
├── SKILL.md
├── scripts/       # executable scripts
├── references/    # detailed material loaded on demand
└── assets/        # templates, images, generated material
```

Long material goes in `references/`, with `SKILL.md` stating when to read it — the standard assumes progressive disclosure: agents read `name` + `description` first, and the body and auxiliary files only when triggered.

## Portability

A skill written to the standard runs on all four tools. Keep in the common skill:

- standard frontmatter, plain Markdown, relative links
- `scripts/`, `references/`, `assets/`
- shell/Python steps, input/output examples, error-handling policy

Keep out of the common skill (ship as per-tool overlays when needed):

- Claude Code syntax: `` !`command` `` dynamic injection, `${CLAUDE_SKILL_DIR}`, `disable-model-invocation`, Claude-form `allowed-tools`, subagent designation
- Codex: `agents/openai.yaml` contents
- tool-specific MCP tool names or permission settings — or declare them in `compatibility`
- always-on instructions — those belong in Cursor rules or `copilot-instructions.md`, and a skill holds task procedures instead

Use relative paths (`python3 scripts/validate.py`) rather than absolute paths or tool variables.

## Placement

Keep the canonical source in this repository's category directories (e.g. `meta/<skill-name>/`). A skill only functions once placed where a tool actually reads it:

| Tool | Project path | User path |
|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.agents/skills/` (also `.github/skills/`, `.claude/skills/`) | `~/.copilot/skills/` or `~/.agents/skills/` |
| Cursor | `.agents/skills/` (also `.cursor/skills/`) | `~/.agents/skills/` or `~/.cursor/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

Two targets cover all four tools: `.agents/skills/` (Codex, Copilot, Cursor) and `.claude/skills/` (Claude Code). Install by symlink for local use, by copy for distributed repositories; when copying, verify drift with `diff -ru <canonical> <installed>`.

## Security

A skill ships scripts as well as Markdown — review it like a dependency:

- Resolve credentials at runtime; skill contents can leave the environment (Agent Skills are ZDR-exempt), so no secrets, tokens, or internal endpoints anywhere in the skill.
- No instructions that read secrets or pipe remote code into a shell (`curl | sh`).
- External destinations fixed and explicit; destructive operations gated on confirmation.
- Scope `allowed-tools` tightly; a code-executing skill assumes sandbox isolation and monitoring.
