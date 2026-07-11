# Reference Catalog: Skill/Agent Repositories and Primary Docs

Curated external resources for skill authoring and agent design. Assessments
are as of collection (2026-07); re-check activity and licenses before
depending on anything here. Treat all third-party skills as supply chain —
review before installing (see
[security-and-operations.md](./security-and-operations.md)).

## Skill/agent packs worth mining

Ranked for this repository's purpose (spec-driven flow, role separation,
quality gates, review automation):

| Priority | Repository | Worth taking |
|---|---|---|
| Top | [github/spec-kit](https://github.com/github/spec-kit) | Spec → plan → tasks → implement flow (`/specify` `/plan` `/tasks` `/implement`); stack-agnostic skill design |
| Top | [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Role separation (PM / Architect / Developer / UX); PRD-to-test AI-driven agile flow; upstream-process skills |
| Top | [wshobson/agents](https://github.com/wshobson/agents) | Large multi-harness marketplace (skills/agents/commands/orchestrators); extract selectively |
| High | [zhsama/claude-sub-agent](https://github.com/zhsama/claude-sub-agent) | Spec-driven subagents with quality gates (orchestrator/analyst/architect/planner/developer/tester/reviewer) |
| High | [lst97/claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents) | Discipline-based subagents (backend-architect, code-reviewer, qa-expert, test-automator, debugger, security-auditor) |
| Mid | [davepoon/buildwithclaude](https://github.com/davepoon/claude-code-subagents-collection) | Discovery hub for skills/agents/commands/hooks/plugins |
| Mid | [ruvnet/claude-flow](https://github.com/ruvnet/claude-flow) | Heavy meta-harness (swarm, ADR, DDD, SPARC); reference in part only |
| Mid | [rahulvrane/awesome-claude-agents](https://github.com/rahulvrane/awesome-claude-agents) | Catalog of skillifiable themes (tech-debt finder, architecture reviewer, test generator) |
| Mid | [animesh303/awesome-cursor-skills](https://github.com/animesh303/awesome-cursor-skills) | Cursor-format templates; orchestrator/planner/implementer/verifier structure |
| Ref | AWS Kiro (specs/steering/hooks) | `requirements.md` / `design.md` / `tasks.md` decomposition philosophy |

Suggested intake order: Spec Kit → BMAD → zhsama → extract from
wshobson/agents. Focus first on five skills: specification, task breakdown,
implementation review, test strategy, change-risk review.

### Skill ideas derived from these

| Idea | Source pattern | Does |
|---|---|---|
| spec-to-tasks | Spec Kit / BMAD | Requirements → acceptance criteria → design → task breakdown → order |
| architecture-reviewer | lst97 / awesome-claude-agents | Boundaries, dependency direction, DB changes, responsibility, over-engineering |
| test-strategist | zhsama / lst97 | Derive needed unit/integration/e2e/regression tests from a diff |
| change-risk-reviewer | wshobson / BMAD | PR blast radius, rollback plan, migration risk, ops impact |
| tech-debt-finder | awesome-claude-agents | Duplication, god functions, mixed responsibilities, untestable design, stale deps |
| negative-guardrails | security incident reports | Explicit prohibitions: unrelated refactors, unknown scripts, production ops |

Caveat: SWE-Skills-Bench (https://arxiv.org/abs/2603.15401) found most
generic skills don't improve outcomes — build few, narrow, flow-fitted
skills rather than importing collections wholesale.

## Foundation / reference implementations

| Repository | Role | License | Note |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Canonical skill examples, skill-creator, spec/template | Apache-2.0 core, some source-available | Most direct reference for skill modularization |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Agent Skills standard itself | Apache-2.0 | Spec + `skills-ref/` starting point |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Engineering-process skills (spec→plan→implement→verify→review→ship) | MIT | Process-stage skill set |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | Agent runtime primitives: tools, handoffs, guardrails, tracing, sandbox | MIT | Execution-side standard parts |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Durable, stateful multi-agent orchestration | MIT | Strong but framework lock-in |
| [google/adk-python](https://github.com/google/adk-python) | Google agent kit incl. eval and deploy | Apache-2.0 | |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | Skills, workflows, observability (Python/C#) | MIT | |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | MCP reference servers (Filesystem/Git/Memory) | — | Teaching material for controlled tool exposure |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | Declarative evals / red team in CI | MIT | |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | Tracing, prompt mgmt, eval, cost visibility | — | |
| [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | Trace-level evaluation and monitoring | — | |
| [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | GitHub-issue-fixing agent; ACI research | MIT | Benchmark-driven improvement exemplar |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | Self-hosted coding agents, ops surface | MIT core, `enterprise/` separate | |
| [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) | Practical samples (autonomous coding, computer use, security reviewer) | MIT | |
| [openai/codex](https://github.com/openai/codex) | Production local coding agent (Rust) | Apache-2.0 | |

## Primary documentation reading list

**Design** — Anthropic *Building Effective Agents*
(https://www.anthropic.com/engineering/building-effective-agents), OpenAI
*Practical Guide to Building AI Agents*, Microsoft *Adding Skills*
(https://learn.microsoft.com/ja-jp/agent-framework/journey/adding-skills),
Agent Skills spec (https://agentskills.io/specification).

**Tooling** — Anthropic *Writing Tools for Agents*
(https://www.anthropic.com/engineering/writing-tools-for-agents), tool-use
overview (https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview),
OpenAI prompt guidance
(https://developers.openai.com/api/docs/guides/prompt-guidance).

**Evaluation** — Anthropic *Demystifying Evals for AI Agents*
(https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents),
LangSmith evaluation concepts
(https://docs.langchain.com/langsmith/evaluation-concepts), MS Foundry agent
evaluators, agentskills.io *Evaluating Skills*.

**Security/ops** — OWASP LLM Top 10
(https://owasp.org/www-project-top-10-for-llm-applications/), OpenAI
sandboxes, Google Agent Gateway, Microsoft governance
(https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization).

## Sources

Collected 2026-07-11 from three research notes (external-pack survey and two
agent-skill research reports). GitHub star counts and activity claims from
the originals were dropped as unverified snapshots.
