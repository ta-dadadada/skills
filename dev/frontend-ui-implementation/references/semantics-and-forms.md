# Semantics, names, and forms

## Native elements first

Use `<button>` for actions, `<a href>` for navigation, native input/select/textarea
for form controls, and `<table>` for tabular data. Set button type deliberately
inside forms. Style these elements to match the design; appearance alone is no
reason to replace them with `div onClick`. ARIA supplements missing semantics.
Check existing components' rendered DOM and behavior before augmenting them.

## Accessible names

Use this **authoring preference**, applying the technique appropriate to the element:

1. Visible text content for elements that take their name from content.
2. An associated visible `<label>` for a labelable form control.
3. `aria-labelledby` referencing suitable text when native naming is insufficient.
4. `aria-label` only when a suitable visible naming source is unavailable.

This is not the browser's computed-name precedence: ARIA naming can override
native visible names. Prefer a single maintained naming source; keep visible
wording in the accessible name. Verify the computed name, especially for shared
components and repeated controls requiring record context.

The icon-only action needs an explicit name; the text action uses its content:

```tsx
<button type="button" aria-label="Delete customer">
  <TrashIcon aria-hidden="true" />
</button>

<button type="button">Delete customer</button>
```

Decorative icons stay out of the accessibility tree. Tooltips and placeholders
supplement persistent labels; they are not substitutes for them.

## Form relationships and recovery

Associate a visible `<label for="email">` with a stable, unique input `id`;
React uses `htmlFor`. Use fieldset/legend for related control groups. Associate
help and current error text with `aria-describedby` IDs. Set `aria-invalid="true"`
when invalidity is established, remove/reset it on correction, and keep the error
text actionable. Preserve help references when adding an error reference.

Implement the designed validation timing and value/commit events. On failed
submission, focus the contracted error summary or first invalid field and expose
the errors for announcement; avoid duplicate disruptive announcements. Retain
entered values. For asynchronous saves, separate draft from confirmed state,
prevent duplicate submissions, expose pending/outcome feedback, and retain draft
and a usable retry path on failure. Reconcile optimistic updates as contracted.

## State exposure

Apply only attributes supported by the actual element/role and keep them current:

| State | Implementation |
|---|---|
| Disclosure | `aria-expanded` on its controller; `aria-controls` points to the controlled element when applicable |
| Current navigation | `aria-current`, such as `page`, for the actual current destination |
| Widget selection | `aria-selected` on supporting roles such as tab/option; native checkbox `checked` for checkbox selection |
| Sort | `aria-sort` on the currently sorted header, matching the actual direction |
| Asynchronous status | A mounted `role="status"` or appropriate live region updated with concise progress/outcome text |
| Measurable progress | Native progress or a correctly named progressbar with actual values; distinguish indeterminate work |

Use urgent announcements only for urgent information; preserve focus for ordinary
status updates. Where relevant, use `aria-busy` on the updating region and clear
it on completion/failure. `aria-disabled` communicates inactivity but does not
block events: enforce the contracted behavior in code or use native disabled
where appropriate. Keep focus and explanatory feedback usable.
