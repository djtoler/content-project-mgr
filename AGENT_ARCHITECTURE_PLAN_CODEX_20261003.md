# Provider-neutral content-agent architecture — Codex proposal

**Date:** 2026-10-03  
**Author:** Matching / Codex  
**Status:** proposal for review and reconciliation with Claude; not implementation authorization

## Objective

Build one coordinated content-production agent system whose domain agents can be run through different providers and model versions without changing domain rules, artifact contracts or completion criteria.

`content-project-mgr` is the coordinator boundary. It dispatches work, validates receipts, reports the current blocker, and preserves the end-to-end task graph. It does not make Story, Data, Matching or Media decisions for those layers.

The first implementation should use installed local CLIs. The design must keep CLI, SDK and API transports replaceable behind the same runner interface. No external model API call is authorized by this proposal.

## Repository and authority map

| Repository | Agent/layer | Owns | Must not own |
|---|---|---|---|
| `djtoler/content-project-mgr` | Coordinator | objectives, task graph, dispatch, dependency state, receipt validation, retries, human gates, global run summary | story meaning, facts, template choice, media identity |
| `djtoler/patterns` | Story | StoryPackage, exact narration/claim spans, meaning, obligations, continuity and Story-owned provenance | template selection, entity minting, media publication |
| `djtoler/Polish` → `hiphop-research-engine` | Data | research, evidence, claim/value support, stable entity publication requests and data receipts | story prose, template choice, media identity approval |
| `djtoler/astra-visual-selector` | Matching | semantic VisualTasks, route disposition, capability admission, candidate ordering, template/media pairing and sequence planning | facts, Story authority, asset publication, rendering authorization |
| `djtoler/media_layer` | Media | sourcing, ingest, identity/quality evidence, processing, lifecycle state and Production Ready receipts | story meaning, template selection, claim truth |
| `djtoler/entity_roster` | Data-owned shared registry | canonical stable IDs, reviewed aliases, evidence and immutable publication receipts | independent reasoning or local agent decisions |

`channel-analyzer` and the earlier `automation-data` repository are upstream intelligence/data sources. They may produce typed inputs for Data or the coordinator, but they should not become additional authorities that bypass the Data contract.

## Core design

```text
                         content-project-mgr
                              Coordinator
                                  |
                 task contracts / receipts / gates
          +-----------+-----------+-----------+-----------+
          |           |           |           |           |
        Story        Data       Matching      Media      Human
       patterns     Polish       astra      media_layer   gates
          |           |           |           |
          +-----------+-----------+-----------+
                 versioned shared artifacts
```

The coordinator operates on artifacts and receipts rather than conversational memory. A provider chat may help produce an artifact, but chat history is never the authority for completion.

## Provider-neutral runner

Every provider/transport adapter implements the same logical interface:

```text
run(task_contract, workspace, agent_profile) -> run_handle
status(run_handle) -> run_state
steer(run_handle, message) -> acknowledgement
cancel(run_handle) -> cancellation_receipt
collect(run_handle) -> agent_receipt
```

Initial adapters:

1. `CodexCliRunner`
2. `ClaudeCliRunner`
3. `GeminiCliRunner` when the local workflow is available

Later adapters may include Codex SDK/app-server, Anthropic SDK/API or Gemini API. Transport adapters may translate invocation details, but they may not change the task contract, validation rules or receipt meaning.

## Configuration

Agent definitions are versioned YAML. Environment variables provide secrets, machine-specific paths, endpoints and explicitly supported runtime overrides. Secrets never appear in YAML, logs or receipts.

Proposed shape:

```yaml
schema_version: content-agent-profile@1
agent_id: matching
contract_version: general-matching-agent@1
active_profile: ${MATCHING_PROFILE:-openai_astra}

profiles:
  openai_astra:
    provider: openai
    model: ${MATCHING_OPENAI_MODEL:-gpt-6-astra}
    transport: ${MATCHING_OPENAI_TRANSPORT:-cli}
    reasoning_effort: ${MATCHING_OPENAI_EFFORT:-xhigh}
    prompt_version: matching-agent-prompt@1
    tool_policy: matching-tools@1
    evaluation_profile: matching-cross-story@1

  claude_opus:
    provider: anthropic
    model: ${MATCHING_ANTHROPIC_MODEL:-claude-opus-5-5}
    transport: ${MATCHING_ANTHROPIC_TRANSPORT:-cli}
    reasoning_effort: ${MATCHING_ANTHROPIC_EFFORT:-high}
    prompt_version: matching-agent-prompt@1
    tool_policy: matching-tools@1
    evaluation_profile: matching-cross-story@1
```

Required configuration fields:

- agent ID and ownership scope;
- provider, exact model and transport;
- reasoning/effort setting;
- prompt and policy versions;
- input/output contract versions;
- tool allow-list and workspace permissions;
- evaluation profile;
- timeout, retry and escalation policy;
- supported environment overrides.

Unknown fields or unresolved environment variables fail closed. Configuration resolution emits a redacted hash-bound receipt.

## Contracts and receipts

### Task contract

Every dispatched task contains at least:

- `taskId`, `objectiveId`, `owner`, `requestedBy`;
- exact input artifact paths, repository commits and hashes;
- expected output schema and destination;
- dependencies and their receipt IDs;
- policy/prompt/config versions;
- allowed tools and mutation scope;
- acceptance checks;
- whether user input or authorization is required;
- deadline/timeout and retry class.

### Agent receipt

Every agent run returns:

- resolved provider/model/transport profile, with no secrets;
- exact input hashes and repository state;
- output artifact paths and hashes;
- commands/checks executed and their outcomes;
- contract and policy versions enforced;
- completion status: `passed`, `failed`, `blocked` or `needs_review`;
- current blocker: `you`, `data`, `story`, `matching`, `media`, `coordinator` or `none`;
- concrete missing input/action when blocked;
- warnings, unresolved gaps and invalidated downstream receipts.

A prose claim that work is complete is not a completion receipt.

## Coordinator algorithm

1. Load the objective, task graph and exact repository heads.
2. Validate every task contract and dependency receipt before dispatch.
3. Choose a ready task by dependency order and declared priority, never merely by the most recent chat message.
4. Resolve the configured provider profile and isolated workspace/worktree.
5. Dispatch through the selected runner.
6. Validate the returned receipt and independently run mandatory acceptance checks.
7. Mark the task complete only when its saved acceptance receipt passes.
8. Invalidate downstream receipts when a bound input changes.
9. Continue to the next ready task while the objective is incomplete.
10. Stop only for objective completion or a concrete human/external dependency.

The coordinator reports exactly one current blocker on every status response. Ready independent work takes precedence over an unrelated human-review wait.

## State model

Keep four distinct state classes:

1. **Context state:** temporary model working context; disposable.
2. **Run state:** task/run ID, current step, tool events and pending action.
3. **Durable project state:** contracts, artifacts, receipts, decisions and repository commits.
4. **Canonical shared state:** entity registry and other explicitly owned cross-layer authorities.

Context compaction or a new chat must not alter durable task status. A resumed agent reconstructs state from the objective, task graph, receipts and repository hashes.

## Isolation and concurrency

- One isolated worktree per mutating run.
- A single declared writer per repository/path scope.
- Parallel execution only for tasks with satisfied dependencies and non-overlapping mutation scopes.
- The coordinator never resolves merge conflicts by guessing domain intent.
- Cross-repository changes use a transaction manifest listing every commit and required merge order.
- A partially completed multi-repository transaction remains visibly incomplete and cannot satisfy downstream gates.

## Human gates

Explicit human authorization remains required for:

- material editorial choices;
- disputed facts or identities;
- provider spend beyond an approved budget;
- external publishing or messaging;
- custom visual construction when existing-template policy requires approval;
- destructive or difficult-to-recover actions;
- final production release.

Human review is recorded as a scoped decision artifact. It is never inferred from silence or from an unrelated earlier approval.

## Provider profiles: starting hypotheses

These are initial evaluation targets, not permanent assignments:

| Agent | Primary starting profile | Alternate/challenger |
|---|---|---|
| Coordinator | OpenAI GPT-6 Astra | Claude Fable/Opus |
| Story | Claude Opus 5.5 | OpenAI GPT-6 Astra |
| Data | OpenAI GPT-6.1 Sol; Astra escalation | Claude Opus 5.5 |
| Matching | OpenAI GPT-6 Astra | Claude Opus 5.5 |
| Media semantic analysis | Gemini multimodal profile | OpenAI/Claude vision profile |
| High-volume roster suggestions | lowest-cost passing profile | deterministic-only fallback |

No model is an authority. Each profile must pass the same layer-specific evaluation suite. The lightest passing model becomes the normal profile; difficult cases may escalate according to saved policy.

## Evaluation plan

### Common evaluation dimensions

- contract compliance;
- correct abstention and blocker ownership;
- artifact/receipt completeness;
- unsupported assertion rate;
- tool-use correctness;
- recovery after context reset;
- deterministic validation pass rate;
- latency and cost per accepted artifact;
- human correction time.

### Layer-specific frozen fixtures

- **Story:** multiple StoryPackages with span, entity, obligation, continuity and provenance checks.
- **Data:** supported/contradicted claims, source receipts, entity collisions, missing-data and comparability traps.
- **Matching:** at least two regression packages plus one untouched StoryPackage, with complete narration routing, no prior-story leakage and no selection/render authorization.
- **Media:** identity/quality positives and negatives, lifecycle transitions, provenance, missing assets and multimodal scene-description checks.
- **Coordinator:** dependency races, stale receipts, conflicting heads, user-review waits, partial multi-repo transactions and provider failure/retry cases.

Provider comparisons use identical frozen inputs and schemas. Do not tune one provider on the held-out evaluation while leaving another untouched.

## Delivery phases

### Phase 0 — reconcile architecture

- Review this proposal with Claude.
- Resolve ownership, runner/config boundary, receipt schema and coordinator stop rules.
- Publish one reconciled architecture decision record.

### Phase 1 — contracts only

- Define JSON Schemas for agent profile, task contract, run state and agent receipt.
- Define the YAML schema and allow-listed environment interpolation.
- Add validators and mutation tests.
- Do not invoke a model yet.

### Phase 2 — one vertical slice

- Implement the coordinator plus one Matching task using the existing local CLI.
- Run in an isolated worktree.
- Require existing matching contract gates and cross-story tests.
- Prove context-reset recovery from durable state.

### Phase 3 — provider variant

- Add a second Matching runner/profile without changing domain code or fixtures.
- Compare receipts, correctness, cost, latency and human correction time.
- Fix abstraction leaks before adding more agents.

### Phase 4 — remaining agents

- Add Story, Data and Media profiles one at a time.
- Validate every inter-layer handoff before permitting concurrent execution.

### Phase 5 — production hardening

- budgets, rate limits and cancellation;
- tracing and redaction;
- recovery and idempotency;
- transaction manifests;
- scheduled monitoring;
- operator UI and audit history.

## Non-goals for the first build

- No autonomous publishing or rendering.
- No new entity authority.
- No provider-specific business rules.
- No requirement that every beat use a template.
- No attempt to merge every existing repository into one monorepo.
- No API-first implementation when local CLI execution is sufficient.
- No claim that the first provider assignment is proven without evaluations.

## Request to Claude

Please publish your independent plan as `AGENT_ARCHITECTURE_PLAN_CLAUDE_20261003.md` in this repository. Address these points directly:

1. Which boundaries above should change, and why?
2. Is `content-project-mgr` the right coordinator boundary?
3. Are YAML profiles plus environment overrides sufficient, or is another configuration layer needed?
4. Where should durable task/run state live?
5. What is the smallest provider-neutral runner interface that supports both Claude Code and Codex CLI without hiding important differences?
6. Which receipt fields are missing?
7. How should concurrent cross-repository writes and stale receipts be handled?
8. Which provider assignments should differ from the starting hypotheses?
9. What vertical slice would falsify this architecture fastest?
10. Identify any part of this proposal that would recreate the drift, false-completion or story-specific coupling seen in earlier work.

After Claude's plan lands, Codex will write a source-bound reconciliation response. Agreement between agents will remain a proposal until the user accepts the final architecture.
