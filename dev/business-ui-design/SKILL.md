---
name: business-ui-design
description: >-
  Task-first business UI structure: identify operational jobs and records,
  choose page archetypes, tables, views, detail context, and scoped actions,
  then hand off to frontend-ui-design and, for requested code,
  frontend-ui-implementation. Use when designing or reshaping a business
  application such as an admin console, CRM, operations queue, or data-heavy
  internal tool.
  Not for general frontend interaction work or isolated styling fixes.
license: MIT
metadata:
  author: ta-dadadada
---

# Business UI Design

Preserve the information operators need while reducing search, comparison, and
operation costs. This domain skill owns business information structure and
record-workflow decisions. The companion `frontend-ui-design` skill owns common
frontend design contracts; `frontend-ui-implementation` owns code and runtime
verification. Install the design companion, and the implementation companion
when working UI is requested.

## When to use

- Designing a business screen or connected operational workflow.
- Implementing or reshaping business UI with decisions about records, comparison,
  information hierarchy, views, or repeated operations.

## When not to use

- General frontend interactions, forms, accessibility, responsive behavior, or
  state handling without business-structure decisions: use `frontend-ui-design`.
- Brand exploration or isolated styling fixes.
- Standalone domain modeling or backend architecture decisions.

## Workflow

### Step 1 — Establish the operational job

Read the request, relevant screens/code, data contracts, and local instructions.
Record the actor, primary job, entry point, successful outcome, and design versus
implementation delivery mode. Reuse prior task notes when available.

Add objects, comparable attributes, approximate volume, permissions, information
needed simultaneously, and frequent/occasional/destructive operations. Capture
one representative scenario plus relevant failure cases. Distinguish evidence,
routine assumptions, and unknown business rules. Infer routine UI choices; ask
only about missing facts that change the task, authority, or deliverable.

**Done when:** one decision record identifies a testable primary job, data and
action needs, scope, delivery mode, and consequential unknowns. Unknown business
rules remain explicit inputs rather than invented UI behavior.

### Step 2 — Choose business structure

Read [patterns.md](references/patterns.md) for page archetypes and action scope.
For collections, comparison, or repeated editing, read
[data-workspaces.md](references/data-workspaces.md).

Record consequential choices as **task evidence → pattern → tradeoff**. Choose
representation, collection/detail relationship, views versus separate workflows,
and action locations from the job. Reuse existing product patterns when known.
Use Step 1's frequency evidence: frequent repeated operations are candidates for
batch actions, inline editing, saved views, or accelerators. Select the candidate
that reduces the observed repetition, and adopt it only when its benefit and task
scope justify it; frequency is a reason to evaluate, not to add every capability.

For data-heavy operational surfaces, favor a restrained visual treatment that
preserves comparison and scanning. The product design system supplies concrete
values; the design companion specifies visual and accessibility requirements.

**Done when:** the primary scenario maps to a justified archetype, representation,
view strategy, detail context, and action scopes, with any efficiency choice tied
to observed repetition and scope, and acceptance cases for
applicable filtering, sorting, selection, editing, and permission behavior.

### Step 3 — Hand off for frontend design and requested implementation

Locate and read `frontend-ui-design`. Pass the existing record, domain decisions,
business acceptance cases below, and delivery intent through its full workflow.
It fills frontend details, reviews the design contract, and delivers design-only
work or continues to `frontend-ui-implementation` when code is requested.
Reuse the same record and acceptance cases across the chain. Let the design
skill own the handoff format and the implementation skill own runtime checks.

If a required companion is unavailable, preserve completed decisions and identify
the dependency and unfinished scope. Business structure alone does not establish
an implemented or verified UI.

**Done when:** the companion returns the reviewed design or requested working UI
with evidence and limitations, or the missing dependency and incomplete scope
are explicit.

### Step 4 — Reconcile business acceptance and deliver

Assess the returned artifact and evidence against these domain cases. Include
them in the design/runtime reviews through Step 3, then reuse those observations
here rather than repeating the frontend checks:

- The entry surface supports the operational job; metrics serve actual decisions.
- Representation supports simultaneous comparison or stage/visual work as intended.
- Views preserve record identity and consistent action semantics.
- Returning from detail retains the expected collection context.
- Collection, record, field, and selection operations affect their advertised scope.
- Server/client paging, filter, and sort behavior matches the advertised dataset.
- Applicable selection and mutation failure cases have honest recovery behavior.
- Optional efficiency features address observed repetition and stay within scope.

After inspection, report actual findings and evidence in the final response.
Fix observed defects and recheck affected cases. Deliver the interface artifact,
key business decisions, verification evidence, and limitations together.

**Done when:** the artifact was inspected and final findings report that evidence;
every applicable domain check has evidence or an explicit unverified status; the requested task is verified at the delivery mode's level;
remaining defects, dependencies, and unknown business rules are visible.

## Red flags

| Symptom | Correction |
|---|---|
| A dashboard precedes understanding the job | Choose the entry surface from the operational scenario |
| Comparable records become decorative cards | Evaluate attribute comparison and repeated editing first |
| Every filter becomes a new workflow | Evaluate views over the same collection |
| Dense UI becomes tiny text or hidden essential actions | Preserve legibility while removing irrelevant UI |
| Every optional productivity feature enters scope | Require demonstrated need and task scope |
| Common frontend rules are copied here | Keep their authoritative home in the companion skill |

## Related

- `frontend-ui-design` — required design companion.
- `frontend-ui-implementation` — also install when working UI is requested.
- [sources.md](references/sources.md) — provenance and reading trail; consult for origins and limits.
- `domain-modeling`, if available — unresolved business meaning before UI decisions.
