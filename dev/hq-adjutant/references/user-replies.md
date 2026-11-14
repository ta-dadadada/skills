# Replies to the user

Every reply has three parts, in this order: waiting on you, then what changed, then next moves. Build "what changed" from this turn's CLI receipts, not from re-reading the ledger.

The examples are in English for maintainers. Write real replies, headings and labels included, in the HQ language — for `ja`, for example: `あなた待ち` / `変化` / `次の動き`, `(報告のみ・未検証)`, `(検証済み: <読んだもの>)`, `(不明)`.

## Labels

| Label | Meaning |
|---|---|
| `(reported, unverified)` | the session claimed it; you have not checked it |
| `(verified: <what you read>)` | you read the artifact, branch, PR state, or diff |
| `(unknown)` | no parsable report, or the session is missing from host listings |

## Example: note-triggered turn

A note from `local_a1` arrives. The first action is `report` with the note piped in verbatim. The receipt:

```json
{"ok":true,"task":"T3","session":"local_a1","state":"waiting-user","parsed":true,
 "waits_opened":[{"id":"W4","kind":"approval","summary":"git push origin feat/retry"}],
 "waits_resolved":[],"artifacts_added":["A2"]}
```

Before presenting W4, you confirm that the branch exists and that its diff matches the claim. The reply:

```
Waiting on you
- W4 (T3 retry fix): approve `git push origin feat/retry`? Branch checked: 3 commits, diff limited to src/retry/ (verified: git log/diff).

What changed
- T3: tests pass, ready to push (reported, unverified beyond the diff).

Next moves
- After your answer, I forward it to T3. T5 is queued behind T3 (depends_on).
```

## Example: user's turn answering approvals

The user writes: `W4 yes, W5 not yet`. Run `wait resolve W4 --resolution 'user: "W4 yes, W5 not yet"'`. Then message T3's session with the approval template, quoting those words. Leave W5 open. The reply:

```
Waiting on you
- W5 (T4 docs): approve opening PR "Add retry guide" against main? Still open.

What changed
- W4 forwarded to T3 with your words; push pending its next report.

Next moves
- T3 reports after pushing; I check that the remote branch exists before calling it done.
```

## Tone

- Put the conclusion first. One line per item. Avoid adjectives about progress.
- Leave out greetings, sign-offs, apologies, and restatements of the request.
- Do not role-play a character. "Staff officer" describes the order and brevity of the reply, not a voice.
