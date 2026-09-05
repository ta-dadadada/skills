# Keyboard and focus implementation

Use the existing accessible component implementation when it fulfills the
contract. Check the rendered control and real keyboard path, not just its API.

## Page and controls

Keep DOM order aligned with reading and task order. Use native tab stops;
`tabindex="0"` admits a necessary custom target, `-1` permits programmatic focus,
and positive values usually break logical ordering. Preserve a visible focus
indicator, including in overflow regions and high-contrast product themes.
Native buttons supply Enter/Space activation; links supply navigation behavior.

For compound widgets, implement the applicable pattern: Tab enters/exits the
widget; arrows navigate within menus, tabs, or grids when their contract requires
it. Use roving tabindex or supported active-descendant management consistently.
Keep focus and selection distinct and let text controls retain editing keys.
A visual action popover can use ordinary buttons and Tab traversal when that is
the intended contract; an ARIA menu requires its menu keyboard behavior.

Provide the contracted keyboard alternative to drag, such as Move up/down or a
Move-to control. Preserve browser and assistive-technology shortcuts.

## Modal dialog

Prefer the established modal component or native `<dialog>` opened with
`showModal()` when appropriate. Give the dialog an accessible name, set initial
focus according to content/task, contain Tab and Shift+Tab, and make the
background inert while modal. Implement Escape/dismissal according to the
unsaved-work contract and include an operable close/cancel path.

After close, restore focus to the trigger or the designed logical successor if
the trigger was removed. Check focus after success, cancellation, error, and
responsive remounts. A custom modal needs actual focus containment and background
inertness; `role="dialog"` and `aria-modal="true"` alone do not provide them.
Nonmodal panes retain background access and use their separate focus contract.

Consult the relevant primary pattern when implementing a custom compound widget:
[APG keyboard practices](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/),
[modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), and
[menu button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/).
