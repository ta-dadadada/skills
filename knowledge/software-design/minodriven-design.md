# MinoDriven's Software Design Philosophy

Systematization of the design philosophy of MinoDriven (ミノ駆動 / 仙塲大也),
author of 『良いコード/悪いコードで学ぶ設計入門』 (Gihyo, 2022; revised
edition 2024). Useful here as source material for design-review and
refactoring skills, and for the "give AI the design context" practice.

## Core thesis

The constant center is **changeability (変更容易性)** — structure code so
future changes are fast and safe. Since ~2023 the framing has expanded
upward and forward:

- **Purpose-driven**: a system is a means to an end, so structure should be
  organized by purpose (目的−目標−手段). Applies from requirements down to
  layer responsibilities and design-by-contract.
- **Business framing**: technical debt explained as slower delivery → higher
  cost → profit decay; changeability sold as speed and loss prevention.
- **AI-era repositioning**: AI is an amplifier — design skill is not
  replaced by AI, it is the precondition for using AI well. Give AI the
  purpose, quality attributes, context, and contracts.

## Principles

| Principle | Definition | Typical anti-pattern |
|---|---|---|
| Changeability first | Aim for structures that absorb future change quickly and correctly | "Works but hard to modify" |
| Structure by purpose | Modules exist as means to a purpose | Cutting models/layers by data items or UI |
| Separation of concerns | Split by use case / purpose / role | God classes, monolithic models |
| Single responsibility | One responsibility = keeping one concern operating correctly (not "few functions") | Same method growing with every spec change |
| Role-driven design | One model doesn't play multiple roles | "User"/"Product" absorbing all duties |
| Constraints inside the model | Reject invalid values/states within the model | DTO with bare values, validation deferred downstream |
| Immutability by default | Values immutable; expose only permitted operations | Setter-riddled mutable objects |
| DRY applies to concepts | Deduplicate knowledge, not code shape | Forced unification of merely similar-looking code |
| Interface/implementation separation | Push selection responsibility to Factory/DI; keep call sites simple | Callers switching on implementation via if/switch |
| Words carry context | Terms defined with actor, purpose, context, rules — a ubiquitous language is not a mere glossary | Glossary that flattens meaning differences |
| Design by contract | Pre/post-conditions and invariants make correctness explicit | Expectations left verbal/implicit |
| Replace safely | Isolate legacy via anti-corruption layer; migrate via Strangler Fig | Big-bang rewrite of complex legacy |
| AI amplifies design skill | AI needs purpose, contracts, quality attributes, context as input | Delegating to AI with no context |

Key building blocks: **ValueObject + complete constructor + immutability**
(reject invalid values at construction; expose only allowed operations);
**update models must carry constraints** ("データ破壊駆動" — a box with data
and no invariants is not a model); **model by invisible purposes and
constraints, not visible physical attributes** ("Invisible Driven Design").

## Practical workflow

1. **Clarify purpose** — whose purpose, achieving what; dig into actor,
   context, and rules; (re)build the ubiquitous language. A bounded context
   is a coarse-grained purpose.
2. **Split models, design constraints** — divide god classes by role/
   concern/purpose; give every update model invariants (ValueObject,
   complete constructor, immutability, permitted operations only).
3. **Isolate branching and external deps** — interface/implementation
   separation with Factory/DI; for legacy, anti-corruption layer ("ふたつの
   橋作戦", READYFOR) or Strangler Fig migration to clean modules (his
   recommended AI-era refactoring route, with Event Storming for domain
   discovery).
4. **Align with the business** — explain debt as profit decay; use everyday
   metaphors (storage/収納) for non-engineers.
5. **Feed AI the design** — purpose, design-by-contract conditions, quality
   attributes, context. He reports embedding "design by contract" and
   "interface/implementation separation" into his own agent skills.

## Review checklist

- Requirements: actor / purpose / context / rules written down?
- Terms: same word, different meaning across contexts? Glossary carries
  context + rules?
- Models: roles/concerns/purposes mixed in one class?
- Constraints: invalid values rejected at construction? Invariants present?
- Interfaces: call sites free of implementation-selection branching?
- Architecture: can each layer's purpose be stated in one sentence?
- Tests: pre/post-conditions and invariants verified?
- Refactoring: goal structure defined up front? Staged migration path?
- Alignment: debt explainable in speed/cost/profit terms?
- AI use: purpose, quality attributes, context, contracts provided?

## Sources

Primary sources concentrate in Qiita, note, X (`@MinoDriven`), Speaker Deck,
the books, and READYFOR Tech Blog. No confirmed Zenn account; GitHub profile
exists but no public repos (official sample code is distributed by the
publisher). Collected 2026-07.

**Books**: revised ed. https://gihyo.jp/book/2025/978-4-297-14622-1 (samples:
…/support), 1st ed. https://gihyo.jp/book/2022/978-4-297-12783-1

**Foundational Qiita** (principles layer):
- Role-driven design: https://qiita.com/MinoDriven/items/2a378a09638e234d8614
- ValueObject + complete constructor: https://qiita.com/MinoDriven/items/5e69d9bd028aa350e2c4
- Separation of concerns & naming: https://qiita.com/MinoDriven/items/37599172b2cd27c38a33
- Single responsibility: https://qiita.com/MinoDriven/items/76307b1b066467cbfd6a
- Cognitive bias in design decisions: https://qiita.com/MinoDriven/items/8e4abda43b05cd7a0200
- Refactoring self-destruct patterns: https://qiita.com/MinoDriven/items/dac5505cf8442e1721d1
- Explaining debt to non-engineers: https://qiita.com/MinoDriven/items/2d63dcaa92b50b049889

**Speaker Deck** (recent synthesis; 2023→2026 traces the purpose-driven arc):
- Purpose–abstraction design (2023): https://speakerdeck.com/minodriven/purpose-abstraction-design
- Invisible Driven Design (2024): https://speakerdeck.com/minodriven/invisible-driven-design
- データ破壊駆動 (2024): https://speakerdeck.com/minodriven/data-destroy-driven
- Purpose-driven architecture (2026): https://speakerdeck.com/minodriven/purpose-driven-architecture
- 前提を疑う認知の視点 (2026): https://speakerdeck.com/minodriven/doubt-premise
- AI refactoring approach (2026): https://speakerdeck.com/minodriven/ai-refactoring-approach
- AI and software quality (2026): https://speakerdeck.com/minodriven/ai-and-software-quality
- Modifius, changeability MCP server (2026): https://speakerdeck.com/minodriven/modifius

**Practice articles**: anti-corruption layer at READYFOR:
https://tech.readyfor.jp/entry/2022/04/11/114603 ; design as team building:
https://tech.readyfor.jp/entry/2022/09/05/170057 ; interface talk (Forkwell):
https://pr.forkwell.com/tech_event_reports/engineer-culturefes-2023-minodriven/

Note: https://github.com/tsujike/minodriven-goodcodebadcode is **unofficial**
— the official samples come from the publisher's support page.
