# Skill Security and Operations

The largest gap between a PoC and production skill usage is operational:
execution logs, permissions, auditability of failures, and controlled
distribution — not the skill text itself.

## Isolation for side effects

Skills that read, write, or execute code should run isolated and monitored
by default. OpenAI separates the harness from sandbox compute: the skill
makes *judgments*, the sandbox absorbs *side effects*. Principle: never run
a side-effectful skill outside a sandbox/worktree boundary.

## Permissions and audit

Manage *what a skill may call, with which permissions* in the same lifecycle
as the skill text. Reference points:

- Google Cloud Agent Gateway: IAM allow/deny policies, IAP end-to-end
  auth, Cloud Logging / Cloud Trace, security findings — agent-to-agent
  traffic is also a control target.
- Microsoft Foundry: Application Insights + continuous evaluation; token,
  latency, error, quality, and trace on one operations dashboard.
- Observability should assume OpenTelemetry-style trace/log/metric.
- OWASP Top 10 for LLM Applications gives the shared vocabulary for attack
  surface review (prompt injection, data disclosure, privilege abuse).

## Data-retention caveat (Anthropic)

Anthropic Agent Skills are **not covered by Zero Data Retention**; skill
definitions and execution data follow normal retention policy. Therefore:
keep skills Git-managed in your own repo, never embed secrets or sensitive
internal design directly — resolve secrets at runtime via external secret
management.

## Third-party skills are supply chain

Treat external skills/agents/hooks/commands like dependencies. Before
installing, review: `SKILL.md` body, hooks, install scripts, shell commands,
symlinks, and external network calls. Reported attack vectors include
symlink abuse in coding agents, Markdown-based instruction injection, and
typosquatted package/repository names. Put static checks in the
distribution pipeline.

### Per-skill checklist

- No instructions that read out secrets
- No unconditional `curl | sh`
- External destinations fixed and explicit
- Confirmation before write operations; destructive ops (`rm -rf`) restricted
- `allowed-tools` not overly broad
- External skills reviewed before install

## Reliability of skill output

For hallucination control, the two levers in Anthropic's guidance: allow
expressed uncertainty, and ground claims with citations/verification steps
built into the procedure.

## Cost

- Cache reusable preambles (prompt caching); manage context explicitly in
  long sessions (context-window docs).
- Track token/cost/latency/score together (e.g. Langfuse) to optimize per
  feature and per user.

## Sources

Collected 2026-07; merged from two research reports.

- https://developers.openai.com/api/docs/guides/agents/sandboxes
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/iam-overview
- https://learn.microsoft.com/en-us/azure/foundry/concepts/observability
- https://learn.microsoft.com/en-us/agent-framework/workflows/observability
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- https://owasp.org/www-project-top-10-for-llm-applications/
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview (ZDR note)
- https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- https://langfuse.com/docs/observability/features/token-and-cost-tracking
- Attack reports: https://www.itpro.com/security/flaws-in-some-of-the-most-popular-ai-coding-tools-left-developers-wide-open-to-attack
