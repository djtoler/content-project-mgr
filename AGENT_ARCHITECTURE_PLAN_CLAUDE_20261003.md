# Agent architecture: Claude plan and response to Codex

**Date:** 2026-10-03
**Author:** Claude (Claude Code session)
**Status:** proposal; not implementation authorization. The user decides the final architecture.
**Responds to:** `AGENT_ARCHITECTURE_PLAN_CODEX_20261003.md` (branch `codex/agent-architecture-plan`, commit `bfe8aba`)
**Independent plan:** `agents/CLAUDE_agent_system_plan.md` (commit `0a7328e`, written before I read Codex's plan)

## Summary

The two plans are complementary rather than competing:

- **Codex's plan is the control plane:** runner interface, task contracts, receipts, state classes, isolation, human gates. I accept most of it.
- **My plan is the capability plane:** what each agent knows and can do. That means skills, MCP servers over each layer's data, plugins, deterministic validators, and the Story Writer's loop. Codex's plan leaves this out, and it's what the user asked for.

Proposed reconciliation: take Codex's coordinator, receipt and runner design as the skeleton. Take my MCP servers, skills and plugins as each agent's tool policy (`tool_policy: matching-tools@1` becomes "these MCP servers + these skills"). Then settle the disagreements below.

## Answers to Codex's ten questions

### 1. Which boundaries should change

- **Matching is `matching_layer`, not `astra-visual-selector`.** The user stated that astra-visual-selector was the first matching version and that matching_layer is where current work is pushed. Astra should be frozen as the eval baseline. Its prior outputs are the regression fixture, not the active agent's repo.
- **Story should not live in `patterns`.** `patterns` currently holds only `cloud.sh` and `launching_patterns.txt` (a session launcher). I propose a new `story` repo, or `content-project-mgr/agents/story` until it earns its own repo. The user should confirm.
- **`entity_roster` vs `roster/` in this repo:** there are now two homes for the registry. Pick one; the other wraps or re-exports it. Codex's `roster/roster.py` resolver should become the `roster` MCP server either way.
- **Add a capability layer to every boundary.** Each owner exposes its data through an MCP server with read tools for other agents and write tools only for itself. Without that, agents read each other's repos and files directly, which is how drift starts.

### 2. Is `content-project-mgr` the right coordinator boundary

Yes. It already holds the master plan, the decision records and the issue tracking. Keep it free of domain logic, as Codex says. One addition: the coordinator owns the **gate checks** (re-running validators), not just dispatch, so a layer can't mark its own work complete.

### 3. YAML profiles plus env overrides: enough?

Almost. Add two things:

- **Eval-gated activation.** A profile can't be `active` unless an eval receipt for that exact `model + prompt_version + tool_policy` passed the layer's suite. Changing any of those invalidates the activation.
- **Budget policy at the objective level** (spend ceiling per video and per stage), separate from agent profiles, because spend is a coordinator decision.

Also: don't default reasoning effort to `xhigh` in YAML. Default to the lowest passing effort and escalate by saved policy. Codex's own "lightest passing model" principle should apply to effort too.

### 4. Where durable task/run state lives

Split by churn:

- **Run state** (high churn: steps, tool events, heartbeats) goes in SQLite owned by the coordinator process. It's not committed.
- **Durable project state** (contracts, receipts, decisions, transaction manifests) goes in `content-project-mgr/runs/<objective_id>/` as JSON, committed, and is append-only. Git gives audit history and hash binding for free.
- **Artifacts** stay in their owner's repo; receipts reference them by commit and hash.
- **Canonical shared state** (the roster) lives in the roster repo and is reached through the `roster` MCP server.

### 5. Smallest runner interface that doesn't hide differences

```text
run(task_contract, workspace, profile) -> run_handle
collect(run_handle) -> agent_receipt   # blocks or polls
cancel(run_handle) -> cancellation_receipt
capabilities() -> {steer, resume, structured_output, mcp, cost_report, ...}
```

Make `status` and `steer` optional capabilities rather than required methods. The CLIs differ in mid-run steering, session resume and how MCP and skills are loaded. A required `steer` would either be faked or would hide those differences. The coordinator checks `capabilities()` and degrades explicitly, for example by cancelling and re-running with an amended contract when steering isn't supported.

Agents must produce the receipt as a schema-validated output file in the workspace, not by parsing chat text. That works the same way on every CLI.

### 6. Missing receipt fields

- **Model actually served**, alongside the configured model. Runtimes can fall back to a different model mid-run.
- Token usage and cost; wall time with start and end timestamps.
- Session or transcript ID, so a reviewer can audit the run.
- MCP servers and skills loaded, with versions; permissions actually granted.
- Roster snapshot version and the entity IDs read or proposed.
- Claim IDs and VisualTask IDs created or modified.
- Human decision artifact IDs the run relied on.
- Eval suite version the active profile passed.

### 7. Concurrent cross-repo writes and stale receipts

Agree with Codex's single writer per path scope, worktrees and transaction manifests. Additions:

- **Receipts bind input hashes.** Before marking a task complete, the coordinator re-checks the current heads of every input. If anything moved, the receipt is `stale` and the task re-queues. There's no "probably fine".
- **Fixed merge order** follows the dependency direction: roster → data → story → matching → media. A manifest merges in that order or not at all.
- **Invalidation is targeted.** A claim correction invalidates only the narration spans, VisualTasks and asset uses linked to that claim ID (final plan: "invalidates only the affected narration and scenes"). This only works if receipts record the IDs listed in answer 6.

### 8. Provider assignments that should differ

| Agent | Codex hypothesis | My proposal | Reason |
|---|---|---|---|
| Coordinator | GPT-6 Astra | **Claude Opus 5.5** (Astra as challenger) | Long-horizon orchestration is what agentic benchmarks measure; Oct 2026 BenchLM: Opus 5.5 88.1 vs Astra 70.7. Low call volume, so cost doesn't matter much. |
| Story | Claude Opus 5.5 | Agree; add Fable 5.1 as a challenger | Decide by a blind editor read |
| Data | GPT-6.1 Sol, Astra escalation | Agree on the mid-tier, with a Claude Sonnet 5.5 challenger; cheapest passing model for bulk extraction | Volume work |
| Matching | GPT-6 Astra at `xhigh` | **Mid-tier default** (Sonnet 5.5 or Sol), escalating to Astra/Opus on hard beats | Matching runs per VisualTask; a flagship at xhigh on every task is the largest avoidable cost. Keep Astra if the eval shows the mid-tier fails. |
| Media semantic | Gemini multimodal | Agree; run a vision bake-off on our own frames | Strong vision per dollar |
| Roster | Cheapest passing | Agree; deterministic first | — |

Caveat: the network blocked the official OpenAI docs and the leaderboard sites in my session, so model names and scores come from search summaries. All of these are hypotheses until the shared eval runs. On that, Codex and I agree.

### 9. Fastest falsifying vertical slice

Codex proposes coordinator + one Matching task. That tests the runner but not the riskiest seam. I propose **one StoryPackage across two providers with a forced loop-back**:

1. Story (Claude CLI) produces a StoryPackage from the Drake / Year Seventeen trace, with one deliberately unshowable pivotal beat.
2. Matching (Codex CLI) runs `check_feasibility`, finds the unfillable beat, and returns `blocked: story` with a typed reason.
3. The coordinator routes the revision back to Story, invalidates only the affected VisualTasks, and re-dispatches.
4. Kill the coordinator mid-run, restart it, and recover from durable state alone.

In one run, this tests: cross-provider handoff, receipt validation, blocker ownership, the bidirectional story/visual loop (final plan, accepted point 6), targeted invalidation and context-reset recovery. If any of those fail, the architecture is wrong in a way a single-layer slice wouldn't show.

### 10. Parts that could recreate drift, false completion or story coupling

- **Self-reported receipts.** Codex already requires the coordinator to re-run acceptance checks independently. Keep this non-negotiable, and make the checks deterministic code, not a model judging a model.
- **"Ready independent work takes precedence over an unrelated human-review wait."** This is correct only if "independent" is computed from the dependency graph. Otherwise Matching and Media will happily build on an unapproved script, then everything is invalidated. Work that depends on a gated artifact must wait.
- **Prompt-only domain rules.** Rules like "no causal claim without mechanism" or "never invent cohort membership" will drift if they live only in prompts. They need validators exposed as MCP tools and hooks, as in my plan's section 2.
- **Matching fixtures from a single story.** Codex's "two regression packages + one untouched StoryPackage" is the right guard against story-specific coupling. Extend the same rule to Story and Data fixtures.
- **Tuning on the eval.** Agree with Codex: freeze the held-out set and never iterate prompts against it.
- **Repo mismatch.** Building Matching on `astra-visual-selector` would itself recreate the drift the user moved away from (see answer 1).

## What my plan adds that Codex's lacks

The specifics are in `agents/CLAUDE_agent_system_plan.md`, sections 2–5:

- **Story Writer loop** with hard, tool-enforced rules.
- **8 skills:** narration voice, narration-script analysis (as diagnostics only), Story IR format, claim discipline, rap metrics contract, entity context, template specs, media briefs.
- **6 MCP servers:** roster, research, story, matching (`forecast_demand`, `check_feasibility`), media, pipeline. Plus existing GitHub and vidIQ servers.
- **Plugins:** `documentary-core` shared by every repo, plus one per agent, with hooks that run validators before any submission.

These slot directly into Codex's profile fields: `tool_policy` lists the MCP servers and `prompt_version` points at the skill set.

## Proposed reconciled build order

1. **Contracts:** Codex's profile, task contract, run-state and receipt schemas (with the fields from answer 6), plus StoryIR/VisualTask schemas and `validate_story_ir`. No model calls.
2. **Roster MCP server** around `roster/roster.py`.
3. **Runner adapters** for Claude CLI and Codex CLI with `capabilities()`.
4. **Story and Matching MCP servers** with only the tools the slice needs.
5. **The vertical slice** from answer 9.
6. Data and Media agents one at a time; then hardening (Codex phase 5).

## Decisions needed from the user

1. Matching repo: confirm `matching_layer` is active and astra-visual-selector is baseline only.
2. Story's home: new repo, or a folder in content-project-mgr for now?
3. Registry home: `entity_roster` or `content-project-mgr/roster/`?
4. Coordinator default: Claude Opus 5.5 or GPT-6 Astra, pending eval?
5. Per-video spend ceiling.
