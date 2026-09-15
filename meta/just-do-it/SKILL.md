---
name: just-do-it
description: >-
  Complete the requested task directly, minimizing lead time without optional
  skill discovery or workflow overhead. Use only when the user explicitly
  invokes just-do-it or asks to work without additional skills. The main agent
  executes by default; delegate only when permitted independent parallel work
  is expected to shorten completion time. Preserve required verification,
  authority boundaries, and explicit limits such as design-only requests.
  Do not activate merely because a task looks simple or urgent.
license: MIT
metadata:
  author: ta-dadadada
---

# Just Do It

The main agent completes the user's requested deliverable directly. Optimize
elapsed time from request to verified result, including coordination and
integration costs. This is a procedure for the current task, not a permanent
change to skill selection.

## When to use

- The user explicitly invokes `just-do-it` or asks to work without additional
  skills.

## When not to use

- There is no explicit request, even if the task seems simple or urgent.
- The user has ended this mode or moved to an unrelated task.

## Workflow

### 1. Keep the requested scope

Use the conversation and relevant task evidence to identify the deliverable
and constraints; do not create a separate brief. Resolve routine choices
yourself. Ask only when available evidence and existing authorization cannot
resolve a decision affecting scope, correctness, or authority. Continue
independent authorized work while waiting.

Do not discover, recommend, load, or chain optional skills, or add procedures
from optional skills already loaded. Follow higher-priority instructions,
mandatory repository requirements, and the user's explicit instructions to
use other skills; perform only their applicable requirements. This skill
does not erase loaded context or override those obligations.

### 2. Do the work directly

Read the necessary task material and use appropriate tools. Avoid unrequested
plans, session records, review stages, and other artifacts unless required
to complete the deliverable. Do not stop at an offer or a plan when execution
was requested. A design-only or no-edit request remains within that limit.

Execute in the main agent by default. Delegate only when delegation is
permitted, the subtask is independent, the main agent can advance other
useful work concurrently, and expected savings exceed startup, context
transfer, waiting, integration, and verification costs. If the benefit is
unclear, execute directly. Do not delegate the whole task merely to wait or
to escape loaded skill context. Give any delegate the bounded task, necessary
context, constraints, and this mode's rules; the main agent owns integration
and completion.

### 3. Verify and deliver

Run required checks and verification proportionate to the change. Reuse
valid evidence; repeat checks only after relevant changes, failures, or
unresolved concerns. Fix failures within scope and continue until complete
or blocked by an unresolved external dependency or required user decision.

**Done when:** the requested deliverable satisfies its applicable constraints,
required checks pass, and the result is delivered. Report the outcome and
material verification briefly. If blocked, state completed work and the
specific remaining dependency without claiming completion. Fewer steps or
an earlier reply alone do not establish a shorter lead time.

## Red flags

- Selecting another optional skill before starting the task.
- Creating workflow artifacts instead of the requested deliverable.
- Delegating while the main agent has no useful concurrent work.
- Skipping verification, exceeding scope, or stopping after a plan for speed.

## Related

No skill dependencies or follow-up skill handoffs.
