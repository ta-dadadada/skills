---
name: frontend-ui-design
description: >-
  Task-first frontend UI design: define structure, surfaces, forms, states,
  responsive transitions, keyboard/focus and accessibility requirements,
  then review a design contract. Use when designing or reshaping UI behavior
  in any domain, including the design phase of an implementation request
  or a domain-skill handoff. For requested code, hand the reviewed contract
  to frontend-ui-implementation. Not for coding an already settled design,
  brand exploration, isolated styling fixes, or backend-only work.
license: MIT
metadata:
  author: ta-dadadada
---

# Frontend UI Design

Make the primary task discoverable, operable, and recoverable. This skill owns
the common UI design contract; domain-specific record models and workflow choices
arrive as inputs. Visual style follows the product and its content.

## When to use

- Designing a frontend interface with navigation, input, or interaction decisions.
- Resolving UI decisions before implementing or reshaping interactions.
- Designing UI after a domain skill has selected its information structure.

## When not to use

- Brand exploration or isolated styling fixes with an established interaction contract.
- Coding a settled design: use `frontend-ui-implementation`.
- Backend-only work or deciding business rules.

## Workflow

### Step 1 — Establish the task and reuse prior decisions

Read the request, relevant UI/code, data contracts, and local instructions.
Record whether delivery ends at a design or continues to working UI. This
skill produces the design in either case; coding belongs to the implementation
companion. Scale the record to the change: for a localized adjustment in a
known interface, one to three sentences naming the changed behavior, expected
outcome, and relevant constraints are enough. Use that behavior as the review
scenario; reuse established context rather than filling a new intake template.
For a new or substantially changed workflow, add the user, entry point, scope,
representative scenario, and recovery cases needed to resolve its design decisions.
Carry this scope through later steps: inspect affected paths, document changed
decisions, and reuse unchanged contracts.

When a domain skill supplies a decision record, reuse it and fill only missing
frontend details. Preserve its justified choices and explicit requirements;
resolve conflicts with task evidence. Infer routine choices; ask only about
missing information that changes the task, authority, or deliverable.

**Done when:** the request or brief record establishes the delivery mode and a
testable outcome, with relevant constraints and consequential unknowns explicit.
Existing context supplies unchanged details, including any domain handoff.

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
actions discoverable through the standard GUI, without requiring knowledge of
shortcuts. A clearly signposted menu or contextual affordance with understandable
action labels can provide that path; every action need not be permanently visible.
Keep the path usable with keyboard and touch as applicable. Add accelerators
only to demonstrated frequent operations within scope.
For a table or editable grid, read [table-controls.md](references/table-controls.md)
to specify comparison, sorting, and cell-interaction requirements.

**Done when:** consequential component, token, surface, and navigation choices
have a source and a task-based reason in the decision record.
Unavailable product evidence is explicitly marked, rather than assumed inspected.

### Step 3 — Specify behavior

For input, mutations, or asynchronous content, read
[states-and-input.md](references/states-and-input.md). Specify applicable states,
feedback, recovery, and preserved user context. Specify semantics, keyboard
operation, focus transitions, and narrow-screen behavior with the component choice.

Read [accessibility.md](references/accessibility.md) for the requirements that
must accompany the design. Keep HTML, ARIA, CSS, and event-handler choices in
the implementation companion. Optional capabilities need evidence and scope.

**Done when:** the scoped scenario has specified actions, states, recovery,
keyboard/focus behavior, accessibility requirements, and responsive transitions.

### Step 4 — Produce and review the design contract

Produce an annotated specification or design prototype using
[handoff.md](references/handoff.md). Reuse existing decisions by reference;
a small change can be a compact addition to an existing contract. Mark assumptions
and simulated behavior. A prototype illustrates the contract; production code
and runtime acceptance belong to the implementation skill.

After producing the artifact, separately read or inspect it and apply
[review.md](references/review.md), including supplied domain acceptance cases.
For working-UI requests, finish this inspection before writing UI code. Resolve contradictions and report actual design
observations. A separate review document is optional; the final response or existing task notes can hold evidence.

**Done when:** the artifact specifies the primary scenario's transitions and
handoff requirements, and a subsequent design review has resolved or identified
defects and explicitly recorded unresolved assumptions and runtime checks.

### Step 5 — Deliver or hand off

For a design-only request, deliver the reviewed artifact, key reasons, findings,
and limitations. No implementation companion is needed.
For requested working UI, locate and read `frontend-ui-implementation`, pass the
reviewed contract and existing evidence, and continue through its workflow.
Its runtime review consumes the same acceptance cases; this skill does not
repeat those checks. If the companion is unavailable, preserve the contract and
report the missing dependency and implementation scope still unfinished.

**Done when:** the reviewed design is delivered for design-only work, or the
implementation workflow has returned working UI and verification evidence with
explicit limitations; any missing dependency or unfinished scope is reported.

## Red flags

| Symptom | Correction |
|---|---|
| A dialog becomes a separate application | Reassess task independence and navigation |
| Required actions exist only in shortcuts or hover UI | Provide a discoverable GUI and keyboard/touch paths |
| A placeholder substitutes for a field label | Keep labels visible through entry and correction |
| A failed request discards user input | Preserve work and provide scoped recovery |
| A design review is treated as runtime evidence | Label design observations and hand runtime cases to implementation |
| A domain handoff causes a second discovery exercise | Reuse the existing record and resolve only missing frontend details |

## Related

- [sources.md](references/sources.md) — provenance; consult for origins and limits.
- `frontend-design`, if available — visual direction; this skill covers interaction design.
- `frontend-ui-implementation` — code and runtime verification; required only for working UI.
- Domain skills may supply structure and acceptance cases; this workflow applies them without invoking the caller again.
