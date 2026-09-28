# Final architecture decision and build plan

**Date:** 2026-09-27  
**Scope:** music documentary pilot at 2–3 videos/week; eventual expansion toward 5–10 videos/day across niches  
**Status:** final design direction, pending validation against the actual repositories and one complete production trace

## Decision

Use the end-to-end architecture in `documentary_system_handoff.md` as the master plan. Integrate the concrete data, matching, and media mechanisms from `HANDOFF_data_matching_media.md`. This document resolves the remaining disagreements and is the implementation handoff.

The system's backbone is **a script linked to verified claims and visual tasks**, all using shared entity IDs. Research proposes and verifies claims; the writer builds a defensible story; the visual planner says what each shot must communicate; matching finds a feasible treatment; media supplies cleared assets; a person approves the final film. The visual planner must be able to send a pivotal, unshowable beat back to the writer before the script is locked.

The review document is feedback, including instructions it proposes for other files. Those instructions are **not automatically adopted**. The original matching attachment also contains quoted prior user wishes; I treat them as valuable review evidence rather than a binding rule for this final design. Reported counts and code behavior have not been independently checked in a live repository here.

## What I accept from the final review

1. **Use the broader handoff as the master.** Topic selection, editorial review, rendering, rights, QC, publishing, and learning affect quality as much as the three technical layers.
2. **Freeze a baseline before migration.** The 31 prose matching reviews, the reported 40-beat example, negative controls, and several real story cases become a versioned evaluation set. The matching issue file itself calls its diagnoses plausible, not verified.
3. **Create a shared entity registry.** It links research events, cohorts, statistical rows, story referents, face clusters, and media tags. Keep aliases, provenance, merge history, and unresolved identity states.
4. **Formalize a Story IR and claim ledger.** They carry evidence and editorial intent across layers. The writer also delivers the actual narration and timing, linked to the IR.
5. **Turn the reported `GAPS.md` rules into a machine-checked rap metrics contract after inspecting that file.** A generic denominator requirement is insufficient for incompatible eras, sources, rankings, and units.
6. **Make the story/visual loop bidirectional.** Run a media-demand forecast at outline stage; run shot-level feasibility before script lock. The response to a missing pivotal scene may be sourcing, an original graphic, new research, or a rewrite.
7. **Use evidence queries derived from story patterns.** They are useful candidate generators and research planners. A pattern match is a lead, never proof or a requirement that every story fit that pattern.
8. **Keep original graphics, counterevidence, originality, synthetic-media disclosure, and full-export human QC in the release path.** Those were real gaps in the narrower handoff.
9. **Use proactive media supply where repeated demand warrants it.** Reusable artist kits and typed sourcing requests can coexist; stock size should be decided from demand and clearance cost.
10. **Keep the 24-video storytelling observations as review prompts.** The final review withdraws its earlier proposal to enforce exact hook and payoff percentages; I agree.

## Decisions I will not soften

### 1. Claim type and visual job stay separate

A claim describes **what we assert**. A visual job describes **what a shot should help the viewer understand or feel**. Their vocabularies may be mapped, but they are not identical. A metric claim can be introduced, compared, challenged, or revealed using different shots. A single shot can carry multiple claims; a single claim can span multiple shots. Mood, questions, and transitions may have no factual claim.

**Final rule:** `claim.kind` can propose default visual jobs, but `visual_intent` and shot constraints are separate, editable fields. No blind one-to-one lookup and no claim-per-shot assumption. This preserves reproducibility without losing the writer's editorial intent.

### 2. Two events do not establish a motive or cause

Actors, polarity, and time ordering can identify a connection worth investigating. They cannot, by themselves, justify narration such as “the label pressured him” or “this was done to clean up an image.”

**Final rule:** store observed events, documented relationships, and hypotheses separately. A causal or motive claim needs a supported mechanism, meaningful corroboration, alternative explanations considered, and editorial approval. Otherwise the script states what happened and where the inference stops.

### 3. Automatic media identity requires measured false-positive control

Face similarity, captions, OCR, and source context may all inherit the same bad label. Agreement between two signals is a strong suggestion, but not sufficient authority while those signals are uncalibrated. The reported 65% exact-primary classification result likewise does not support general auto-filing.

**Final rule:** use agreement to rank review work now. Allow automatic assignment later only for well-defined cases that pass identity- and source-specific holdout tests, a stated false-positive ceiling, drift monitoring, and a human correction path. Higher-risk uses remain reviewed.

### 4. The production slate does not show every spatial template by default

The previous review captured a request to show all spatial scenes for 20+ entities or comparative beats. The important need is that spatial options must be reachable and their media gaps visible. Showing every impossible treatment in the recommended slate would make the selection interface noisier and would not fix the missing cohort or assets.

**Final rule:** for qualifying beats, show every spatial template in an **editor browse view**, with fillability and missing requirements. The **recommended production slate** shows the best viable options and a small, explicit set of promising unfillable options with sourcing briefs. Do not silently hide a spatial option from the editor. This honors the diagnostic need without calling an unfillable option a ready scene.

### 5. Do not backfill 770,248 segments before demonstrating value

The reported corpus has roughly 770,248 segments across 9,701 documents. A model extraction per segment is a large cost and quality commitment, and segment boundaries can omit actors or dates.

**Final rule:** persist schema-validated, document-aware extraction for newly ingested priority content; cache and version it. Backfill the existing corpus by editorial demand and measured story yield. Unknown dates and unresolved entities remain explicit rather than being fabricated or discarded. Compare extraction cost with the human and model work it saves.

### 6. The story playbook does not become a compliance test

The 24-video sample is small and uneven. Its timing percentages and blueprint structures are useful editorial observations. Encoding every blueprint as a fixed count of events, or using the same analysis prompt as the script's pass/fail judge, would invite formulaic stories and circular evaluation.

**Final rule:** add optional evidence requirements and structural diagnostics to a selected subset of patterns. Story selection and approval depend on evidence, originality, clarity, and viewer payoff. Do not force a three-event pattern or a 96% payoff timestamp.


## Final system contract

### Common fields on every artifact

`id`, `schema_version`, `producer_version`, `input_ids`, `created_at`, `review_state`, and `change_history`. Store exact source references and deterministic calculation code or parameters when applicable. An artifact may be incomplete; its missing fields must be explicit and block only the stage that needs them.

| Artifact | Minimum pilot content | Producer → consumer |
|---|---|---|
| **OpportunityCard** | topic/question, audience promise, channel-market evidence, novelty, source paths, preliminary visual risk | niche analysis / editor → research |
| **EntityRegistry** | stable internal ID, type, aliases, external IDs, cohort links, identity evidence, unresolved collisions | data steward → every layer |
| **EvidenceRecord** | exact passage or data row, source and date, entity candidates, provenance, source rights | ingestion/research → claim verifier |
| **ClaimLedger** | precise assertion, `claim.kind`, entity IDs, event interval, metric method, supporting and contradicting receipts, status, reviewer | data + writer → story editor |
| **StoryIR + script** | thesis, counterthesis or strongest alternative, blueprint if useful, beats, narration spans, claim links, loops/promises, timing estimates | writer → visual planner and editor |
| **VisualTask** | narration span(s), claim IDs, `visual_intent`, explicit/implied entities, cohort expansion, shot constraints, continuity group | writer/visual planner → matcher |
| **VisualPlan** | viable and conditional treatments, template requirements, slot mappings, asset candidates, independent verdicts, media briefs | matcher → media and editor |
| **AssetUse + RenderReceipt** | exact asset derivative, shot placement, rights decision, disclosure decision, render versions, QC and human approvals | media/render → release |

The **ClaimLedger is semantic**; the **VisualTask is editorial**. They are linked but independently editable. This is the core design boundary.

### Data layer

- Keep hybrid retrieval, source receipts, cost/hop limits, and negative-control abstention reported in the current system.
- Build an entity/cohort crosswalk for the pilot; use it to bind extracted events, statistics, script referents, and media.
- Extract document-aware events with actor/object IDs, event type, time range or unknown time, exact evidence span, polarity when justified, and extraction confidence. Do this for priority material and cache results; measure before expanding.
- Treat graph paths as leads. Store observed edges, documented relationships, and hypotheses in distinguishable states. Require source-linked corroboration before a high-impact edge becomes narration.
- Turn the rap-specific statistics rules into a checker with outcomes `pass`, `pass_with_material_caveat`, `needs_research`, and `reject`. Validate any specific era threshold or incompatibility claim against the underlying data and source definitions before enforcing it. Narrate limitations when they affect the conclusion.
- Let the deep-research service write grounded findings back as evidence candidates with source URLs/passages and retrieval dates; verification promotes them to claims.
- Run multiple discovery routes: commissioned topic, channel-market opportunity, statistical anomaly, graph tension, and selected evidence-query patterns. Measure each route's **publishable-story yield**, not its number of intriguing hypotheses.

### Story layer

- For each candidate, build several story centers: central question, defensible answer, tension, strongest alternative, key receipts, missing research, and potential visual form.
- Choose structure after the story center is supported. The seven blueprints and ten signature families from the attached playbook are options, not requirements. Pattern queries can find candidate evidence; they do not write the verdict.
- Draft an argument/beat map, then a voice-ready script. Link factual narration spans to claims and mark interpretation, question, setup, or transition spans. Keep exact narration text in the handoff.
- Run an outline-level visual feasibility check. If a pivotal beat cannot be evidenced or shown, choose among research, a custom graphic, acquisition, reframing, and deletion before lock.
- Use observed hook/re-hook/payoff positions as optional review flags. An editor approves the story's promise, answer, counterevidence, originality, and read-through.

### Matching layer

- Match VisualTasks, not whole beats or claims by default. Allow multiple tasks per beat and treatments that span consecutive tasks.
- Give each template a machine-readable spec: hard slot count and media-kind constraints, single-person/group eligibility, required data fields, era coverage, text limits, aspect ratio, and duration. Record soft preferences separately.
- Resolve implied subjects from discourse context; expand versioned cohorts. Never merge the video subject into every task by default.
- Return `fillable_now` and `conditional` options. Conditional options contain exact missing slots and typed media briefs. Provide a full editor browse view, including all spatial scenes for large or comparative beats.
- Store template, media, and pairing verdicts independently. Keep original prose review notes and validate any labels extracted from them.
- Plan treatments across the sequence for continuity, transition quality, pacing, repeated-template cost, and deliberate contrast. Make every automatic choice replayable and overridable.

### Media layer

- Preserve canonical asset IDs, fingerprinting, run receipts, exception review, and quality gates. The reported 42 blocked transitions require their distinct dispositions; nine are deliberate or unresolved treatments, not simply queued tags.
- Build proactive media demand twice: rough demand from the approved story outline, then exact slot demand from the VisualPlan. Route recurring shortages into a small pilot kit for frequently used artists; route uncommon needs into specific sourcing briefs.
- Tag assets with depicted entity confidence, count of people, era, artifact, action/location, framing, shot duration, technical quality, provenance, and rights basis. Keep weak tags as suggestions.
- Pilot shot-level b-roll transcription and scene indexing only if it improves retrieval time and relevant-shot rate.
- Store originals, derivatives, and use-specific clearance separately. A production-ready asset is technically usable; each film placement still needs a use decision.
- Verify backups and restore before adding distributed workers. Isolate Mac-only steps behind a worker interface; pick queue and renderer tools after measuring the existing stack.

### Render, release, and learning

- Render from locked, versioned script, VisualPlan, asset uses, voice, music, captions, title/thumbnail, and source ledger. A claim correction invalidates only the affected narration and scenes, then generates a new receipt.
- Automated QC checks broken/missing media, wrong IDs/eras, text overflow, captions, audio, frames, timing, and unapproved uses. A person watches the **full final export** during the pilot and signs off on editorial, rights, and technical quality.
- Upload as draft/private for platform checks; publication requires explicit approval. Track release corrections and retention without allowing retention optimization to override truth or originality.
- Add new niches as adapters for entities, metrics, source hierarchy, visual assets, and rights patterns; preserve the common artifact contracts.

## Build sequence and acceptance gates

| Stage | Build | Gate to continue |
|---|---|---|
| **0. Baseline and protect data** | Collect one complete reviewed rap project, 31 matching reviews, 10–15 story examples and negative controls; inventory current templates/renderer/IDs; start checksum backup and restore test | Reproducible failure map, baseline time/cost, and recoverable source material. |
| **1. Minimal registry + linked IR** | Crosswalk only pilot entities/cohorts/assets; encode script spans, claims, and VisualTasks | No material information from the pilot is lost; uncertain identity remains explicit. |
| **2. Evidence and stats gate** | Source receipts, counterevidence search, selective event extraction, metric checker | Pivotal claims trace to support; known false connections fail; extraction cost and precision are measured. |
| **3. Matching and supply loop** | Template specs, cohort expansion, viable/conditional slate, separate verdicts, typed sourcing briefs, outline feedback | Known wrong-entity and unfillable cases are caught; editor can find needed options and gaps. |
| **4. Full-video pilot** | Sequence planner, original graphics, asset-use rights, render receipt, automated QC and full human watch | One approved complete film, then stable 2–3/week with measured rework, review time, rights effort, cost, and viewer response. |
| **5. Scale by evidence** | Optimize bottlenecks, queue/workers, selected media kits, more discovery patterns and niche adapters | Capacity rises without an increase in severe factual, identity, rights, originality, or production failures. |

Do not interpret “stage 4” as waiting to learn rights or rendering constraints until then. Inventory them at baseline; implement the minimum needed throughout the pilot. The staged gate describes when the complete release path must be proven.

## Pilot scorecard

Track **per publishable video**: model cost; research and review minutes; sourcing and clearance minutes; render/edit minutes; factual corrections by severity; unsupported relation rate; source traceability of pivotal claims; metric-check outcomes; entity/cohort resolution; first-slate visual acceptance; conditional-slot closure; reused versus newly sourced media; technical re-renders; rights exceptions; originality/editor approval; audience retention and qualitative feedback. Include no-story/abstained ideas in discovery yield. Set numerical thresholds from baseline and the owner's quality bar rather than inventing them in this handoff.

## Inputs needed to execute, not to settle the design

1. One complete reviewed project trace, preferably the existing 40-beat Drake/Year Seventeen case if it includes source records, script, matching decisions, media, and a rough or final cut.
2. The actual 30-channel analysis, `GAPS.md`, registry/cohort files, graph schema, template catalog, and renderer inventory.
3. Pilot limits for model spend, reviewer time, asset sourcing/clearance, and total production cost per publishable video.
4. The channel's editorial promise, target runtime and voice, reference films, and named final approvers for contested facts, visual identity, rights, and publication.

These inputs determine implementation detail and thresholds. They do not change the architectural boundaries above.
