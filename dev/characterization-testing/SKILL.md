---
name: characterization-testing
description: >-
  Safety-net-first workflow for changing existing code that has no or
  untrusted tests: scope the observable behaviour that must survive the
  change, find the least invasive seam to get the code under test, write
  characterization tests that pin down what the code actually does today
  — capturing surprising or buggy behaviour as-is and reporting it
  instead of silently fixing it — then make the intended change with the
  net in place, so the failing tests are exactly the intentionally
  changed behaviours. Use before modifying, refactoring, or extracting
  legacy code that lacks tests, or when changes to an area keep breaking
  behaviour nobody predicted. Not for greenfield code, not for code
  already covered by trusted tests, and not for deciding whether current
  behaviour is correct — that decision belongs to the user.
license: MIT
metadata:
  author: tadaair
---

# Characterization Testing

A characterization test asserts what the code actually does, not what it should do — a bug-looking behaviour is captured and reported exactly as it is, and whether to fix it is a separate decision that belongs to the user. Nothing changes until this net is green; once the change lands, the net's failures should equal exactly the set of intentionally changed behaviours, and that match is what proves the change caused zero surprises.

## When to use

- Modifying, refactoring, or extracting existing code that has no tests, or whose tests are not trusted.
- Changes to a given area keep breaking behaviour nobody predicted.

## When not to use

- Greenfield code — write ordinary tests instead.
- Code already covered by trusted tests.
- Deciding whether the current behaviour is correct — that judgment belongs to the user, not this workflow.

## Workflow

### Step 1 — Scope the behaviour surface

- Enumerate the target code's observable behaviour surface: entry points, outputs, side effects (files, database, external calls), and known consumers.
- Split the surface into two lists: behaviour that must be preserved, and behaviour that this change intentionally alters.

**Done when:** a written list splits the observable behaviours into preserve and intentionally-change, with the entry points that exercise each.

### Step 2 — Find the seams

- Find the least invasive seam that gets the target code under test: an existing harness, a function callable as-is, or an injectable dependency.
- Any refactor performed only to create a seam is limited to mechanical, behaviour-preserving moves (extract, parameterize) and is recorded as such.

**Done when:** the test harness runs against the target code, and any seam-creating refactor is recorded as mechanical and behaviour-preserving.

### Step 3 — Write characterization tests

- For every behaviour on the Step 1 preserve list, exercise it with representative inputs — typical, boundary, and error paths — and pin the **actual** output as the expected value.
- Capture surprising or buggy-looking behaviour as-is, note it in the test, and report it to the user instead of fixing it silently. Coverage is measured against the Step 1 behaviour list, not a line-coverage percentage.

**Done when:** every behaviour on the preserve list has a test that passes against the current code, and every surprising behaviour found is captured as-is and reported.

### Step 4 — Make the intended change

- With the net green, implement the intended change. Check which tests now fail against the intentionally-change list from Step 1: only tests on that list get their expectations updated, each update carrying a reference to the intent it corresponds to.
- A failure outside that list is a real accident — fix the change, not the test.

**Done when:** the change is implemented and the set of updated tests equals the intentionally-change list, each update traceable to the stated intent.

### Step 5 — Hand off

- Report three things: the behaviour that stayed preserved (the tests still green), the behaviour intentionally changed (which tests were updated and why), and any surprising behaviour discovered along the way (left unfixed).
- Decide with the user whether the characterization tests become permanent or are pruned.

**Done when:** the report covers preserved / intentionally changed / surprising behaviours, and the keep-or-prune decision for the tests is made with the user.

## Red flags

| Rationalization | Reality |
|---|---|
| "Reading the code tells me what it does" | reading produces a hypothesis; only a test proves current behaviour |
| "This is obviously a bug, I'll just fix it" | mixing a fix into the safety net erases what the net was proving; report it and let the fix be a separate decision |
| "Let me refactor first to make it testable" | a large refactor with no net in place is exactly what causes accidents; seam creation stays mechanical |
| "Aim for 80% line coverage" | the bar is the Step 1 behaviour list, not a coverage number |
| "The test failed, just update the expected value" | a failure outside the intentionally-change list is a caught accident, not a stale expectation |
| "No time for a safety net, just make the change" | a change without a net costs more time later, in the investigation it forces |

## Related

- `hypothesis-driven-debugging` — diagnosing an existing bug once the net is in place.
- `purpose-driven-software-design` — the design judgment behind the change itself.
