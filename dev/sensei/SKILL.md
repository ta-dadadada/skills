---
name: sensei
description: >-
  Create a one-page visual PDF in Japanese that explains a topic or source material at a chosen level of prior knowledge: low (beginners new to the field), mid (readers who know the basics), or high (experts seeking depth and insight). Use when explicitly invoked or when the user asks for a visual handout, PDF, or one-page guide for beginner, intermediate, or advanced readers. Leave routine chat explanations and summaries to other workflows.
license: MIT
metadata:
  author: ta-dadadada
---

# Sensei

Help the reader explain one idea in their own words through a clear visual and concrete supporting detail in natural Japanese.

## When to use

Use for explicit invocations and requests for a visual handout, PDF, or one-page guide aimed at beginner, intermediate, or advanced readers. Skip routine chat explanations and summaries.

## Reader level

Take the level from a leading `low`, `mid`, or `high` argument, or from the audience the user describes (for example, 初心者 → low, 中級者 → mid, 上級者・専門家 → high). Default to `mid` when neither is given. Judge the level against prior knowledge of this topic, not general expertise.

| Level | Reader's starting point | How to explain the same subject |
|---|---|---|
| low | New to the field | Break the subject down so a reader without background can follow it. Explain only the few points that matter most (usually three or four) and the terms and background they need; leave out secondary details even when space remains. |
| mid | Knows the basic terms and ideas | Convey the material as a whole, organized for a quick read: group its points so the reader sees the overall structure at a glance, and skip explanations of familiar basics. |
| high | Can already derive the mid-level account independently | Spend the space on a specific detail of the central point: how it works, what supports it, under which conditions it holds, or what it implies in practice. Distinguish documented facts from inference. |

## Workflow

1. **Choose the takeaway.** Read the supplied source, if any. Before adapting to the reader, state the source’s central point in one sentence (or identify the central idea of the requested topic). Keep that point across levels; additional sources support and detail it but do not replace it. Adapt the vocabulary, background, and details used to explain it. If the topic or required source is missing, ask for it; if a supplied source is inaccessible, disclose the gap and ask for the material instead of substituting an unrelated explanation.
   At any level, read the supplied resources and, without asking, relevant pages linked directly from them when they help explain the takeaway to this reader. If that evidence is insufficient, identify the open question and proposed research, then ask the user and wait for approval before searching elsewhere or following links beyond that first hop. If the user declines, explain what the available evidence supports and identify the limit. Attribute supporting details to the source that establishes them.
2. **Build the explanation.** State the takeaway near the top, then explain the key relationship or sequence with a diagram, annotated illustration, or worked example. At mid and high, use the full page when a source detail helps this reader understand or apply the takeaway. For example, trace what happens in a specific case or show how the outcome changes under a different condition. Use short captions and define terms beyond the assumed background at first use. An analogy is optional; if its limits matter, state where it stops applying. Preserve any condition or uncertainty that changes the takeaway. Credit the source where the reader can find it.
3. **Lay out and export.** Use one page of Japanese text and visuals. Start with a single column; add a second or third only when it makes related items easier to compare or follow. Use at most three columns and keep their reading order obvious. If the page is crowded, cut secondary material or simplify the visual before reducing type size. Use a Japanese-capable font and keep body text selectable.
4. **Verify and deliver.** Confirm the exported PDF has exactly one page. Render and inspect it at normal reading size for missing glyphs, clipping, overlaps, legible labels, and clear reading order. Check that the headline and main visual convey the central point, that the assumed reader can reach it, and that any deeper analysis helps explain it. At mid and high, if substantial space remains, revisit the source for a useful detail the draft omitted. Keep the space when the explanation is already sufficient or the separation helps the reader follow the visual. Check that the visual and prose agree with the source or verified facts. Fix issues before sharing the PDF. If the available environment cannot produce or verify the PDF, explain what is blocked and label any draft as incomplete.

## Red flags

- Child-directed wording or an analogy that obscures how the subject actually works.
- A decorative image that does not help answer the reader's question.
- Tiny type or extra columns used to squeeze in secondary points.
- A higher level that restates the lower-level account in denser jargon instead of adding substance.

## Related

Inspired by [Anthropic's ELI5 skill](https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md) and its emphasis on visual explanation.
