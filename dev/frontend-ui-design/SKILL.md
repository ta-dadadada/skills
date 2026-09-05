---
name: frontend-ui-design
description: >-
  Task-first frontend UI design and implementation: reuse the design system,
  choose interaction surfaces, specify forms and states, implement the task,
  and verify responsive behavior, keyboard access, and recovery. Use when
  designing a frontend interface or implementing or reshaping UI interactions
  in any domain, or when a domain skill supplies UI decisions for execution.
  Not for brand exploration, isolated styling fixes, or backend-only work.
license: MIT
metadata:
  author: ta-dadadada
---

# Frontend UI Design

Make the primary task discoverable, operable, and recoverable. This skill owns
the common frontend process; domain-specific record models and workflow choices
arrive as inputs. Visual style follows the product and its content.

## When to use

- Designing a frontend interface with navigation, input, or interaction decisions.
- Implementing or reshaping those interactions in any product domain.
- Executing UI work after a domain skill has selected its information structure.

## When not to use

- Brand exploration or isolated styling fixes with an established interaction contract.
- Backend-only work or deciding business rules.

## Workflow

### Step 1 — Establish the task and reuse prior decisions

Read the request, relevant UI/code, data contracts, and local instructions.
Choose **design** for a specification/prototype request or **implementation**
for working UI. Record the user, primary task, entry point, successful outcome,
scope, constraints, and a representative scenario with recovery cases.

When a domain skill supplies a decision record, reuse it and fill only missing
frontend details. Preserve its justified choices and explicit requirements;
resolve conflicts with task evidence. Infer routine choices; ask only about
missing information that changes the task, authority, or deliverable.

**Done when:** a single decision record identifies the delivery mode, testable
task, constraints, and unresolved assumptions, including any supplied domain choices.

### Step 2 — Inspect and choose the interface foundation

Find the closest implemented UI, component library, tokens, routing, form
conventions, and available tests. Record reuse and necessary additions.
Read [visual-language.md](references/visual-language.md) when establishing or
changing visual treatment. Use existing values; when no system exists, define
a small coherent token set suited to the product and input devices.
For design-only work without source access, distinguish the supplied system
description from inspected components and list implementation checks still needed.

Use [interaction-surfaces.md](references/interaction-surfaces.md) for detail,
transient UI, action placement, and narrow-screen transitions. Make essential
actions discoverable through a visible, labeled GUI path. Add accelerators
only to demonstrated frequent operations within scope.
For a table or editable grid, read [table-controls.md](references/table-controls.md)
to implement its semantics and keyboard behavior.

**Done when:** consequential component, token, surface, and navigation choices
have a source and a task-based reason in the decision record.
Unavailable product evidence is explicitly marked, rather than assumed inspected.

### Step 3 — Specify behavior

For input, mutations, or asynchronous content, read
[states-and-input.md](references/states-and-input.md). Specify applicable states,
feedback, recovery, and preserved user context. Specify semantics, keyboard
operation, focus transitions, and narrow-screen behavior with the component choice.

**Implementation:** before writing UI code, apply
[review.md](references/review.md) to the proposed design and supplied domain
acceptance cases. Record the scenario, structural findings, resolutions, and
pending runtime checks in the existing task notes or a progress message.
**Design:** carry the behavior decisions into the specification/prototype in
Step 4; its review happens against that artifact in Step 5.
Optional capabilities need evidence and scope.

**Done when:** the primary scenario has specified actions, states, recovery,
keyboard/focus behavior, and responsive transitions. In implementation mode,
the recorded pre-build review resolves structural defects before coding starts.

### Step 4 — Produce the requested interface

**Design:** deliver annotated structure or a prototype, interaction/state contracts,
key decision reasons, and concrete acceptance scenarios. Mark assumptions and
simulated behavior so an implementer can distinguish them.

**Implementation:** build a complete vertical slice with existing components
and data contracts. Connect controls to advertised actions and preserve context
and edits during transitions. Exercise realistic content, long values, and
applicable permission/error cases. Identify fixture-only behavior when an
integration is unavailable.

**Done when:** the design specifies every transition needed for the primary
scenario, or the implementation supports those transitions; missing integration
is explicitly identified as incomplete scope.

### Step 5 — Verify and deliver

After Step 4, separately read or inspect the produced artifact, then run
[review.md](references/review.md) and fix observed defects.
For implementation, exercise the running UI with pointer and keyboard at wide
and narrow widths, check zoom, and run relevant repository checks. For design,
walk the annotated scenario and identify runtime checks left to implementation.
Include the task's domain acceptance cases in the same pass.
Report the actual observations, check results, and limitations in the final
response after inspection. The artifact specifies behavior; verification claims
describe work actually performed on it. Keep the task record proportional.

**Done when:** applicable checks have evidence or explicit unverified status,
observed defects are fixed or reported, and the primary task is verified at the
delivery mode's level. Static inspection remains static evidence.

## Red flags

| Symptom | Correction |
|---|---|
| A dialog becomes a separate application | Reassess task independence and navigation |
| Required actions exist only in shortcuts or hover UI | Provide a discoverable GUI and keyboard/touch paths |
| A placeholder substitutes for a field label | Keep labels visible through entry and correction |
| A failed request discards user input | Preserve work and provide scoped recovery |
| A screenshot is treated as interaction verification | Exercise the task, transitions, and keyboard path |
| A domain handoff causes a second discovery exercise | Reuse the existing record and resolve only missing frontend details |

## Related

- [sources.md](references/sources.md) — provenance; consult for origins and limits.
- `frontend-design`, if available — visual direction; this skill covers interaction execution.
- Domain skills may supply structure and acceptance cases; this workflow applies them without invoking the caller again.
