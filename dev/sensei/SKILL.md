---
name: sensei
description: >-
  Create a one-page visual PDF in Japanese for readers new to a topic or
  source material. Use when explicitly invoked or when the user asks for
  a beginner-friendly visual handout, PDF, or one-page guide. Leave routine
  chat explanations and summaries without a beginner audience to other workflows.
license: MIT
metadata:
  author: ta-dadadada
---

# Sensei

Help a first-time reader grasp the core idea through a clear visual and a few well-chosen words. Write natural Japanese for a reader who is new to the subject, regardless of age.

## When to use

Use for an explicit invocation or a request for a visual handout, PDF, or one-page guide for beginners. Skip ordinary chat explanations and summaries that do not target beginners.

## Workflow

1. **Choose the takeaway.** Read the supplied source, if any. Identify what the reader should be able to explain after reading and write it in one sentence. Assume no subject-specific knowledge unless the request says otherwise. If the topic or required source is missing, ask for it; if a supplied source is inaccessible, disclose the gap and ask for the material instead of substituting an unrelated explanation.
2. **Build the explanation.** State the takeaway near the top, then explain the key relationship or sequence with a diagram, annotated illustration, or worked example. Use short captions and define necessary technical terms at first use. An analogy is optional; if its limits matter, state where it stops applying. Preserve any condition or uncertainty that changes the takeaway. Credit the source where the reader can find it.
3. **Lay out and export.** Use one page of Japanese text and visuals. Start with a single column; add a second or third only when it makes related items easier to compare or follow. Use at most three columns and keep their reading order obvious. If the page is crowded, cut secondary material or simplify the visual before reducing type size. Use a Japanese-capable font and keep body text selectable.
4. **Verify and deliver.** Confirm the exported PDF has exactly one page. Render and inspect it at normal reading size for missing glyphs, clipping, overlaps, legible labels, and clear reading order. Check that the visual and prose agree with the source or verified facts. Fix issues before sharing the PDF. If the available environment cannot produce or verify the PDF, explain what is blocked and label any draft as incomplete.

## Red flags

- Child-directed wording or an analogy that obscures how the subject actually works.
- A decorative image that does not help answer the reader's question.
- Tiny type or extra columns used to squeeze in secondary points.

## Related

Inspired by [Anthropic's ELI5 skill](https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md) and its emphasis on visual explanation with few words.
