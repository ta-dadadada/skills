# frontend-ui-design

Design the UI contract: structure, surfaces, forms/states, responsive behavior,
keyboard/focus and accessibility requirements, visual language, and design review.

## Usage

Design-only work needs no implementation companion. For working UI, install
`frontend-ui-implementation`; the reviewed contract flows to code and runtime
checks there. A supplied domain record is reused. For visual direction, use the
product design process or `frontend-design` when available. No enterprise theme
is imposed.

## Contents

- [SKILL.md](SKILL.md): workflow.
- [interaction-surfaces.md](references/interaction-surfaces.md)
- [states-and-input.md](references/states-and-input.md)
- [accessibility.md](references/accessibility.md)
- [table-controls.md](references/table-controls.md)
- [visual-language.md](references/visual-language.md)
- [handoff.md](references/handoff.md)
- [review.md](references/review.md)
- [sources.md](references/sources.md)

## Validation

See [VALIDATION.md](VALIDATION.md) for scope, observations, and limitations.

From the repository root:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/frontend-ui-design
```
