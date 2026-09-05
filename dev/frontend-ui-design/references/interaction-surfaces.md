# Interaction surfaces

Choose by task complexity and navigation needs. Existing accessible components
and established behavior take priority over inventing a new interaction model.

## Page structure

For configuration, group forms by user task and expose the save scope. For
complex creation, use a focused form page with necessary context. For search,
organize query, filters, and results and state the search scope. Reuse an
existing domain structure when supplied; choose new sections by the information
users need together, rather than by available components.

## Detail and transient surfaces

| Need | Default surface | Escalate when |
|---|---|---|
| A little supplementary information | Inline expansion | Content crowds the primary surface |
| Quick inspection while keeping context | Detail pane | Work needs extensive space or independent navigation |
| Brief configuration | Side pane | Inputs become a long or multistep task |
| Bounded confirmation or short contextual task | Dialog | Content needs navigation or extensive editing |
| Independent, long, or multistep work | Dedicated page | Preserve a return path to the originating context |
| Choose or invoke | Menu | Rich search/selection needs a select panel or dialog |

Deep-linkable work needs stable navigation; default to a page. An established
routable pane is valid when direct entry and browser Back behave coherently.
For dialogs, define initial focus, focus containment, dismissal, and return
focus. For nonmodal panes, keep background context operable and provide an
explicit close/back path. Preserve unsaved work across transitions.

## Actions and escape paths

Place actions near their affected object or content region. Keep primary and
frequent actions visible; use labeled, discoverable menus for secondary actions.
Make the effect and scope clear in the label where ambiguity is possible.
Confirm consequential irreversible actions with target and consequence; offer
undo when safely reversible. Provide cancel/back paths for temporary work.

Shortcuts and context menus are alternate paths to the same GUI actions.
Preserve text-entry behavior and browser/assistive shortcuts. Give drag operations
an accessible alternative. Hover affordances also need focus and touch access.

## Responsive behavior

Preserve the task by changing presentation: simultaneous panes can become
sequential views, navigation can become a menu/index, and auxiliary content can
stack or move into a sheet. Preserve user state and a reliable return path.
Define meaningful reading/focus order and usable pointer/touch targets in each
structure. Verify access to primary content at narrow widths and zoom; merely
scaling the desktop layout is insufficient evidence.
