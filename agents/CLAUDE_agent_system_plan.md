# Agent system plan: Story Writer and the layers as agents (Claude)

**Date:** 2026-10-03
**Author:** Claude (Claude Code session)
**Status:** proposal for review. No code yet. Compare against Codex's plan before choosing.
**Builds on:** `final_documentary_system_plan.md` (artifact contracts and decisions) and `codex/entity-context-roster` (`roster/`: entity-context schema, validator, authority order).

This plan doesn't reopen anything decided in `final_documentary_system_plan.md`. It describes how to turn that architecture into agents: which agent owns which artifact, which tools each one gets, which skills and plugins carry the rules, and which model each one runs by default.

## 1. Principle: agents own artifacts, MCP servers own data

Each agent produces exactly one or two of the contract artifacts and reads the others through tools. Deterministic work (validation, the metric checker, roster resolution, rendering) stays as plain code exposed as MCP tools and never as model judgment.

| Agent | Repo | Produces | Consumes |
|---|---|---|---|
| **Coordinator** | `content-project-mgr` | OpportunityCard routing, stage state, gate decisions, revision requests | every artifact's status |
| **Research / Data** | `Polish` (hiphop-research-engine) | EvidenceRecord, ClaimLedger candidates, metric-check results | EntityRegistry |
| **Story Writer** (new) | new repo or `content-project-mgr/agents/story_writer` | StoryIR + script, VisualTask drafts | ClaimLedger, roster, feasibility reports |
| **Matching** | `matching_layer` (v2); `astra-visual-selector` frozen as the eval baseline | VisualPlan (fillable_now / conditional, media briefs) | VisualTask, template specs, asset index |
| **Media** | `media_layer` | Assets, AssetUse, sourcing results, kits | media briefs, VisualPlan |
| **Roster service** (not an agent) | `entity_roster` / `roster/` | EntityRegistry + resolved context | everyone |

## 2. Story Writer agent

### Loop

1. Receive an OpportunityCard from the coordinator.
2. Build 2–4 **story centers**: central question, defensible answer, strongest alternative, key receipts, missing research.
3. Query research for claims; request new research for gaps through the coordinator. It never researches the web directly into narration.
4. Resolve every referent through the roster. Unresolved identity stays explicit.
5. Write the beat map, then the outline, then call the **outline-level feasibility** check (matching `forecast_demand`).
6. Revise for unshowable pivotal beats (research, graphic, reframe, cut) before lock.
7. Write the voice-ready script. Link factual spans to claim IDs and mark the rest as interpretation, question, setup or transition.
8. Self-check with the deterministic validators, then submit the StoryIR, script and VisualTask drafts to the coordinator for editor review.

### Hard rules (enforced by tools and hooks, not just prompts)

- A factual narration span without an `accepted` claim ID can't be submitted (validator).
- Causal or motive language requires a claim with a supported mechanism (final plan, decision 2). The checker flags causal verbs on spans linked only to event claims.
- `claim.kind` may *suggest* `visual_intent`, but the writer sets it explicitly (decision 1).
- Editor context from the roster outranks data-derived characterization (roster authority order).
- Playbook patterns are prompts, not pass/fail (decision 6). The analysis skill produces diagnostics, never a score that gates approval.

## 3. Skills (instructions loaded on demand)

| Skill | Used by | Content |
|---|---|---|
| `narration-voice` | Writer | Channel promise, voice, reference excerpts, banned moves. Needs the owner's editorial promise (final plan input 4). |
| `narration-script-analysis` | Writer, editor | The narration-script analysis strategy (24-video observations, hooks/re-hooks/payoffs, 7 blueprints, 10 signature families) as **optional diagnostics** |
| `story-ir-format` | Writer, matching | StoryIR/script/VisualTask schema with worked examples |
| `claim-discipline` | Writer, research | Observed vs documented vs hypothesis; what causal claims require; how to narrate where inference stops |
| `rap-metrics-contract` | Research, writer | `GAPS.md` rules as written guidance alongside the machine checker |
| `entity-context` | All | How to use the roster: IDs, cohorts, the authority order, never inventing membership |
| `template-specs` | Matching | How to read template specs, slot constraints, and when to issue a conditional option |
| `media-brief` | Matching, media | Typed sourcing-brief format, rights basis, disclosure rules |

## 4. MCP servers (to build)

| Server | Key tools | Backed by | Notes |
|---|---|---|---|
| `roster` | `resolve_entity`, `get_entity_context(story_id)`, `expand_cohort`, `propose_entity` | `roster/roster.py` | Wrap Codex's existing validator/resolver; no model calls |
| `research` | `search_evidence`, `get_claims(entity_ids, topic)`, `request_research`, `check_metric` | Polish | `check_metric` returns pass / pass_with_material_caveat / needs_research / reject |
| `story` | `save_draft`, `validate_story_ir`, `link_span_to_claim`, `diff_versions`, `submit_for_review` | new store | `validate_story_ir` enforces the hard rules above |
| `matching` | `forecast_demand(outline)`, `check_feasibility(visual_tasks)`, `get_visual_plan`, `browse_templates` | matching_layer | `forecast_demand` closes the story/visual loop |
| `media` | `search_assets`, `get_asset`, `submit_brief`, `get_brief_status`, `record_asset_use` | media_layer | Rights and use decisions stay human-approved |
| `pipeline` | `get_project_state`, `advance_stage`, `request_revision`, `log_metric` | content-project-mgr | Only the coordinator can call `advance_stage` |

Existing servers worth using: **GitHub MCP** (issues as the work queue; matches the current `issues_*` tracking), **vidIQ MCP** (`outliers`, `trending_videos`, `keyword_research`, `video_transcript`) for OpportunityCards and hook study, and web search/fetch only inside the research agent.

## 5. Plugins

- **`documentary-core`**: the `roster` MCP config, `entity-context` and `claim-discipline` skills, and shared schemas. Every repo installs it.
- **`story-writer`**: writer skills, the `story` server, `/write-episode <opportunity_id>` and `/revise-beat <beat_id>` commands, and a hook that runs `validate_story_ir` before any `submit_for_review`.
- **`matching`**, **`media`**, **`research`**: each layer's skills, server and commands.
- **`coordinator`**: `/new-project`, `/status`, `/gate <stage>`, and a scheduled routine for the weekly 2–3 video cadence.

Hooks enforce the gates deterministically (schema validation, unresolved entity IDs, unsupported causal spans) so model compliance isn't the only safeguard.

## 6. Default models

Searched 2026-10-03. The network blocked the official OpenAI docs and the leaderboard pages, so OpenAI names come from search summaries; confirm exact IDs before use. October 2026 agentic leaderboard (BenchLM): Claude Opus 5.5 88.1, Claude Fable 5.1 78.9, Claude Opus 5 77.6, Gemini 4 Argon 74.2, GPT-6 Astra 70.7. The OpenAI Agents SDK defaults to its Luna tier; Sol is the balanced tier and Astra the flagship.

| Agent | Default | Cross-provider alternative | Reason |
|---|---|---|---|
| Coordinator | Claude Opus 5.5 | GPT-6 Astra | Long-horizon planning and recovery; low call volume |
| Story Writer | Claude Opus 5.5 (try Fable 5.1 head to head) | GPT-6 Astra | Writing quality and rule-following are the product; decide with a blind editor read |
| Research / Data | Claude Sonnet 5.5; Haiku 4.5 for bulk extraction | OpenAI Sol / Luna | Structured extraction at volume; pick bulk models by JSON validity on our documents |
| Matching | Claude Sonnet 5.5 | OpenAI Sol, Gemini mid-tier | High volume; if matching on images, run a vision bake-off on our frames |
| Media | Claude Haiku 4.5 | OpenAI Luna | Mostly deterministic pipeline; the model only routes and tags |
| Roster | No model; Haiku only for fuzzy alias/dedupe suggestions | — | Data service; deterministic resolution |

Each agent's model is a config value. Choose with the Stage 0 eval set (31 matching reviews, the 40-beat example, negative controls), not leaderboards.

## 7. Build order (follows the final plan's stages)

1. **Roster MCP server** around `roster/roster.py`. Everything depends on IDs.
2. **StoryIR / VisualTask schema + `validate_story_ir`** (Stage 1 gate).
3. **Research MCP server** (`get_claims`, `check_metric`) over Polish (Stage 2).
4. **Story Writer agent** on the Claude Agent SDK with the `story-writer` plugin; first run on the Drake / Year Seventeen trace.
5. **Matching `forecast_demand` / `check_feasibility`** to close the loop (Stage 3).
6. **Coordinator** wiring the stages, then a media agent.

## 8. Open inputs

- The narration-script analysis strategy document, to turn into the `narration-script-analysis` skill.
- Where `matching_layer` lives and its current interfaces; whether `entity_roster` replaces or wraps `roster/`.
- Channel editorial promise and voice references (for `narration-voice`).
- Per-video model spend ceiling (affects the Opus vs Sonnet choice for the writer and coordinator).
