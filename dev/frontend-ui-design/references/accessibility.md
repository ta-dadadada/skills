# Accessibility requirements

Design what users must be able to perceive and operate. The implementation
companion owns element selection, naming attributes, and event/focus code.

- Every control needs an understandable accessible name, including icon-only
  actions. For persistent visible field labels, help/error relationships, and
  validation announcements, apply [form contracts](states-and-input.md#forms).
- Make the primary task and its recovery possible with keyboard alone. Define
  reading/Tab order, visible focus, and any component-specific key behavior.
- Apply [surface contracts](interaction-surfaces.md#detail-and-transient-surfaces)
  for modal containment, initial/return focus, and dismissal. Include Escape and
  a logical focus destination when the original trigger is gone.
- For menus, tabs, and cell navigation, define the expected keyboard pattern and
  exit path. Apply the [non-drag alternatives](interaction-surfaces.md#actions-and-escape-paths)
  and [table requirements](table-controls.md) when those interactions are present.
- Use the [state contract](states-and-input.md#state-contract) for non-color cues
  and identify which asynchronous updates need announcement without moving focus.
- Preserve meaningful reading/focus order and task access at narrow widths and
  200% zoom. Use [visual requirements](visual-language.md) for legibility,
  usable targets, and the product's applicable contrast targets.

Specify observable outcomes, including failure recovery, in acceptance cases.
A design review can confirm these requirements are coherent and present; their
runtime implementation and assistive-technology behavior remain pending.
