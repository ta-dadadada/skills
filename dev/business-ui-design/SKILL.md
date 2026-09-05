---
name: business-ui-design
description: >-
  Task-first business UI structure: identify operational jobs and records,
  choose page archetypes, tables, views, detail context, and scoped actions,
  then compose with frontend-ui-design for design or implementation and
  verification. Use when designing or reshaping a business application such
  as an admin console, CRM, operations queue, or data-heavy internal tool.
  Not for general frontend interaction work or isolated styling fixes.
license: MIT
metadata:
  author: ta-dadadada
---

# Business UI Design

Preserve the information operators need while reducing search, comparison, and
operation costs. This domain skill owns business information structure and
record-workflow decisions. The companion `frontend-ui-design` skill owns common
frontend design, implementation, and verification; install both for this workflow.

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
Keep optional data-workspace capabilities conditional on frequency and scope.

For data-heavy operational surfaces, favor a restrained visual treatment that
preserves comparison and scanning. The product design system supplies concrete
values; the companion skill handles visual and accessibility execution.

**Done when:** the primary scenario maps to a justified archetype, representation,
view strategy, detail context, and action scopes, with acceptance cases for
applicable filtering, sorting, selection, editing, and permission behavior.

### Step 3 — Produce the artifact through the frontend skill

Locate and read the installed `frontend-ui-design` skill. Pass the existing
record, domain decisions, acceptance cases, and delivery mode into its Steps 1–4.
Reuse its single decision record. It supplies component/token inspection,
interaction surfaces, forms/states, responsive and accessible behavior,
artifact production, and a pre-code review when implementation is requested.
The companion's Step 5 is executed in the next step below, together with domain
acceptance. At this point the artifact exists and final review is still pending.

If the companion is unavailable, complete the domain decisions and identify the
missing dependency and unfinished execution scope. Do not claim an implemented
or verified UI from business structure alone.

**Done when:** the requested artifact exists, the implementation-only pre-code
review was performed if applicable, and final review is pending; or the missing dependency is explicitly reported
with domain decisions preserved and execution marked incomplete.

### Step 4 — Check business acceptance and deliver

Now read or inspect the artifact produced in Step 3 and execute the companion's
Step 5. Add these domain checks to that review, using the same evidence:

- The entry surface supports the operational job; metrics serve actual decisions.
- Representation supports simultaneous comparison or stage/visual work as intended.
- Views preserve record identity and consistent action semantics.
- Returning from detail retains the expected collection context.
- Collection, record, field, and selection operations affect their advertised scope.
- Server/client paging, filter, and sort behavior matches the advertised dataset.
- Applicable selection and mutation failure cases have honest recovery behavior.
- Optional saved views, bulk actions, grids, and accelerators stay within scope.

After inspection, report actual findings and evidence in the final response.
Fix observed defects and recheck affected cases. Deliver the interface artifact,
key business decisions, verification evidence, and limitations together.

**Done when:** the artifact was inspected and final findings report that evidence, every
applicable domain check has evidence or an explicit
unverified status; the requested task is verified at the delivery mode's level;
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

- `frontend-ui-design` — required companion; install alongside this skill.
- [sources.md](references/sources.md) — provenance and reading trail; consult for origins and limits.
- `domain-modeling`, if available — unresolved business meaning before UI decisions.
