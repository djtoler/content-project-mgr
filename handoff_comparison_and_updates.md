# Comparison of the two architecture handoffs

**Date:** 2026-09-27  
**Compared:** `HANDOFF_data_matching_media.md` (new feedback) and `documentary_system_handoff.md` (my earlier handoff)

## Verdict

The new handoff improves the **implementation specificity** of the data → story → matching → media seam. It identifies a canonical entity registry, a Story IR, template requirement specs, typed media briefs, and sequence-level matching as concrete integration work. I agree with that direction and would incorporate most of it.

Its strongest claims should be treated as **design hypotheses**, not settled fixes. In particular, a claim's factual type cannot always determine its visual communication job; two time-ordered events do not establish a causal relationship; and two agreeing media signals do not automatically justify an identity decision. The update should retain the new handoff's concrete contracts while adding uncertainty, evaluation, and editorial gates.

The new document says it read several repositories and files not supplied in this conversation (`GAPS.md`, `JOBS.md`, `GRAMMAR-v2.md`, `SCOPE.md`, and source code). I can compare its reported findings with the attachments, but I have **not independently inspected those extra files or the running systems**. Its opening status correctly says its recommendations are unbuilt and unmeasured. References to a quoted prior user instruction or repo rule are context, not a new instruction from this request.

## Where I agree

| New feedback | My assessment | Update to make |
|---|---|---|
| One entity registry across research, cohorts, matching, and media | Strongest operational insight. My handoff asked for shared IDs but did not make registry migration the first cross-layer deliverable. | Specify a versioned registry with aliases, external IDs, cohort membership, evidence for identity merges, and a crosswalk to existing IDs. |
| Claim ledger and structured Story IR | Strong agreement. This is the right seam between fact finding, script, and visual planning. | Define the schema and migration path on one real video before broad adoption. Keep prose/script alongside the structured representation. |
| Extract typed events with source spans and time | Valuable way to stop keyword co-occurrence from masquerading as a relationship. | Pilot extraction on a curated subset, measure precision, and only then expand. Store uncertain and undated records instead of forcing them into false precision. |
| Machine-enforced metric comparability | Concrete improvement over my general requirement for denominators and reproducible calculations. | Add metric lineage, unit, population, time window, coverage, and comparability rules; test each rule against real claims. |
| Template slot specs and feasibility checks | Directly addresses PI-07/08 and the false promise of a visually plausible but unfillable slate. | Make requirements a versioned catalog; return both fillable options and sourcing options, visibly separated. |
| Sequence-level matching and independent verdicts | Correct for continuity (PI-09) and “right media, no template” (PI-10). | Model treatment runs across claims/shots, and store media, template, and pairing judgments separately. |
| Typed media briefs and proactive sourcing | A meaningful improvement over reactive intake. | Generate briefs after an approved story outline and again after the visual plan, so early sourcing remains adjustable. |
| Existing gates and receipts | Keep them. My handoff likewise preserved media lifecycle receipts and exception review. | Connect gate results to video-level state and reviewer queues. |
| No invented rating baseline | Correct reading of PI-11. | Use structured reasons derived from review notes, with human validation of the label mapping. |

## Where I disagree or would narrow the claim

### 1. Factual claim type is not the same as visual job

The new handoff proposes a closed claim-type list that mirrors matching jobs, so job choice becomes a lookup. That conflates **what is asserted** with **how a shot communicates it**. “Artist A released eight albums in period X” can be shown as a timeline, cover rail, count-up, chart, or performance montage depending on narrative context. One claim may need two shots; one shot may combine several claims. A job may also communicate a question, contrast, or mood without asserting a new fact.

**Revision:** keep separate fields for `claim.kind` (event, metric, comparison, quotation, interpretation), `visual_intent` (compare, locate, sequence, prove, reveal, evoke), and `shot_requirements`. Derive candidate jobs from the claim plus story role and nearby shots, then let the matcher rank feasible treatments. This may reduce paid classification, but it does not eliminate interpretation.

### 2. “The writer never hands off prose” is too absolute

The writer must deliver narration and timing for voice and edit. A structured Story IR should travel **with** the script, not replace it. Each factual narration span should reference claim IDs; each shot should reference the narration span and the claims it carries. Creative narration can be tagged as interpretation, setup, or transition.

**Revision:** change the line to: “The writer hands off a script linked to a validated Story IR; matching reads the IR and the exact narration span.”

### 3. Extracting every segment at ingestion is an unproven cost and quality bet

The attachment reports about **770,248 segments across 9,701 documents**. A “one-time model run per segment” is therefore potentially hundreds of thousands of extraction calls or batches, not 9,701. Some segments lack a complete event or its date; splitting context at segment boundaries can produce incorrect actors or chronology.

**Revision:** pilot a document-aware extractor on the sources used by approved topics, with priority by editorial demand and retrieval frequency. Reuse cached results and extend incrementally. Measure event precision, entity binding, date quality, cost, and later story yield before backfilling the corpus. Keep event time as a range, unknown, or inferred status; do not reject every undated event.

### 4. Paired events do not prove pressure, incentive, or causation

Two events with actors, polarity, and order are useful candidates for investigation. They are not sufficient to assert a motive or causal edge. Temporal order alone can generate the very type of “clean up Future's image” error the current data layer warns about.

**Revision:** distinguish `observed_event`, `documented_relationship`, and `hypothesis`. Derived causal or motive claims require a stated mechanism, direct testimony/documentation or strong triangulation, plausible alternatives considered, and editorial approval. If those conditions fail, narrate the chronology without claiming why it happened.

### 5. Pattern-first discovery should be one path, not the search engine's organizing principle

Turning every blueprint into an evidence query is a promising experiment, especially for rankings and repeated measurable sequences. But story blueprints were inferred from a small, uneven sample and describe **presentation**, not a complete ontology of true stories. Hard rules such as “three milestone → rejection → response triples” could reward forced narratives and miss original ones.

**Revision:** run several candidate generators in parallel: anomalies, graph tensions, direct editorial questions, channel-market opportunities, and a small set of high-precision pattern queries. Compare their publishable-story yield. Choose the structure after evidence supports a story center, and allow the writer to reject a pattern.

### 6. Quantified storytelling positions should not be a hard QA gate

The new handoff proposes reusing the analysis prompt on generated scripts and checking a hook at ~1%, payoff ~96%, re-hook ~12%, and opening callback. These are observations from 24 selected videos, with sample caveats in `story_layer.md`. A generated script can pass those proportions while being repetitive, unsupported, or dull. The same analysis prompt judging its own template also risks circular validation.

**Revision:** use those checks as editorial diagnostics. Separate structural analysis from independent human reviews of clarity, originality, evidence, and audience comprehension. Retention and satisfaction from published videos can later test whether any timing heuristic actually helps this channel.

### 7. “Offer all spatial templates” is too broad as a production rule

The prior matching file quotes the user's wish to show all spatial scenes for 20+ entities or comparative beats. That is important feedback from the review, but the rule was not validated against every spatial template's slot count and purpose. “Any comparative intent” could include a two-item contrast best shown by a side-by-side graphic.

**Revision:** ensure spatial templates are **discoverable** for large/cohort or spatially meaningful comparisons. Show viable spatial options, plus a clearly marked “requires assets or adaptation” list where appropriate. Preserve the ability to browse all spatial templates in an editor, but do not flood the recommended slate with impossible options.

### 8. Media auto-approval needs calibrated evidence, not just agreement

A face cluster, caption/OCR, and source context may be correlated or share the same wrong label. Two agreeing signals are a useful review priority, not a proof of identity. Likewise, a wide classification margin plus source metadata does not establish that the 65% exact-primary classifier is safe to auto-file.

**Revision:** separate high-confidence **suggestion** from automatic promotion. Calibrate on artist-specific and source-specific holdouts, including lookalikes, group shots, alias collisions, and mislabeled posts. Define a very low tolerated false-positive rate, monitor drift, and retain human review for identities or classes that can mislead a documentary.

### 9. Standing media kits are a hypothesis, not a default build target

The proposed 150–300 artist kits would imply at least 450–900 portraits and 300–600 performance clips, before covers, interviews, derivatives, rights work, and storage. The reuse benefit is plausible, but the attachment does not show demand concentration or rights availability sufficient to justify that investment.

**Revision:** start with the next approved slate and the most reused entities from actual scripts. Build a small kit standard, measure reuse, cost, and clearance effort, then expand to the point where stocked media beats on-demand sourcing. Distinguish a **searchable lead** from a **cleared production asset**.

### 10. Rights status needs more than “safe to use in a monetized video”

That phrase is too coarse for clips, music, photographs, social posts, and AI depictions. Assets may be usable only for a particular edit, platform, term, territory, or purpose; some use may rely on a case-specific legal analysis rather than a general license.

**Revision:** store rights basis, proof, owner, permitted use, territory, term/expiry, attribution obligations, edit restrictions, and clearance decision per usage. The video-level RenderReceipt should link each asset use to its decision. Keep public-search availability separate from permission.

### 11. Tool choices and build order are premature

Postgres queues, Whisper, PySceneDetect, nexrender, and aerender may be sensible, but the supplied context does not establish the current renderer, failure modes, throughput budget, or constraints. The new handoff also places storage and worker recovery after media kits and sequence planning, although losing the canonical local library would be a more immediate operational risk.

**Revision:** describe required capabilities and test candidate tools against the existing stack. Establish backup plus restore verification early; add distributed workers only after one-machine performance and bottlenecks are measured. Defer cloud GPUs until a workload actually needs them.

## What the new feedback showed I missed

1. **Registry migration needs to be a named project.** I specified shared entity IDs but did not spell out how roster entries, cohort CSVs, face clusters, and external IDs would merge or how collisions would be reviewed.
2. **The statistics contract deserves its own checker.** I required denominator and transformation lineage, but the new handoff adds a practical route to machine-enforced comparability. Its examples need validation against `GAPS.md`, which was not supplied here.
3. **The writer's output needs a formal IR schema.** My BeatSpec and ClaimLedger were directionally right; the new handoff makes the linking contract more explicit. I would add narration-span and shot-span mappings.
4. **Preproduction media demand should be calculated early.** I described asset-gap requests after matching, but an outline-level forecast could surface a 93-person cohort or rare performance footage before script lock.
5. **Media and template verdicts need separate records.** I mentioned media approval independent of templates; the new handoff makes that a first-class review model and directly addresses PI-10.
6. **Sequence optimization is a real matching layer.** I called for continuity runs but did not specify a whole-video planner or the tension between continuity, pacing, and template variety.
7. **A model and human-time budget are architectural inputs.** The new handoff surfaces the previously discussed possibility of no LLM API calls at high volume. Without an explicit budget, extraction and review design cannot be sized.
8. **Existing runtime ownership matters.** The proposed Mac-specific worker boundary, AE/Remotion inventory, and distinct template counts are useful questions. My plan was too abstract on integration with the current production stack.

These points improve my handoff, but they do not imply that the new document's specific fixes have been verified in the live system.

## How I would update the new handoff

### Replace the “one structural change” section

Describe **three linked contracts**, not two:

1. **Entity/asset registry:** stable internal IDs, alias and cohort crosswalks, provenance, merge history, and uncertainty.
2. **Evidence/claim ledger:** precise assertion, supporting and opposing evidence, event time, metric method, status, and review state.
3. **Story-to-visual IR:** script spans → claims → visual intents/jobs → shot requirements → template slots → asset uses, including continuity groups and rights state.

An entity registry and claim ledger alone do not carry the editorial visual intent needed to choose a template. Keep `claim.kind` and `visual_intent` separate.

### Revise the data plan

- Change “extract once for each segment at ingest” to **priority, document-aware extraction with caching**, followed by measured backfill.
- Allow unknown/ranged event dates and unresolved entities in a quarantine/review state; exclude them from hard graph joins until resolved.
- Treat paired events as hypothesis candidates; require stronger evidence for causality and motive.
- Use pattern queries as one discovery source. Preserve direct topic research and anomaly-led discovery.
- Make the stats checker return either `pass`, `pass_with_disclosed_limit`, `needs_research`, or `reject`. A caveat should appear in narration when material to understanding, not automatically become a separate beat every time.
- Define a small gold set with positives, adversarial negatives, and uncertain cases. Evaluate source support, relation precision, and story usability separately.

### Revise the matching plan

- Match at the **shot or visual-task** level, with explicit many-to-many links between narration spans and claims. Do not assume every claim equals one shot.
- Derive candidate jobs from claim semantics plus editorial visual intent; do not hard-map `claim.type` to one job.
- Give template specs hard constraints (slot count, kind, single-person rule, aspect ratio) and soft preferences (pace, motion, aesthetic, reveal style).
- Return two lists: **fillable now** and **possible after acquisition/adaptation**. Add an editor browse mode for all templates, including spatial scenes.
- Validate reason labels extracted from the 31 prose reviews before using them as ground truth; keep the original notes and a `miscellaneous/new reason` route.
- Optimize continuity across the sequence, but allow editorial override and explicitly account for scene transitions, pacing, and cost.

### Revise the media and infrastructure plan

- Pilot media kits for the highest-demand entities instead of committing to 150–300 artists.
- Keep suggested identity/classification separate from automated Production Ready promotion until calibrated false-match and misfile rates are acceptable.
- Index b-roll at shot level when the demand justifies it; measure transcription and shot-detection yield against human search time.
- Add a rights **use record** for every placement in a video, not only a one-time asset flag.
- Move checksum backups and a successful restore drill earlier. Scale rendering only after measuring actual render time, failure rate, and concurrent-work constraints.

### Revise the story-writer connection

- Output a linked script **and** Story IR.
- Treat blueprint targets as optional diagnostics. Approve the central thesis, factual support, audience clarity, and originality through independent review.
- Run a visual feasibility check on the story outline before full script lock; let missing assets trigger a research, rewrite, custom graphic, or sourcing decision.

## How I would update my earlier handoff

Keep its broader coverage of channel intelligence, editorial selection, rendering, QC, publishing, policy, and phased scale. Add the new handoff's specific integration mechanisms:

- A versioned entity-registry migration and crosswalk as Phase 0.
- A formal Story IR with narration spans, typed claims, visual intents, shot IDs, and continuity groups.
- A metrics-comparability checker with explicit outcomes and evidence tests.
- A two-pass media demand forecast: outline stage and shot-planning stage.
- Independent review records for media, templates, and final pairings.
- A sequence planner with deterministic replay, editorial overrides, and cost/continuity objectives.
- An explicit operating budget: model spend, review minutes, sourcing/clearance effort, storage, and render capacity per **publishable** video.

Do not replace the broader architecture with a narrower three-layer plan; the system's quality is determined at topic selection, editorial approval, final QC, and release as well as at the data/media seam.

## Revised build order I recommend

| Step | Deliverable | Evidence of completion |
|---|---|---|
| **1. Baseline one real video** | Collect its sources, graph outputs, claims, script, beats, matching review, media, and rough/final cut; freeze the 31-review matching sample | A reproducible failure map and current costs/time. |
| **2. Registry crosswalk + minimal IR** | Map the pilot's entities/cohorts/assets to IDs; link script spans, claims, and visual tasks | The pilot video can be represented without losing information or inventing IDs. |
| **3. Evidence and metric gate** | Claim receipts, contradiction search, metric comparability checker, uncertainty states | No unsupported pivotal claim in the pilot; known false links are rejected. |
| **4. Template/media feasibility** | Slot specs, two-list slate, typed sourcing requests, independent verdicts | Reviewed wrong-entity and unfillable examples have correct outcomes. |
| **5. Research discovery experiment** | Priority event extraction and several story-candidate generators | Measured relation precision, story yield, cost, and negative-control behavior. |
| **6. Sequence and production pilot** | Continuity planner, proactive media sourcing, render package, full-video QC | One publishable video and then 2–3/week for several weeks within an explicit human-time and cost budget. |
| **7. Reliability and scale** | Tested backups, recovery, queue/worker boundaries, workload-based capacity expansion | Stable pilot recovery and measured throughput before adding niches or daily-volume targets. |

Backup and restore work should begin during steps 1–2 if the current media/database are only on one machine; the table places scale infrastructure later, not basic data protection.

## Decisions to ask the team for

1. Provide one full project trace and the actual registry/cohort/graph/schema files so these recommendations can be tested against current code.
2. Set a maximum **model spend, human review time, and clearance effort per publishable video** for the pilot and for scaled production.
3. Choose the review authority for factual claims, contested allegations, visual identity, and rights decisions.
4. Confirm the renderer/template inventory and distinguish 445 pool records from distinct templates and render implementations.
5. Decide whether the first pilot optimizes commissioned-story completion, discovery of new stories, or matching repair; use the same IR to support all three over time.

## Immediate next step

Take one already reviewed rap documentary and encode **ten difficult visual tasks** plus its pivotal claims in the proposed registry and IR. Include a cohort, a metric comparison, an implied subject, b-roll, and a continuity run. Run the current matcher and the revised feasibility logic side by side. Have the editor judge the resulting claims and visual options blind to which system produced them. That experiment will show which structural changes truly remove work, and which merely move it to another layer.
