# frontend-ui-design

Common UI design and implementation for any frontend domain: discoverable
actions, surfaces, forms, state feedback, recovery, responsive behavior,
accessible interaction, design-system reuse, and evidence-based review.

## Usage

- “Design the reading-list and book-detail interactions for a personal library.”
- “Implement account settings with validation and failed-save recovery.”
- “Reshape this learning interface for keyboard and narrow-screen use.”

Design requests produce annotated specifications/prototypes. Implementation
requests produce working UI and runtime evidence where tools are available.
`business-ui-design` can supply domain decisions, but is not a dependency.
For visual direction, combine with the project's design process or
`frontend-design` when available. This skill does not impose an enterprise theme.

## Contents

- [SKILL.md](SKILL.md): shared execution workflow.
- [references/interaction-surfaces.md](references/interaction-surfaces.md): surfaces, actions, responsive transitions.
- [references/states-and-input.md](references/states-and-input.md): forms and state contracts.
- [references/table-controls.md](references/table-controls.md): table/grid semantics and keyboard behavior.
- [references/visual-language.md](references/visual-language.md): product-led visual consistency.
- [references/review.md](references/review.md): pre-construction and final review.
- [references/sources.md](references/sources.md): provenance and limits.

## Validation

See [VALIDATION.md](VALIDATION.md) for the model, trial scope, findings, and limitations.

From the repository root:

```bash
python3 meta/shiranui-hanten/scripts/validate_skill.py dev/frontend-ui-design
```
