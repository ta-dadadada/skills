---
name: kono-hen
description: >-
  Turn a rough remark and its conversational context into one ready-to-use
  prompt that gives another agent direction and room for judgment. Use when
  the user asks for a prompt or instructions to give an agent. A vague request
  to perform the work itself does not trigger this skill.
license: MIT
metadata:
  author: ta-dadadada
---

# Kono Hen

Give the receiving agent enough context to choose a good approach. The user
can have a clear preference about the result while leaving the method open.

## When to use

Use for a prompt-writing request or an explicit invocation with a rough idea.
For a direct request to do the underlying task, do the requested work.

## Workflow

1. Read the remark in context. Identify what prompted it, what the user wants
   to change or preserve, and whose experience matters. Use details the user
   supplied, including earlier decisions that still apply. A concrete phrase
   like “I want to remember why we did this” can carry more intent than a
   generic instruction to “improve the document.”
2. Express the desired difference in terms the receiving agent can use to
   judge its choices. Carry over explicit constraints and keep suggestions
   optional. Leave structure, technique, and style open wherever the user
   delegated them. Omit invented metrics, process steps, and deliverables.
3. Draft directly when the remaining choices can be made by inspecting the
   material or exercising judgment. Ask one focused question only when
   plausible readings lead to materially different goals or scopes and the
   conversation gives no basis for choosing. After the answer, draft the prompt.
4. Return one copy-ready prompt in the user's language unless another language
   was requested. Resolve references such as “this” with the relevant title,
   input, or a short excerpt so the recipient can start without the chat history.
   If material must travel with the prompt, mark where to attach or paste it.

Done when the recipient knows what to work on, what a good result would
achieve, and has room to choose how. A short paragraph is enough when it
conveys all three.

## Examples

**Draft directly.** “These work notes will have me wondering why we did this
in a month. Turn that into a prompt.”

> Edit the attached work notes so that, a month from now, I can trace the
> reasons for the decisions we made. Use whatever organization fits the
> notes. Where the notes give no reason, leave that gap visible.

**Clarify the goal.** “Write a prompt to get this proposal ready for Friday.”
If Friday's meeting has already been described as a funding decision, use
that context. If the conversation leaves both approval and early feedback
plausible, ask “What do you want the people in Friday's meeting to do after
reading the proposal?” Slide count and section order can wait for the agent.
