# Layout Examples and Visual Defaults

Use these examples to apply the main workflow. They illustrate choices, not a
universal slide skeleton. Keep necessary content and evidence relationships ahead
of a preferred composition.

## Title and opening sequence

A complete talk starts with a title slide identifying its subject, with supplied
speaker or event details when relevant. It is not a dense content slide. Follow
it with enough grounding for the audience to share the presenter's premises.

For an information-access talk, an illustrative progression is:

1. Title: "AI Ready repositories and information access."
2. Background: agents work in existing repositories under time and cost
   constraints; previous project knowledge may not carry into a new session.
3. Problem: repeated discovery and irrelevant reading consume resources even
   when the information exists. Explain the concrete task where this matters.
4. Hypothesis: discoverable sources and reliable module boundaries may reduce
   that work. Explain why those mechanisms address the stated problem.
5. Main argument: examine navigation, local contracts, and their limits using
   examples that build on the opening.

This is a dependency sequence, not a prescribed slide count. Combine or expand
parts to suit audience knowledge and explanatory depth. The hypothesis slide may
rely on the problem just established; it need not restate the whole opening.
Later slides can develop one example across several pages. Choose section counts
from the argument instead of reproducing the same three-section layout everywhere.

## Evidence with explanation, then a full-width finding

1. Title: "TTL caching can return an old value after a database update."
2. Optional subtitle: "Updating the database leaves a valid cached value intact."
3. Middle left: the actual code or pseudocode under discussion.
4. Middle right, top: criterion and assumptions.
5. Middle right, below: the procedure needed to interpret the evidence.
6. Below both columns, full width: a claim heading with supporting details.

Illustrative walkthrough, not benchmark data:

```python
value = cache.get(key)
if value is None:
    value = db.read(key)
    cache.set(key, value, ttl=60)
return value
```

The criterion is to return the latest value after a completed update. Assume one
cache, expiration exactly 60 seconds after insertion, and no concurrent reads,
writes, or failures. Cache A at time 0, update the database to B at time 10, and
read at times 20 and 60. These conditions belong in the right-hand body, not
in a faint footer or a long subtitle.

Use the following full-width finding below that evidence:

**An old value can be returned within the TTL**

- At 20 seconds: A is returned; the latest value B is not read.
- At 60 seconds: the expired entry triggers a database read, returning B.

## Text-led discussion in one column

Title: "Can invalidation after an update reduce stale reads?"

Optional subtitle: "Deleting the updated key is a candidate for forcing a fresh read."

Arrange these claim-led sections vertically:

**A shorter TTL does not eliminate stale reads immediately after an update**

- A database update does not change the cached value.
- A cache hit within the TTL skips the database read.

**Hypothesis: deleting the updated key directs the next read to the database**

- An absent key causes the shown read path to fetch the database value.
- This requires update, deletion, and read to complete in sequence; concurrent
  execution remains unverified.
- Invalidation responds to an update while allowing reuse between updates.

**Concurrent correctness and database load need further validation**

- Vary interleavings to check whether an old value can be inserted again.
- Check stale reads after deletion failure and the extra database reads caused
  by invalidation.

Do not arrange these sections as a two-by-two grid. Split discussion across
slides if explaining the mechanism or test rationale needs more room.

## Whole-talk summary

Close a complete presentation with its abstract: why the problem matters, what
was investigated, what was established, and what follows within the stated limits.
Select statements from the actual talk. Do not substitute a list of chapter names,
a new unsupported recommendation, or a thank-you-only slide. This layout remains
content-dependent; there is no fixed number of summary bullets.

## Default palette and typography

Use this accepted starting palette when no user template or visual direction
supersedes it. Its pale blue and lavender direction was inspired by
[kurageu.com](https://kurageu.com/); the dark text colors are adaptations for slides,
not a claim to reproduce the site's brand specification. The palette is complete
here: visiting the site or reusing its imagery is not required.

| Role | Color |
| --- | --- |
| Slide background | `#F1FBFF` |
| Body text | `#29364D` |
| Claim headings | `#365E91` |
| Code background | `#EFEEFF` |
| Code border | `#B5BFFC` |

Use a legible font with coverage for the presentation's language, and a monospaced
font for code. Set a clear hierarchy without relying on faint text. Font size,
spacing, and aspect ratio depend on the actual medium and content; check them
visually rather than treating this palette as proof of readability. Maintain
visible code indentation and enough separation between heading and supporting
bullets. Avoid decorative panels for ordinary prose.

When comparing visual options, keep the wording, information, and layout constant
to isolate color or typographic preferences. A preference for code occupying the
main area is evidence about information hierarchy, not automatically a preference
for that sample's colors.
