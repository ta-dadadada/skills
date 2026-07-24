---
name: hypothesis-driven-debugging
description: >-
  Hypothesis-first debugging workflow for defects whose cause is unknown:
  reproduce and capture the failure, localize it to a candidate region,
  form falsifiable hypotheses ranked by evidence, confirm or refute each
  by observation (instrumentation, debugger, bisect) — one variable at a
  time, with refuted hypotheses recorded so they are not retried — fix
  the confirmed root cause minimally, then verify by re-running the
  original reproduction and lock it in with a regression test. Use when
  investigating a failing test, wrong output, crash, or regression whose
  cause is not yet established, or when a supposed fix did not hold and
  the defect has resurfaced. Not for changes whose cause is already
  demonstrated, not for performance tuning, and not for live-incident
  mitigation where restoring service precedes diagnosis.
license: MIT
metadata:
  author: ta-dadadada
---

# Hypothesis-Driven Debugging

A fix is only made against a root cause confirmed by observation. A guess formed by reading code is a hypothesis, not a diagnosis — and a hypothesis earns a fix only after it predicts something and that prediction is checked. Shotgun changes (edit until it happens to pass) and symptom suppression (a null check that silences the error instead of removing its cause) are what this discipline replaces. The work is done when the original reproduction passes and a regression test exists that fails without the fix and passes with it.

## When to use

- Investigating a failing test, wrong output, crash, or regression whose cause is not yet established.
- A prior fix did not actually resolve the defect and it has resurfaced.

## When not to use

- The cause is already demonstrated — go straight to the fix.
- Performance tuning — a measure-first workflow, not a cause/effect hunt for a defect.
- Live-incident mitigation where restoring service precedes diagnosis.

## Workflow

### Step 1 — Reproduce and capture the failure

- Establish a minimal, deterministic reproduction: a command or sequence of steps that triggers the failure on demand. Record the exact symptom — error message, stack trace, expected versus actual output.
- When reproduction is not achievable, inventory the evidence that is available instead (logs, user reports, conditions under which it was observed) and mark reproduction as unavailable rather than forcing a fabricated repro. This raises the bar downstream: without a reproduction to fail and then pass, Step 3's confirmation and Step 5's lock-in both rest on accumulated observational evidence instead.

**Done when:** a command or procedure reproduces the failure with the exact symptom recorded, or the available evidence is inventoried with reproduction marked unavailable.

### Step 2 — Localize to a candidate region

- Narrow the symptom to a candidate region using the evidence at hand: the stack trace, tracing the data flow backward from the wrong output, recent changes (`git log`, or `git bisect` when it is cheap to run), and diffing against a working, closely related case.

**Done when:** a candidate region is named with the evidence that points there.

### Step 3 — Form and test hypotheses by observation

- List hypotheses grounded in the Step 2 evidence and order them by likelihood. For each, write down its prediction before testing it — what would be observed if it is true, what would be observed if it is false — then check it with instrumentation, a debugger, a minimal isolating test, or bisection.
- Change one variable at a time. Keep the hypothesis ledger in the investigation's working notes — a separate file only when the repo's conventions call for one. A refuted hypothesis goes into it with its refuting observation instead of being retried; return to the Step 2 evidence and move to the next hypothesis.
- A hypothesis is confirmed only when an observation matches its prediction *and* explains the full path from cause to symptom — not merely a correlation. Any instrumentation added for this investigation is flagged for removal in Step 5.

**Done when:** one hypothesis is confirmed by an observation that matches its prediction and explains the full path from cause to symptom, and every refuted hypothesis is in the ledger with its refuting observation.

### Step 4 — Fix the root cause minimally

- Fix at the point the confirmed cause originates, not at the point the symptom appears. Keep the diff scoped to the confirmed cause — every behaviour flowing from that same cause is in scope, while unrelated refactors and other suspicious-looking code go into separate work.
- When the cause turns out to hinge on a behaviour or spec judgment call (for instance, whether the current behaviour was ever intended), get the user's answer before writing the fix.

**Done when:** the diff addresses exactly the confirmed cause and any behaviour-level judgment call carries the user's answer.

### Step 5 — Verify and lock in

- Re-run the original reproduction from Step 1 and confirm it now passes — this is the primary verification; an existing test suite going green is not a substitute for it.
- Add a regression test that fails without the fix and passes with it. Remove the instrumentation flagged in Step 3, then run the surrounding test suite.

**Done when:** the original reproduction passes, a regression test fails without the fix and passes with it, instrumentation is removed, and the surrounding suite is green.

## Red flags

| Rationalization | Reality |
|---|---|
| "Let me just change this and see" | a change that happens to work leaves the actual cause unconfirmed |
| "This code looks suspicious, I'll fix it" | a fix against an untested hypothesis is a gamble, not a diagnosis |
| "Can't reproduce it, but it's probably this" | with no reproduction, confirmation must rest on accumulated observation, not a guess |
| "Add a null check and the error goes away" | silencing the symptom leaves the cause in place |
| "Fix a few likely candidates at once" | when several things change together, which one mattered stays unknown forever |
| "The test suite is green, so it's fixed" | the suite existed before the bug; the original reproduction is the actual judge |
| "Leave the debug prints in for now" | instrumentation is scaffolding for the investigation; remove it once the investigation ends |

## Related

- `characterization-testing` — building a safety net for cause investigation in code that has no tests.
