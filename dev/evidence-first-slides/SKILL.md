---
name: evidence-first-slides
description: >-
  Create or revise technical presentation slides, outlines, and reusable slide
  templates with explicit evidence, claim-led headings, visible assumptions,
  and an unambiguous reading order. Use only when the user explicitly invokes
  this skill or asks for this evidence-first slide method. Complete the requested
  artifact using available authoring tools; design-only requests end with a
  usable specification. Not for advertising copy, slogan slides, or prose-only
  reports.
license: MIT
metadata:
  author: ta-dadadada
---

# Evidence First Slides

Build technical presentations whose claims can be examined from the slides and
whose reasoning becomes easier to follow when spoken. Preserve the discipline
of a scientific talk without requiring equations, charts, or a particular tool.
The primary responsibility is slide content and design, including production of
the requested artifact, not operation of a specific presentation application.

## When to use

- Explicit requests to apply this method when creating or revising a technical
  deck, selected slides, an outline, or a reusable slide template.
- Reuse accepted decisions from the conversation or existing material; do not
  restart preference interviews for each revision.

## When not to use

- An unrelated presentation request without invocation of this method.
- Advertising, copywriting, or a one-line rhetorical effect as the deliverable.
- Prose-only reports or generic application configuration.

## Workflow

### 1. Establish the requested outcome

Identify the subject, audience knowledge, speaking time, available evidence,
existing material, and requested deliverable. Distinguish deck structure from
visual-template choices. Ask only for missing information that changes the work;
use established preferences and clearly stated assumptions for routine choices.

Treat a requested draft as an editable handoff for the user's own revision.
Keep the argument, evidence status, and legibility sound; do not pursue finished
copy or repeated aesthetic refinements unless requested.

Create from sources or revise the requested scope of an existing artifact.
For an outline, deliver slide purposes, claims, evidence, and sequencing. For a
template, provide reusable layout rules and filled examples, not empty boxes.
For a deck or sample request, produce the actual requested slides using available
tools and formats. Do not substitute a plan for authorized production work.
Do not infer permission to publish, send, or install software from skill use.

**Done when:** the deliverable and its boundaries are clear, and material gaps
in evidence are identified rather than silently filled with invented findings.

### 2. Establish the argument and its evidence

- Identify the central message the audience should take away, preserving the
  user's stated message and its status as a proposal, finding, or hypothesis.
  Choose examples and supporting topics to develop it; an accessible example
  must not replace the main argument. If sources leave a gap, expose it rather
  than silently changing the message or inventing support.
- For a complete presentation, include a title slide that identifies the talk
  and, when supplied, its speaker and occasion. Do not invent those details.
  A title slide is a framing element, not a slogan-only content slide, and does
  not need the content-slide density target. Honor explicit requests for excerpts
  or a deck without a cover; count the cover within any requested total.
- Before the main argument, establish shared premises: the relevant background,
  the problem it creates, why that problem matters, and the hypothesis or question
  that motivates the investigation. Make the links between them explicit. Allow
  several opening slides when needed; a title, agenda, or immediate conclusion
  does not substitute for this grounding.
- Make the problem, what would be useful to learn, and why the answer matters
  understandable across the presentation.
- Follow the investigation from question through method, results, interpretation,
  and next test as appropriate. This may span slides; do not force a complete
  cycle onto each slide or impose a fixed chapter sequence.
- Separate observed or derived results from interpretation, hypotheses, and
  untested claims. Results include what meets or misses an explicit criterion.
  Explain why a remaining gap matters and why the next hypothesis is reasonable.
- Keep every premise, limitation, and disadvantage that changes interpretation
  or a decision on the slides. An informed reader must be able to follow the
  reasoning without discovering a missing premise only during the talk.
- Oral explanation may guide attention, supply intermediate reasoning, and
  describe trials, frustrations, or nuance that does not reverse the written
  conclusion. Leave that speaking freedom instead of writing a full transcript.
- Never invent measurements to fill a results section. Label illustrative data,
  code walkthroughs, assumptions, and actual observations distinctly. Attribute
  external evidence where the audience can locate it.

Keep results and discussion on one slide only when their relationship fits
legibly. Prefer a separate discussion slide when explaining causes, hypotheses,
or the significance of a gap needs space. Plan the argument across the deck before
dividing it into slides. Each slide needs an identifiable role in that argument,
not an independently complete miniature argument. Established premises can carry
forward with a clear reference; keep new or changed conditions visible where they
matter. Never require each slide to repeat background, hypothesis, evidence, and
conclusion. Split for the audience's reasoning pace as well as for physical fit.

**Done when:** the opening establishes the premises needed for the main argument,
and each transition uses knowledge already introduced or explicitly supplies it.

For a complete talk, end with a substantive summary that acts as its abstract:
problem, approach, findings, significance, and material conditions. Do not end
with a thank-you-only slide. Do not append a whole-talk summary to a requested
single-slide sample merely to satisfy this rule.

### 3. Write claims at the appropriate level

- **Title:** identify what this slide explains: a concrete question, subject, or
  supported finding. If that remains unclear, fix the title first. For example,
  name the metric rather than writing only "Cache evaluation."
- **Optional subtitle:** give a short supporting claim that extends the title.
  Do not repeat the title, announce the speaking agenda, or collect methods and
  scope into a paragraph here. Put criteria and conditions in the relevant body
  section. Omit the subtitle when it contributes nothing.
- **Body heading:** state the claim directly when possible. Under it, use concise
  bullets for evidence, conditions, or explanation. Avoid an extra classification
  heading such as "Findings" above a bullet that merely states the real heading.
- Classification labels such as "Evaluation criteria" or "Procedure" remain
  useful for locating information. Do not turn every heading into an assertion.
  Mark an inference or hypothesis when a claim-shaped heading could otherwise
  be mistaken for an established fact.

Use sober, precise language. Do not exaggerate or devote a slide to a one-line
hook or joke. Aim for enough substance to support roughly one to three minutes
of explanation per content slide, adjusting for the task rather than padding
text or enforcing a timer. This is not a rule for covers or other framing slides.

For wording, reduce the audience's need to translate abstractions into meaning:

- Name the actual object and action when known. Prefer "AGENTS.md lists the
  relevant documentation" to "Tool-specific entry points support the index"
  when that is the intended claim. Preserve any condition on tool support in
  the nearby explanation; concrete wording must not broaden the claim.
- Use technical concepts when the audience needs them, explaining their meaning
  on first use. Do not replace concrete files, people, or operations with vague
  metaphors such as "entry point" merely to make a heading sound general.
- Keep reasons, conditions, and uncertainty that affect interpretation. Shorten
  by removing repeated claims and empty emphasis, not by leaving the causal link
  for the audience to supply.
- Use contrasts and parallel phrasing when the content calls for them. Do not
  invent an opposing view, repeat "not X but Y," or force every slide into three
  balanced statements. Plain topic headings are fine when a claim sounds forced.

### 4. Choose evidence and arrange the reading order

Give space to what this audience can directly interpret: code, a plot, a log,
a table, a diagram, or text. A diagram must explain an actual relationship;
decorative simplification is not evidence of understanding.

- Use a top-to-bottom single column for text-led reasoning.
- Use two columns when the roles are clear, such as evidence on the left and
  its explanation on the right. Paired alternatives may also use columns.
  Do not distribute unrelated text sections into a grid with competing reading
  orders.
- A conclusion supported by the whole middle block may span the full slide
  below it. Do not confine that conclusion to one evidence column by default.
- Put criteria and scope near the evidence they qualify. Material premises and
  limits use readable body-sized, high-contrast text, not faint footnotes.
- Make code recognizable through a monospaced font, preserved indentation, and
  a distinct background or border. Keep evidence legible at presentation size.
- Split at a logical boundary when necessary explanation does not fit. Do not
  solve crowding by hiding conditions, shrinking essential text, or arbitrarily
  dividing information that needs to be compared together.

When building layouts or choosing an unspecified visual theme, read
[references/LAYOUTS.md](references/LAYOUTS.md). Reuse an accepted visual direction.
When preferences are unresolved, compare a few samples with identical content;
hold layout fixed when eliciting color preferences. Treat color preference as
preference, while checking legibility separately. Avoid unnecessary decoration.

**Done when:** claims have support, epistemic status and conditions remain
visible, and the arrangement cues a clear explanation order.

### 5. Produce, inspect, and deliver

Use any suitable authoring environment; this skill requires no vendor API,
model, slide library, browser, file format, or companion skill. Keep text, code,
and evidence editable when the requested format supports it. Respect supplied
templates and explicit user constraints when they differ from defaults.

For produced slides, render or open every changed slide at its intended aspect
ratio and inspect wrapping, overflow, hierarchy, reading order, code indentation,
and the visibility of important conditions. Inspect affected neighboring slides
when sequence or shared styles change. Repair problems and inspect again.
For an outline or design-only task, inspect its text and layout specification
and state that visual rendering has not been verified.

Read titles, subtitles, and headings together to catch repetition, unsupported
certainty, and category labels that delay the real claim. Then check the detail
against the sources. A geometry check alone cannot establish factual validity.
Also read the deck in sequence as a first-time listener: check that the opening
grounds the problem and hypothesis, that unfamiliar terms are introduced before
use, and that slides develop the argument rather than repeatedly restart it.
Check that the opening, examples, and summary develop the central message.
For drafts, make one focused wording pass using step 3 and deliver after material
errors are repaired. Leave optional stylistic polish to the user; report only
unresolved issues that affect meaning or use, not a list of taste preferences.

**Complete when:** the requested artifact is delivered, applicable content and
visual checks are done, important conditions and evidence status are explicit,
and any unverified rendering or missing source evidence is reported. If tools
cannot produce the requested format, preserve a usable source/specification and
report the limitation; do not claim the requested artifact is complete.

## Red flags

| Pattern | Correction |
| --- | --- |
| The audience must hear a hidden assumption | Put it beside the claim or evidence in readable text. |
| A polished result omits an operational drawback | Include it if it changes the judgment. |
| Every text section becomes a card or column | Restore one reading order unless comparison requires columns. |
| "Results" introduces a bullet that is really the heading | Promote that claim and keep its evidence underneath. |
| A subtitle describes what the presenter will do | State a short supporting claim or remove it. |
| A one-line hook replaces substance | Show the concrete issue and evidence without rhetorical inflation. |
| Every slide must stand alone | Preserve the deck's cumulative reasoning and make dependencies clear. |
| The title or agenda is the entire introduction | Establish background, problem, and motivating hypothesis before the main argument. |

## Related

- [Layout examples and visual defaults](references/LAYOUTS.md) — use during
  layout construction or visual-theme selection; examples are not mandatory slots.
