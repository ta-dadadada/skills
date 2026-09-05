# business-ui-design

Design operational jobs, record comparison, views, detail context, and action scope
for a CRM, admin console, operations queue, or similar business interface.

## Usage

Install `frontend-ui-design` for common UI design. Also install
`frontend-ui-implementation` for working UI. The chain is business structure →
frontend design contract → implementation and runtime verification. One decision
record and its acceptance cases flow through the chain. Common frontend rules
remain in their respective companion packages.

## Contents

- [SKILL.md](SKILL.md): workflow.
- [patterns.md](references/patterns.md)
- [data-workspaces.md](references/data-workspaces.md)
- [sources.md](references/sources.md)

## Validation

See [VALIDATION.md](VALIDATION.md) for scope, observations, and limitations.

From the repository root:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/business-ui-design
```
