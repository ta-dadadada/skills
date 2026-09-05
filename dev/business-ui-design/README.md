# business-ui-design

Business information structure and record-workflow decisions for operational UI.
Use it for a CRM, admin console, operations queue, or similar application where
comparison, views, and repeated record operations drive the screen structure.

## Companion

Install `frontend-ui-design` alongside this skill. This skill supplies domain
decisions and acceptance cases; the companion executes common UI design,
implementation, accessibility, responsive behavior, and verification. They share
one decision record and one review result. The frontend skill works independently.

## Usage

- “Design an operations queue for comparing orders and inspecting each one.”
- “Implement the CRM company list using our existing components.”
- “Reshape this approval workflow so reviewers retain evidence while deciding.”

Design requests produce a specification/prototype; implementation requests
produce working UI. The skill assumes no particular framework or vendor style.

## Contents

- [SKILL.md](SKILL.md): domain workflow and companion handoff.
- [references/patterns.md](references/patterns.md): business page archetypes and action scope.
- [references/data-workspaces.md](references/data-workspaces.md): tables, views, selection, and editing.
- [references/sources.md](references/sources.md): research provenance.

## Validation

See [VALIDATION.md](VALIDATION.md) for the model, trial scope, findings, and limitations.

From the repository root:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/business-ui-design dev/frontend-ui-design
```
