---
name: orchestrate
description: >-
  Orchestrate a requested task through up to three subagents: decompose the
  work, select a suitable available model for each bounded assignment,
  delegate substantive execution, coordinate dependencies, and integrate and
  verify the results while the main agent remains the orchestrator. Use only
  when the user explicitly invokes orchestrate or asks the main agent to
  delegate the work and orchestrate it. Not for creating persistent subagent
  definitions. Does not broaden the task's scope or authority.
license: MIT
metadata:
  author: ta-dadadada
---

# Orchestrate

Delegate the task's substantive work to no more than three subagents. The main
agent owns decomposition, assignment, coordination, integration, verification,
and the final response.

## When to use

- The user explicitly invokes `orchestrate` or asks the main agent to delegate
  the work and act as orchestrator.

## When not to use

- Delegation is unavailable in the current environment.
- The request is to create or edit persistent subagent definitions rather than
  to execute the current task.

## Workflow

### 1. Partition

- Preserve the requested deliverable, constraints, authority boundaries, and
  applicable mandatory procedures.
- Split it into the fewest independently executable assignments, with disjoint
  ownership where possible. Keep dependent or tightly coupled work together.

### 2. Delegate and coordinate

- Create at most three subagents for the task; the main agent does not count
  toward this limit. Use fewer when more would not help.
- Match each assignment to a suitable available model by reasoning difficulty,
  domain fit, speed, and cost. Use the inherited or default model when selection
  is unavailable.
- Give each subagent a bounded outcome, necessary context and constraints,
  relevant instructions, owned files or evidence, and a completion condition.
  Run independent assignments concurrently; sequence dependencies.
- Monitor blockers, overlap, conflicting edits, and missing evidence. Redirect
  assignments rather than silently taking over substantive work. The main agent
  may perform only coordination, small integration edits, and verification.

### 3. Integrate

- Check every result against its assignment and the original request, resolve
  contradictions, and combine the work into one coherent deliverable.
- Run or delegate required verification. Report unverified claims and blockers
  explicitly; a subagent's success report is not sufficient evidence by itself.

**Done when:** every assignment is accounted for, the integrated deliverable
satisfies the original request and constraints, required verification has
passed or its limitation is stated, and the main agent has delivered one
coherent final response.

## Red flags

- Creating three assignments only to fill the available slots.
- Giving multiple agents overlapping write ownership without a merge plan.
- Waiting passively, taking delegated work back without cause, or repeating a
  subagent's conclusion without checking its evidence.

## Related

- `just-do-it` — the contrasting explicit mode for direct execution with
  delegation used only when it clearly reduces lead time.
