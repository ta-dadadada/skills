---
name: backend-api-implementation
description: >-
  Contract-first workflow for implementing a backend API endpoint in an
  existing project: discover the project's conventions, fix the input/output
  contract (schemas, error shapes, status/error codes), write tests against
  the contract, implement, verify with a real request. Tech-agnostic — REST,
  GraphQL, and gRPC alike. Use when adding a new endpoint or operation to an
  existing backend, or when changing an existing endpoint's request/response
  shape, error handling, or behaviour. Not for designing a new API or
  service from scratch.
license: MIT
metadata:
  author: ta-dadadada
---

# Backend API Implementation

The contract — input and output schemas, error shapes, status/error codes — is fixed before any test or implementation exists, and every later step answers to it. The project's existing conventions are the default for how the contract is expressed and how the code is written; a deviation is justified only where the convention would reproduce a known correctness, security, or changeability problem, and it stays as small as its reason. The endpoint is done when a real request, not only the test suite, returns the contracted response.

## When to use

- Adding a new endpoint or operation to an existing backend (REST, GraphQL, gRPC, or whatever the project already speaks).
- Changing an existing endpoint: request/response shape, error handling, status/error codes, or behaviour.

## When not to use

- Designing a new API or service from scratch — resource model, protocol choice, and versioning strategy are settled before this skill applies.
- Refactors that leave the contract untouched — there is no contract to fix.
- Client-side or frontend-only changes.

## Workflow

### Step 1 — Discover the project's conventions

- Locate how existing endpoints are defined: routing/registration, handler layout, and any contract artifacts already in the repo (schema files, IDL, generated types, API docs).
- Read one or two existing endpoints closest in shape to yours, end to end: handler → validation → business logic → response serialization.
- Record from that reading the project's way of doing input validation, error shapes, authn/authz wiring, and tests (where they live, how they call endpoints, what they assert). Flag any pattern you will deliberately keep out of the new code — one carrying a known correctness, security, or changeability problem — with its reason.
- Locate how the service runs locally and how a real request reaches it (dev-server command, container setup, test client) — Step 5 depends on it.

**Done when:** you can name, with file paths, the project's pattern for routing, validation, error shape, auth, and tests — and the command that starts the service.

### Step 2 — Fix the contract

- Open with one line naming the actor and the purpose: who calls this endpoint, to achieve what. Pin any ambiguous domain word to the meaning the project already uses.
- Write the contract in the form the project already uses (schema file, IDL, type definitions; a spec block in your task notes if the project keeps none), covering three conditions: preconditions (which inputs are accepted, which rejected), postconditions (the success response and every error case, each with concrete shape and status/error code), and invariants (what stays true about stored data after any call, including failed or retried ones).
- Give every row of the review table a verdict: addressed in the contract, or not applicable with a reason.
- For a change to an existing endpoint: inventory the consumers visible in the repo and its docs (client code, other services, tests, generated clients), and record any population you cannot verify — external callers, other repositories — as unknown. State per known consumer whether the change is compatible; an incompatible change, or a breaking change with an unknown population, gets an explicit migration decision before you proceed.
- Freeze the contract: tests and implementation follow it from here, and a contract edit later means re-entering this step first.

| Concern | Question the contract must answer |
|---|---|
| Validation | which inputs are rejected, with what error shape and code? |
| AuthN/AuthZ | who may call this, and what does an unauthorized call get? |
| Error handling | is every failure path mapped to a documented shape and code? |
| Idempotency | what does a retried or duplicate call do? |
| Invariants | what must stay true about stored data, even when the call fails? |
| Side effects / atomicity | what state changes, which changes succeed or fail together, what remains after a partial failure — and how are side effects on external systems handled? |
| Concurrency | what happens when conflicting calls execute concurrently — which wins, and what state results? |
| Ownership | which component is each rule's authoritative owner — transport checks at the protocol boundary, each domain invariant defined at one owner every known write path crosses? Boundary pre-checks and DB constraints are defense-in-depth echoing the owner, never a second definition of the rule. |
| Pagination / limits | are unbounded collections capped, paged, or both? |
| Compatibility | does every existing consumer keep working, or is a migration decided? |
| Observability | how is a failing call diagnosed, matching project practice? |

**Done when:** actor and purpose are stated; preconditions, postconditions, and invariants are written with concrete shapes and codes; every table row has a verdict; and consumer compatibility is stated (or the endpoint is new).

### Step 3 — Write the tests

- Write tests in the project's test pattern from Step 1, one per contract case: each success shape, each error shape/code, and each invariant (a failed or duplicate call leaves stored data consistent).
- Place each test at the cheapest level in the project's suite that catches its failure: domain-rule cases where the rule lives, shape/status/serialization cases at the transport layer, storage constraints against real persistence — routing and middleware are what Step 5's real request covers.
- For a changed endpoint, pin the behaviour that must survive: each compatible consumer expectation from Step 2 gets its own test.
- Run the new tests and confirm each fails because the behaviour is absent — a failure in the harness or fixtures means fixing the test first.

**Done when:** every contract case from Step 2 maps to a named test, and each new test fails because the behaviour does not exist yet.

### Step 4 — Implement

- Implement following the Step 1 record — the same layering, validation mechanism, error helpers, and naming as the neighbouring endpoints; where a neighbour's pattern was flagged in Step 1, deviate minimally and record why.
- Put each rule where the Step 2 ownership verdict placed it: transport checks at the boundary, each domain invariant with its authoritative owner; boundary pre-checks and DB constraints stay echoes of that owner, not second definitions.
- Enforce a state-transition precondition as a single conditional write at the persistence owner — a guarded `UPDATE ... WHERE <state predicate>` or a DB constraint that succeeds or refuses atomically — so concurrent calls cannot both pass. A read-then-write check in application code leaves a race window; keep it only as a fallback when the toolchain to add the guarded write is unavailable, and record that it is one.
- Keep the contract and the internal design distinct: the contract's request/response/operation types are not automatically the internal units of abstraction. When the same kind/provider/policy branch is being added across several endpoints, or a new operation keeps forcing edits to stable routing, use-case flow, or serialization code, apply `purpose-driven-software-design` for the axis-of-change decision — and a single endpoint never justifies a generic framework, plugin mechanism, or factory hierarchy.
- Work until the Step 3 tests pass; when implementation reveals a contract gap, re-enter Step 2 and update contract and tests before the code.
- Run the project's full relevant test suite and its configured linters/type checks, beyond the new tests alone.

**Done when:** all Step 3 tests pass, the surrounding suite and configured checks pass, the new code reads like the neighbouring endpoints, each rule sits with its Step 2 owner, and any deliberate deviation is recorded with its reason.

### Step 5 — Verify with a real request

- Start the service the way the project runs it (Step 1) and send real requests with a protocol-appropriate client (curl, grpcurl, a GraphQL client): at least one success case and one contracted error case.
- Compare each real response against the Step 2 contract field by field — body shape, status/error code, headers where contracted.
- For a changed endpoint, replay a representative existing-consumer call and confirm it still succeeds.
- Confirm the failing call is diagnosable the way the Step 2 observability verdict promised: the project's log/trace conventions fire with enough context to locate the fault, and sensitive data stays out of the output.

**Done when:** real responses match the contract for a success case and an error case, the error case is diagnosable per the Step 2 observability verdict, and, for a change, an existing-consumer call still succeeds.

## Red flags

| Rationalization | Reality |
|---|---|
| "The framework makes the contract obvious" | implicit contracts drift; write the contract down before tests |
| "Tests after implementation is faster" | tests written after mirror the code, not the contract |
| "The tests pass, so it works" | only a real request exercises routing, serialization, and middleware end to end |
| "Standard best practice says…" | the project's conventions are the default; a deviation needs a Step 1-flagged problem, not taste |
| "The neighbouring endpoint already does it this way" | convention is the default, not proof of sound design — patterns flagged in Step 1 stay out of the new code |
| "The handler already validates it" | a domain invariant whose only owner is one transport boundary vanishes when another path writes the same data |
| "The API types are the domain model" | the contract fixes the surface; internal abstraction follows the axes of change, not the operation list |
| "Every endpoint gets the same switch" | a branch repeated across endpoints per new kind is an axis of change already showing — separate it, don't replicate it |
| "Error cases can be a follow-up" | error shapes are contract; consumers code against them from day one |
| "Nobody calls this endpoint yet" | tests, docs, and generated clients are consumers too — inventory before changing |
| "The repo search found no consumers" | callers outside the repo exist; record them as unknown rather than compatible |

## Related

- `purpose-driven-software-design` — the general design workflow behind this one: where rules and logic live, authoritative owners, evidenced axes of change, abstraction sizing, test-level choice. Reach for it when the design question outgrows the contract; the ownership and convention principles embedded in the steps above stand alone when it is unavailable.
