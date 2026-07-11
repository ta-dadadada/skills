# Agent Skill Design Principles

How to design agent skills that stay reusable across tasks, tools, and model
generations. Synthesized from vendor documentation (Anthropic, OpenAI,
Microsoft, Google), the Agent Skills open standard, and agent-design
research.

## What a skill is — and is not

A skill is a **reusable procedure package**, not an override of model
capability. It standardizes: in what order to check what, under which
conditions to use which tool, and what done-criteria the output must meet.
Skills do not replace tools or MCP — Anthropic positions Skills as
complementing MCP by describing the complex workflows that *use* external
tools.

The most portable unit is the Agent Skills standard's folder form:
declarative metadata + procedure + auxiliary resources, kept loosely coupled
from the runtime. The skill describes *what to do and how to proceed*; the
runtime provides *execution, monitoring, and approval*. The standard assumes
**progressive disclosure**: agents read `name` + `description` first, the
body on activation, and auxiliary files only when the procedure calls for
them — so long material belongs in `references/`, with `SKILL.md` stating
when to read it.

## Workflow first, agent second

The consistent vendor guidance (Anthropic *Building Effective Agents*, OpenAI
*A Practical Guide to Building AI Agents*): start with a simple, narrow
workflow, and introduce agency/skills/tools only where the workflow needs
them. Complex frameworks are a cost, not a starting point. OpenAI's Agents
SDK demonstrates that a small set of primitives — agent / tools / handoffs /
guardrails / tracing — covers most designs.

## Narrow skills beat many generic skills

SWE-Skills-Bench found that most of 49 generic skills produced no
improvement; gains concentrated in a few specialized skills. Prefer a small
number of skills fitted to your own development flow over bulk-importing
plausible-looking skill collections.

## Layering skills

A practical four-layer split that maps onto the standard folder form, OpenAI
handoffs/guardrails, and LangGraph subagents/memory:

| Layer | Unit | Examples |
|---|---|---|
| Domain skill | a job | bug fix, code review, release notes |
| Procedure skill | a shared flow | reproduce → diagnose → minimal fix → verify |
| Guard skill | a safety rule | secret detection, dangerous-command approval |
| Operations skill | upkeep | log capture, failure reporting, update notices |

Organizationally: L1 = org-wide, L2 = per discipline, L3 = per repo/team.
Avoid monolithic skills — the split is what survives model swaps and runtime
migrations. Keep skills as Git-managed text assets (prompt text, scripts,
templates, test sets) rather than configurations locked inside a vendor UI.

## Context engineering

For long or multi-step tasks, context management dominates quality. LangChain's
four operations: **write / select / compress / isolate**. Applied to a
software-development skill: don't hand over the whole repo — standardize
target-file selection, diff compression, test-result summarization, and
delegation of subtasks to isolated subagents *inside the skill's procedure*.

## Tool design within a skill

From Anthropic *Writing Tools for Agents*: tools deserve deliberate design of
naming, boundaries, meaningful return values, and token efficiency — and their
own evals. Distinguish server-side vs client-side execution responsibility
(Anthropic tool-use docs). When a skill drives external APIs, build in
authentication and rate-limit/retry behavior from the start.

## Theoretical grounding

ReAct (interleaved reasoning and acting) and Toolformer (models can learn
API selection, argument construction, and result integration) underpin the
current practice: skills externalize these behaviors as reusable workflow
modules instead of fixed prompts.

## Sources

Collected 2026-07; merged from two research reports.

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
- https://agentskills.io/specification
- https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- https://openai.github.io/openai-agents-python/
- https://developers.openai.com/api/docs/guides/prompt-guidance
- https://learn.microsoft.com/ja-jp/agent-framework/journey/adding-skills
- https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/
- https://www.langchain.com/blog/context-engineering-for-agents
- https://docs.github.com/ja/copilot/concepts/agents/about-agent-skills
- ReAct: https://arxiv.org/abs/2210.03629 / Toolformer: https://arxiv.org/abs/2302.04761
- SWE-Skills-Bench: https://arxiv.org/abs/2603.15401
