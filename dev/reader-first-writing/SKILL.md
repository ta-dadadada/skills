---
name: reader-first-writing
description: >-
  Create or revise reports to reduce length and reading effort while preserving
  necessary information and clear logical relationships. Use only when the user
  explicitly invokes this skill. Develop the central question, abstract, and body
  in that order; reconstruct conversations around their final judgments.
  Not for memorable rhetorical effects, copywriting, or verbatim records.
license: MIT
metadata:
  author: ta-dadadada
---

# Reader First Writing

An agent creates a report from source material or revises an existing document.
This writing procedure reduces length and the reader's work of finding conclusions,
reorganizing information, and supplying missing logic while preserving necessary information.

Assume readers may not want to read from beginning to end. Make the destination clear
at the start so they can skip familiar material and unnecessary detail while still
meeting their needs. Getting everyone to read the whole document is not a success criterion.

## When to use

- The user invokes this skill to create a report from material or conversations.
- The user invokes this skill to make an existing document's structure and wording more concise.

## When not to use

- Speeches, copy, or narrative writing whose primary purpose is to leave an impression.
- Requests that require a verbatim transcript or chronological record itself.
- Automatic application to ordinary conversation or every writing task.

Removing an "AI-like" style is not an independent goal. Judge repetition, ambiguity,
and unnecessary emphasis by the burden they impose on readers, not their presumed origin.

## Workflow

### 1. Understand the sources and choose the central question

- Read the requested scope. Establish the audience, existing knowledge, purpose, and
  destination from the request and context. Follow a specified audience's knowledge
  and needs; otherwise, assume a reader who did not participate in the conversation.
  Do not reconfirm settled conditions. Ask only when audience differences materially
  change the central question or necessary information and context cannot resolve them.
  Continue work that ordinary editorial judgment can settle.
- Identify claims, evidence, conditions, exceptions, uncertainty, and the distinction
  between decisions, proposals, withdrawn ideas, and unresolved matters. Establish what
  readers need to understand or judge before shortening the document.
- Define the central question as the reader's question this document answers. Do not
  choose an unsupported conclusion first or promote an unaccepted proposal into a decision.
- Connect that question to the understanding, judgment, or action needed after reading,
  where known. If the document combines roles such as a status report and a detailed
  record, separate its primary role from material reserved for detail. Do not assume
  it requests approval when its purpose is unknown.
- When revising, preserve meaning and the requested editing scope. Respect constraints
  on numbering, reference targets, required headings, and format.

**Done when:** the central question, information to retain, and unresolved matters are
understood. Working notes need not be presented each time, and each stage does not
require user approval.

### 2. Construct the abstract

Use [Abstract construction](#abstract-construction) to draft an answer whose purpose,
method, and result form a relationship understandable on its own.

**Done when:** the abstract alone explains the problem, approach, outcome, and what
follows from them. The body can be organized to develop that core. This is a provisional
abstract; finalize it by checking consistency after writing the body.

### 3. Build the body

Write the body so the abstract's core can be understood and examined in detail.
Use [Designing how much readers need to read](#designing-how-much-readers-need-to-read)
to separate reading scopes, and [Information placement and reconstruction](#information-placement-and-reconstruction)
to organize evidence and detail.

### 4. Compress the wording

After arranging the information, apply [Sentence and phrase compression](#sentence-and-phrase-compression)
to remove words and sentences while retaining necessary information and logical connections.

### 5. Compare and deliver

- Compare with the sources for unchanged necessary information, numbers, conditions,
  exceptions, certainty, and decision status. Do not settle unresolved matters through editing.
- Check that the abstract alone conveys the purpose–method–result relationship and that
  background and implications connect to that core. Compare both ways: no unsupported
  claims beyond the body, and no missing main results or important conditions. Update
  the abstract when the body changes.
- Check whether deletion makes readers infer more. Before adding an explanation,
  consider whether placement or concrete wording can make it unnecessary.
- For a two-layer document, verify that the short main text alone supports the required
  understanding or judgment. Distinguish reducing total length from reducing required
  reading; moving material into details is not deletion.
- Apply [Designing how much readers need to read](#designing-how-much-readers-need-to-read)
  to test each opening sentence and the information added by the details. Remove repeated
  answers to the same question. Apply [Reader assumptions and explanation](#reader-assumptions-and-explanation)
  to check whether conversation-specific labels need to remain.
- Deliver the requested document or revision proposal, briefly noting material unresolved
  passages. Do not append a narration of the editing process or every change rationale.

**Done when:** the central question is clear at the start, necessary information and its
certainty are preserved, and readers can understand relationships without supplying
missing logic. Removable wording is gone and unresolved gaps are explicit. Reduced
length alone is not evidence of information preservation or readability.

## Writing techniques

Use these criteria at the relevant workflow stages. Organize information first,
then refine sentences and phrases.

### Reader assumptions and explanation

- Distinguish someone absent from the conversation from a domain beginner. Clarify
  document-specific roles, terms, and decision status without explaining all domain basics.
- Where different interpretations affect understanding or action, make the actor,
  meaning, and certainty unambiguous. First try concrete wording, then add only the
  explanation still needed. Match terminology explanations to the request and purpose.
- Make roles and document-specific terms understandable on first use, including in the
  opening. Avoid shorthand whose actor becomes clear only in a later definition. Do
  not expand a brief parenthetical explanation into a separate paragraph.
- Give distinct names to operations or states readers must distinguish, and use them
  consistently in state labels. For example, distinguish receipt from content review
  when both are called "checked," or creation from approval when both are called "done."
  These are examples: inspect terms that admit different meanings in the actual document.
- Do not carry conversation-specific labels or responses to earlier requests into the
  document as shared reader knowledge. Decide whether readers need the term itself or
  only the behavior. If behavior suffices, describe what happens rather than retaining
  and explaining the label.

### Judgment ownership and certainty

- Make decisions, proposals, and unresolved matters explicit through headings or labels
  where needed; do not leave the distinction to shifts in sentence endings. Separate
  adoption from verification: an adopted approach can still be untested.
- Do not hide the decision-maker behind phrases such as "it was recommended." If ownership
  matters, identify the actor from evidence. Otherwise, state what the proposal is directly.
  Do not turn a proposal into agreement.
- State shared sources, dates, and caveats once with a clear scope, near the beginning
  if appropriate. Repeat a caveat only for a different condition or to explain the next
  action. Do not repeat it in every section just in case; identify the specific misunderstanding
  its removal would cause. Under a heading such as "Design proposal," write directly rather
  than ending every sentence with "is proposed." Do not make blanket assertions across
  mixed decisions and proposals.
- Separate attribution from the summarizer's working circumstances. Avoid phrases such
  as "recorded in the supplied conversation." If needed, identify once whose discussion
  about what is summarized, then state its substance directly. Do not present historical
  research as verification performed now.

### Abstract construction

An abstract here is a condensed version of the body's logic that stands on its own.
An extracted conclusion or list of topics is insufficient. Connect what needed solving,
the method or basis of judgment, and the outcome so readers can also decide whether
they need the body.

- Start with a purpose–method–result core. In a report, these correspond to the problem,
  approach or comparison criteria, and resulting findings or decisions. Explain how
  the method serves the purpose and how the result answers it. Merely including all
  three is insufficient if readers must consult the body or infer their connection.
- Add the background needed to understand that core and what follows from the result.
  Tie both to this problem and outcome, rather than generic context or declarations
  of importance. Retain conditions, limits, and unresolved matters that change the result's meaning.
- In a report on a concept, the result can be a design decision. Do not describe planned
  work as completed or expected benefits as verified outcomes. Do not invent methods
  or implications absent from the sources.
- Select the main results that answer the central question; do not pack in every secondary
  finding. Make the core and its meaning understandable without body references or unexplained terms.
- Do not substitute a preview such as "This document describes..." for the answer. If
  the title or answer makes the purpose clear, omit declarations of purpose or audience.
- Refine connections so each sentence's role and relationship are clear. Fixed headings
  or stock phrases for background, purpose, method, result, and significance are not
  required. Prioritize early understanding of the destination; a short reason and
  conclusion may share one sentence.
- Neither an "Abstract" heading nor a paper format is mandatory. The opening of a short
  document may serve this role, but do not sacrifice logical connections for brevity.

### Designing how much readers need to read

- Use two layers when immediate understanding or judgment is mixed with details needed
  for checking or recordkeeping. Let the opening summary and necessary next actions
  form a complete short main text; place requirements tables and design specifics in
  subsequent "Details" or appendices. Do not require readers satisfied by the short
  text to read all the details.
- Test each opening sentence: would removing it prevent understanding of the purpose,
  outcome, or necessary next judgment or action? If not, move its specifics to the
  details, or delete it if already covered there. Keep methods and reasons necessary
  to understand the answer's logic.
- Details should add evidence, conditions, or specifics absent from the summary. Delete
  passages that merely restate the same answer to the same question. Allow minimal
  repetition to show correspondence, but do not interpret "elaborate" as repeating an explanation.
- Put technical information or reference lists that do not change the reader's judgment
  in details or appendices if needed for the record; otherwise omit them. Separate files
  must respect the requested delivery scope and have explicit references.
- Adapt length targets such as one screen to the purpose and display environment. Do
  not remove necessary conditions or reasons to meet a fixed count or reduction percentage.

### Information placement and reconstruction

- Arrange evidence and information that develop the abstract around the reader's questions.
  Keep related information together and let headings guide selective reading.
- Connect the title's subject to the opening with the same concrete name. Keep one topic
  per paragraph. Collect material readers check together, such as exclusions, in one
  place, separated by a heading, paragraph, or list rather than appended to another topic.
- Put requirements with requirements and caveats with caveats. Do not attach unrelated
  material to the previous sentence with "especially" or "also."
- Reconstruct conversation logs around final judgments rather than discussion order.
  Omit temporary changes of direction and deliberation history unless readers need them.
- When comparison is needed, show the chosen and rejected options and the criteria.
  Do not retain an option merely because it was considered. Keep change history when
  needed to understand impact or for auditing, without replacing the original rationale
  with a different one after the fact.
- Use who, what, when, where, why, and how to fill only necessary gaps that context does not resolve.
- Use lists for parallel items or steps, and tables for comparison on common dimensions.
  Do not fragment a short causal explanation or create multiple items that restate one
  judgment. For simple enumerations such as update occasions or retained records, put
  the shared action in the heading and omit repetitive endings and connectors.
- Do not pack different things to check into one table cell. Use lists rather than prose
  chains for independently selected items such as verification tasks and references.
- Place numbers, versions, and environment details where their relevance to the reader's
  judgment is clear. Omit them if irrelevant. Do not strengthen existence checks into
  readiness claims merely to give them a purpose.

### Sentence and phrase compression

- Remove preambles, repeated assurances, generic statements or concessions that do not
  inform judgment, and explanations serving the same role.
- Keep reasons needed to understand a choice or a non-obvious causal relationship. Omit
  restatements of effects already apparent from the action. Retain reasons whose removal
  would obscure criteria or applicable conditions.
- Prefer concrete actions, states, and reasons to abstract evaluations. Explain what
  changes and how instead of repeating that something is important.
- Combine a closely connected reason and conclusion if they remain short. Do not pack
  separate points together and make readers split them. Judge splitting and combining
  by both length and ease of understanding.
- Connectors alone do not repair missing logic. Retain reasons and conditions that
  determine the conclusion. Do not obscure referents by dropping subjects or names.
  Make the object of actions such as replying or checking clear from first use.
- Use analogies and examples when they reduce understanding effort, not for memorable effects.

Example:

> To meet the mandatory deadline, we selected B. A costs less than B but misses the deadline.

There is no need to split this into "We selected B. This is because it meets the mandatory
deadline." This example assumes the choice and timing are supported by the sources;
do not invent them while editing.

## Red flags

| Shortcut | Criterion |
| --- | --- |
| Keeping everything is faithful | Preserve what readers need, not every turn of deliberation. |
| Shorter is better | Check whether omissions require more inference or reorganization. |
| The conclusion must be the very first words | A short reason may precede it if the judgment is clear immediately. |
| Politeness requires explaining purpose or importance | Omit declarations and assurances already clear from the content. |

## Related

- [How to write an abstract: four steps with examples](http://www.ams.eng.osaka-u.ac.jp/user/ishihara/?p=626)
  (Japanese): source for the purpose–method–result relationship. This skill adapts it to
  reports, drafting a provisional abstract from the central question and finalizing it
  through comparison with the body.
- [document-context-edit](../document-context-edit/SKILL.md): clarify conversation-dependent
  terms and premises while retaining document structure.
- [work-report](../work-report/SKILL.md): report outcomes for a defined period or work scope.
- [shiranui-hanten](../../meta/shiranui-hanten/SKILL.md): revise this skill itself.
