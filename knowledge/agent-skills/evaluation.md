# Evaluating Agents and Skills

Final-answer scoring alone is insufficient for agents: multi-step,
multi-tool behavior has to be evaluated along the path, not just at the end
(Anthropic *Demystifying Evals for AI Agents*). Design skill-level quality
assurance on three axes: **output quality × trajectory × tool-use validity**.

## Three evaluation layers

LangSmith's decomposition, with Microsoft Foundry's concrete metrics filling
each layer:

| Layer | What it judges | Example metrics (MS Foundry) |
|---|---|---|
| Final response | is the end result correct/complete | task completion |
| Trajectory | was the path sensible | task adherence, intent resolution |
| Single step | was each tool call right | tool call accuracy, tool input accuracy, tool output utilization, tool call success |

## Offline vs online

Run both, separately:

- **Offline** — regression sets with expected outputs, compared on each
  change. Skills can carry their own eval data: the Agent Skills standard
  supports `evals/evals.json` with per-skill test cases and expectations.
- **Online** — scoring production traces for quality, safety, and behavior
  drift. OpenAI's guidance: understand behavior via traces first, then enter
  the eval loop. Trace-level evaluation (e.g. Arize Phoenix) covers tool
  selection, ordering, and intermediate judgments.

Promptfoo-style declarative evals and red-teaming are designed to run in
CI/CD — treat skill changes like code changes.

## Minimum acceptance set for a skill

1. **Regression cases** — realistic issues/change requests with expected
   outcomes.
2. **Trajectory tests** — assert the expected tool-call order.
3. **Automated verification** — tests, lint, type check, build.
4. **Continuous scoring** — against production traces after release.

## Lessons from coding-agent benchmarks

SWE-bench (real GitHub issues: long context, execution environment,
multi-file, test runs) and the SWE-agent paper show performance differences
come not only from model capability but from **Agent-Computer Interface
(ACI) design** — the file-edit/search/test-execution interface itself. So
skill verification must include the interfaces the skill drives, not just
its prompt text.

## Platform caveat

OpenAI's Evals platform and Agent Builder were deprecated 2026-06-03 with
end-of-life 2026-11-30 — don't build new eval pipelines on them; prefer
traces + external eval infrastructure + Git-managed skill assets.

## Sources

Collected 2026-07; merged from two research reports.

- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://docs.langchain.com/langsmith/evaluate-complex-agent
- https://docs.langchain.com/langsmith/evaluation-concepts
- https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators
- https://learn.microsoft.com/en-us/agent-framework/agents/evaluation
- https://developers.openai.com/cookbook/examples/agents_sdk/evaluate_agents
- https://developers.openai.com/api/docs/guides/evaluation-best-practices
- https://developers.openai.com/api/docs/deprecations
- https://agentskills.io/skill-creation/evaluating-skills
- https://arize.com/docs/phoenix/cookbook/evaluation/trace-level-evaluation
- https://www.promptfoo.dev/docs/red-team/
- SWE-bench: https://arxiv.org/abs/2310.06770 / SWE-agent: https://arxiv.org/abs/2405.15793
