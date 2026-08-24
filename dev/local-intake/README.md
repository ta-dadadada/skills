# local-intake

> Form-first local intake that turns an ambiguous request into an agreed brief
> through two or three browser questionnaires while keeping the full working
> state in one temporary Markdown file.

## Install

This is an [Agent Skills](https://agentskills.io) skill. Install it with the
`skills` CLI:

```bash
npx skills add ta-dadadada/skills --skill local-intake
```

Or with `apm`:

```bash
apm install ta-dadadada/skills/dev/local-intake
```

## Requirements

- Python 3.10 or newer
- A browser on the same computer as the agent
- Git is optional and is used only to hide the temporary intake document from
  `git status`

The form server binds to `127.0.0.1`, loads no remote assets, and sends no data
to an external service. Its preparation command registers the future working
document in Git's local exclude before that document is created.

## Files

- [SKILL.md](./SKILL.md) — the intake workflow
- [references/protocol.md](./references/protocol.md) — the working-document and
  form contracts
- [scripts/serve_form.py](./scripts/serve_form.py) — the one-shot local form
  server
- `scripts/local_intake/` — typed protocol, document, submission, Markdown,
  rendering, HTTP, and CLI modules used by the entry point
