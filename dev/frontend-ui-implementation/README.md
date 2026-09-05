# frontend-ui-implementation

Implement a reviewed UI contract with native HTML, appropriate ARIA, working
keyboard/focus behavior, responsive code, and evidence from the running interface.

## Usage

Use for a settled design or a `frontend-ui-design` handoff. Install the design
companion when design is missing or a decision conflicts with implementation.
Coding consumes the contract; only affected conflicting decisions return to design.
This package owns implementation details and runtime review, not UI discovery.

## Contents

- [SKILL.md](SKILL.md): workflow.
- [semantics-and-forms.md](references/semantics-and-forms.md)
- [keyboard-and-focus.md](references/keyboard-and-focus.md)
- [tables-and-grids.md](references/tables-and-grids.md)
- [runtime-review.md](references/runtime-review.md)
- [sources.md](references/sources.md)

## Validation

See [VALIDATION.md](VALIDATION.md) for scope, observations, and limitations.

From the repository root:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/frontend-ui-implementation
```
