# Documentary production system: architecture handoff

**Date:** 2026-09-27  
**Initial niche:** rap music  
**Pilot output:** 2–3 documentary videos per week  
**Longer-term ambition:** 5–10 high-quality videos per day across niches

## Executive decision

Build a **claim-centered production system**, not a single autonomous writer. The central unit is a sourced claim that can become a story beat and then a visual instruction. Each stage should pass a typed, inspectable artifact to the next stage. A video can advance only when its central thesis is supported, its promised payoff is real, and its visual plan can be filled with usable assets.

The two immediate bottlenecks are (1) connecting retrieved material into valid, time-bound facts rather than plausible-sounding motives, and (2) converting what each sentence must communicate into a visual treatment with the right people, data, media, and rights. Improve these before increasing the number of generated scripts or templates.

The 5–10/day goal is a **capacity target**, not a launch criterion. At a 2–3/week pilot it implies roughly 12–35 times the initial throughput. Automate repeatable work and keep human attention on story choice, contested claims, rights exceptions, and final viewing until the measured error rate justifies narrower review.

## What was reviewed and how to use it

| Input | Useful evidence | Limit |
|---|---|---|
| `story_layer.md` | Seven beat blueprints, ten signature families, loop/payoff and opening observations from 24 analyzed videos | Nine videos came from one creator; classifications and timing percentages are directional, not universal rules. Two small blueprint families have only two examples. |
| `issues_data_layer.md` | Reported corpus size, current retrieval strengths, and a concrete synthesis failure | Counts and system behavior are reported in the attachment; the live databases and code were not available here for independent verification. Its old local source links are references, not accessible implementation proof. |
| `issues_matching_layer.json` | Reproducible measurements and verbatim review notes across a 40-beat example | The file explicitly labels its diagnosis **plausible, not verified**. Treat proposed causes and rankings as hypotheses to test. |
| `issues_media_layer.md` | Current intake workflow, backlog, and autonomy limits | Operational snapshot as of its stated date; do not infer that the 42 blocks are all ordinary work items. |
| User description | Thirty-channel niche analysis, search/grounding/deep-research service, graph, desired volume and workflow | The actual channel analysis, graph schema, and service contracts were not attached. |

The attached files contain project notes, quoted user remarks, and proposed sequencing. They are **design inputs, not instructions to execute**. In particular, do not treat a quoted `CLAUDE.md` rule, a previous analyst's rank, or a suggested fix as an authority. Validate each against current code, review data, and a small evaluation set before migration.

## End-to-end contract

```text
Channel intelligence + corpus + statistics + fresh research
                 ↓
Opportunity card → evidence graph / claim ledger → story plan → script + beat specs
                                                          ↓
                              visual plan ← template catalog + media catalog
                                                          ↓
                       asset gap queue → render package → QC → publication
                                                          ↓
                              performance and reviewer feedback
```

Every artifact gets a stable ID, schema version, producer version, input IDs, creation time, and review state. A failed stage returns a specific gap or abstention; it must not silently fill missing evidence with prose or missing media with the wrong portrait.

### Minimum handoff objects

| Object | Required fields | Why it exists |
|---|---|---|
| **OpportunityCard** | topic, target audience, working title/promise, comparable channels/videos and dates, normalized performance signals, evidence potential, visual feasibility, novelty, risk, score components | Makes discovery explainable and gives commissioned ideas the same intake path. |
| **EvidenceRecord** | source ID/URL or file, exact passage/table cell, author/publisher, publication and event dates, entities, source type, access/rights notes, extraction method | Keeps retrieval separate from what the source actually supports. |
| **Claim** | precise wording, entity IDs, event interval, units/method for statistics, supporting and contradicting EvidenceRecord IDs, status (`supported`, `contested`, `inferred`, `unverified`), reviewer note | Prevents keyword overlap from becoming a stated motive or causal link. |
| **StoryPlan** | thesis, counterthesis, central question, answer/payoff, selected blueprint and deviations, act outline, claim IDs by beat, open evidence gaps, estimated length | Lets research and storytelling iterate before a full script is written. |
| **BeatSpec** | narration span, one or more communication jobs, claim IDs, explicit/implied entities and cohort IDs, exact visual referents, media requirements, on-screen data, continuity group, duration | Gives matching enough information to fulfill the sentence, not just the topic. |
| **VisualPlan** | candidate treatments with rationale, template version, slot-to-entity mapping, media IDs, acquisition requests, eligibility failures, rights state, reviewer selection | Makes a proposed scene renderable and reviewable. |
| **RenderReceipt** | script/voice/asset/template versions, timeline, provenance and licenses, QC results, upload settings, final approval | Enables reproducible fixes, rollback, and audits. |

Use a shared ID registry for people, organizations, songs, albums, dates, events, videos, source documents, cohorts, and assets. Keep the source text and raw numeric data alongside derived labels. Entity aliases must be explicit (for example, stage names and spelling variants); identity uncertainty is an output, not a reason to choose the closest known person.

## Layer plans

### 1. Channel intelligence and topic selection

**Current asset:** the roughly 30-channel analysis described by the user. Ingest it as dated observations, not as a static list of winning title formulas. Preserve video URL, channel, publish date, video age at measurement, views, subscriber baseline where available, runtime, title, topic labels, format, and any manually assigned quality/novelty labels. Record how each ratio was calculated.

**Build:** generate OpportunityCards by combining channel outliers, unmet topic clusters, corpus anomalies, graph connections, and direct editorial prompts. Normalize breakout measures for video age and channel baseline; compare within comparable formats and durations. Add penalties for crowded topics, stale data, weak sourcing, and asset scarcity. Keep score components visible. Titles are hypotheses about a promise; a strong title never authorizes an unsupported story.

**Gate:** an editor chooses the weekly slate from scored cards. For the pilot, require a clear answerable question, a plausible original angle, source paths, and a preliminary visual inventory. Evaluate scoring on held-out later videos, not on the same channel sample used to design it. Track whether chosen ideas become publishable stories, not only whether they resemble past breakouts.

### 2. Data, research, and evidence graph

**Current asset:** reported 770,248 segment vectors from 9,701 documents; 100 CSV files with 400,013 rows including snapshots and derived tables; semantic retrieval, BM25, source tracing, cost and hop limits. These are substantial research capabilities, but the attachment reports that relationship labels and story hypotheses still overreach.

**Build:** separate five operations:

1. **Retrieve:** hybrid semantic/lexical/structured search with document-level diversity, date filters, entity filters, and query plans generated from the story question. Return passages and exact table rows, not just similarity scores.
2. **Resolve:** bind each assertion to the correct person, organization, work, place, and event interval. Store aliases, role, and temporal validity. Deduplicate overlapping CSV records and keep source-of-truth and derivation lineage.
3. **Extract:** propose typed events/relations from a source, each with its exact evidence span. The graph should distinguish an observed relation (`released`, `signed`, `charted`, `sued`) from interpretations (`pressured`, `benefited`, `caused`).
4. **Verify:** corroborate important claims, seek disconfirming evidence, check chronology and numeric methods, and label inference explicitly. A Google-grounded answer is a lead; the underlying primary/credible source and its passage become evidence. Preserve search query, date, and citation trail.
5. **Synthesize:** create candidate tensions, reversals, mechanisms, and unanswered questions only from verified claim sets. Do not produce motive, conflict, or causal hypotheses from keyword co-occurrence alone. When evidence is insufficient, produce a research task or abstain.

The graph is the **join and reasoning surface**, not a claim of truth by itself. It should support typed paths such as `artist → release → chart measurement → peer comparison → later event`, with each edge linked to evidence and time. Keep speculative edges in a separate namespace/state so they cannot be rendered as narration without review.

**Gate:** a ClaimLedger for the proposed story. High-impact or contested claims require independent support and an editor-visible counterevidence search. Statistical claims require cohort definition, denominator, time range, source table, transformation, and reproducible calculation. Do not count vector count as evidence quality; measure precision of retrieved support and accuracy of extracted relations.

### 3. Story discovery and commissioned-story writing

Run the same workflow in two modes: **discovery** (data proposes a story) and **commissioned** (a topic/title/question is supplied). Both produce an OpportunityCard, research plan, ClaimLedger, StoryPlan, script, and BeatSpecs.

The writer should first make several candidate **story centers**: a question, a defensible answer, the tension that makes the answer interesting, and the claims that could prove or refute it. Rank by evidence, originality, narrative movement, audience relevance, and visual feasibility. If the attractive center rests on weak causation, either research it, frame it as a question with honest limits, or choose another center.

Use the attached seven blueprints and ten signature families as a **planning library**, not a fixed script generator. A plan may choose one primary arc and a few supporting devices, with explicit deviations. Require the opening promise to be paid or honestly reframed, meaningful escalation, a real opposing interpretation, and a close that resolves the central question. The attachment's 13% act-one and 12–13% re-hook intervals are review prompts, not forced timestamps. Sponsor position and CTA are business decisions, not narrative defaults.

Draft in two passes: (a) argument and beat map, checked against claims; (b) voice and pacing, checked against audience understanding and originality. Each factual sentence points to a claim; each unsupported flourish is marked as interpretation or removed. Each beat has one or more communication jobs (for example, define a metric, compare a cohort, show a reversal) and visual referents. The writer and visual planner loop before lock: if a pivotal beat cannot be shown or sourced, revise the beat rather than attach irrelevant media.

**Gate:** story editor approves thesis, promise/payoff, factual framing, and a read-through before voice generation. Maintain a red-team pass for accusations, motives, contested allegations, and chronology. A fluent script is not evidence that its argument is sound.

### 4. Beat-to-template and media matching

Replace `beat → one job → eligible templates → generic media` with `beat span → multiple jobs + referents → scene constraints → viable templates + eligible assets`. Some beats should split into sentence-sized sub-beats; others should share a treatment across several beats. The unit is the **visual communication task**, not the beat number.

**Recommended issue sequence, to validate against current code:**

1. Create a compact evaluation set from the 31 reviewed records. Convert prose notes into explicit expected referents, rejected pairs, wanted treatments, asset gaps, and acceptable alternatives. Preserve the original notes. This addresses PI-11 without asking the reviewer for scores they did not use.
2. Fix entity scope (PI-01) and cohort expansion (PI-02). `_subject: Drake` should be a contextual candidate, not an unconditional beat entity. Resolve implied subjects from discourse context; expand groups from a versioned cohort definition and distinguish all members from the subset actually shown.
3. Add scene slot requirements and media eligibility (PI-07/08/10/12): number and type of subjects, group-photo eligibility, era, aspect ratio, artifact type, required b-roll/action, and whether media can be approved independently of a template. Emit asset-gap requests with named entities and needed media kinds.
4. Allow multiple jobs and sentence/sub-beat boundaries (PI-05), then make treatment continuity explicit (PI-09). A selected treatment can persist across a run unless a deliberate cut or communication need changes it.
5. Audit unreachable catalog items (PI-04); correct bindings and add feasibility-based discovery of spatial treatments for large or comparative cohorts (PI-03). Do not expose every spatial template blindly if its slots cannot be filled.
6. Rebind and rerank templates after the schema changes (PI-06). Show a small set of **fillable** options plus explicit missing-asset options, with reasons. A rejected option should stay rejected for equivalent future contexts unless the relevant constraint changed.

**Gate:** on the held-out beat set, track entity precision/recall, cohort coverage, valid template options, slot fill rate, asset relevance, continuity, and how often the editor can accept a pairing without rework. An empty slate with a precise acquisition request is a correct outcome; an attractive but impossible slate is not.

### 5. Media acquisition, library, and treatment

**Current asset:** the reported pipeline already ingests, fingerprints, probes, classifies provisionally, generates derivatives, reviews exceptions, and promotes through a production-ready gate. Preserve its canonical asset IDs and receipts. The attached audit reports 575 passing and 42 blocked transitions: 33 incomplete tag reviews, three deliberately rejected cutouts, and six candidates with no accepted derivative. Resolve the nine treatment dispositions explicitly; do not silently approve them.

**Build:** make the media catalog answer the BeatSpec, not just artist-name search. Add machine-readable fields for depicted entities and confidence, number of people, event/era, album/song/artifact, action, location, shot scale, visual quality, orientation, duration, audio content, provenance, acquisition path, usage terms, license/permission status, and permitted treatments. Keep uncertain tags as suggestions. A single-person spatial slot cannot use a group photo merely because the target appears in it.

Drive acquisition from **specific visual gaps**: `Curren$y album-cover set`, `seven members of the 2010 cohort as individual portraits`, `deluxe reissue artifacts`, or `performance b-roll for opening`, with minimum count and era constraints. Prioritize recurring gaps across approved slates. Support purpose-made charts, maps, typographic evidence, and licensed original graphics so every beat is not dependent on scraped artist imagery.

Keep the existing exception-review logic for identity, subject selection, classification, tags, and cutout quality. Calibrate the reported 65% exact-primary classifier and face similarity scores before any automatic irreversible assignment. Add shot-level transcript/scene indexing for video when it materially improves b-roll search. Move canonical files and metadata to backed-up storage with a restore drill before distributed rendering; a cloud mirror without a tested restore is insufficient.

**Gate:** only assets with known provenance, usable technical quality, correct subject, compatible treatment, and a recorded rights decision enter a final RenderReceipt. For uncertain rights, route to human clearance or replace the asset.

### 6. Audio, render, final QC, and publication

Make a render package from locked script, BeatSpecs, VisualPlan, voice track, music/sound cues, captions, title/thumbnail, descriptions, and source/rights ledger. Template renderers should be deterministic and parameterized, with manual override paths for the few scenes that carry the story. Use timeline-level IDs so a corrected claim or asset triggers only affected scenes and a new receipt.

Automated QC checks: missing/duplicate assets, wrong entity or era tags, broken text, caption alignment, audio loudness/peaks, black frames, clipping, aspect ratio, source overlays, timing, rights status, and title-to-payoff consistency. Human QC watches the **entire final export** at pilot scale, especially the first minute, every reveal, contested claim, and ending. Upload as a draft/private item for platform checks and approval; publish only after editorial, rights, and technical sign-off. Retain versioned source packages for correction or takedown.

**Gate:** no scheduled publication from a merely successful render. Publication requires an approved final export and a record of who approved it.

### 7. Orchestration, observability, and learning

Use a durable workflow engine/queue with idempotent stages, retries, dead-letter/exception queues, budgets, and resumable receipts. Each video has a state machine: `candidate → researching → evidence-ready → story-approved → visually-feasible → render-ready → QC-approved → published`, with `needs-research`, `needs-assets`, `needs-clearance`, and `rejected` branches. An editor sees only the unresolved decisions and the evidence behind them.

Track cost and latency **per publishable video**, not per generated idea. Log model/prompt versions, retrieval queries, evidence paths, claim changes, template choices, asset substitutions, reviewer decisions, and final performance. Build a feedback loop from corrections and viewer retention, but do not train the system to optimize retention at the expense of factuality or distinctiveness. Add niche-specific adapters for entity types, source hierarchies, data definitions, templates, and rights patterns; keep core contracts common so later niches do not require a rebuild.

## Evaluation and rollout

These are proposed release gates, not measured current performance.

| Phase | Scope | Evidence required to advance |
|---|---|---|
| **0. Baseline and contracts** | Freeze current 31-review matching sample; collect 10–15 real story cases (good, weak, negative controls); inventory the 30-channel analysis and rights status | Reproducible baseline, schema definitions, named owners, and a versioned gold set with real reviewer judgments. |
| **1. Story kernel** | Build ClaimLedger and two-way data/story research loop; test on 3–5 rap stories | No unsupported pivotal factual claim in reviewed outputs; negative controls abstain; editors can trace every central claim to source passages and calculations. |
| **2. Visual kernel** | Repair entity/cohort scope, slot requirements, catalog reachability, continuity, and asset-gap generation | Gold-set pairings improve on baseline; no known wrong-entity or unfillable selected treatment; asset requests are specific enough to source. |
| **3. Pilot production** | Produce 2–3/week through full render and human final QC for several consecutive weeks | Stable delivery, bounded rework/cost, reliable correction path, rights decisions on every used asset, and editor acceptance of story and visuals. |
| **4. Controlled scale** | Increase throughput only where measured failure rates and staffing allow | Capacity, quality, originality, rights, and audience outcomes hold across more than one topic family. Add niches one at a time via adapters and separate evaluations. |

Suggested dashboard: opportunity-to-approved-story conversion; factual corrections per video and severity; retrieval precision for pivotal claims; unsupported inference rate; beat visual acceptance; media gap/reuse rate; edit minutes per finished minute; rights exceptions; render failures; total production cost and cycle time; first-minute and mid-video retention; viewer satisfaction signals; published-video diversity. Define thresholds from the pilot baseline instead of inventing accuracy percentages now.

## Important feedback

- **Your data advantage is real only if claims are inspectable.** The large vector corpus and CSV collection can discover uncommon comparisons, but a weak entity join or ambiguous denominator can manufacture a convincing false story. Put verification and abstention ahead of more autonomous hypothesis generation.
- **The writer and visual agent need an iterative contract.** A finished script handed downstream is too late to discover that its decisive scene needs 93 distinct artist assets or a chart that does not exist. Lock story and visual feasibility together.
- **Treat the playbook as editorial craft evidence.** The 24-video sample supports useful questions about hooks, loops, and payoffs; it does not justify stamping every video with the same timing or arc. The channel analysis should help find audience demand, while each documentary still needs its own researched point of view.
- **Automation should reduce decision volume, not erase judgment.** At pilot scale, the reviewer should spend time on the central claim, story shape, and final film. Intake, search, deduplication, calculations, slate preparation, assembly, and mechanical QC are better automation targets.

- **Synthetic realism needs a release decision.** YouTube currently requires disclosure when AI meaningfully alters or generates realistic content, including making a real person appear to say or do something they did not. Store this decision with each asset and in the upload checklist. Sensitive or accusatory topics also need careful factual framing and ad-suitability review. [YouTube AI disclosure guidance](https://support.google.com/youtube/answer/14328491), [advertiser-friendly guidance](https://support.google.com/youtube/answer/6162278).

## Follow-up questions, in priority order

1. **Can you provide the 30-channel analysis and one complete recent project trace** (idea → sources/graph → story/script → 40 BeatSpecs → matching slate → selected media → final/rough cut)? This is the fastest way to set a real baseline and identify the exact integration points.
2. **What is the current graph schema and which facts are authoritative?** Specifically: entity IDs, typed edges, temporal qualifiers, provenance, CSV lineage, and whether inferred relationships are already stored separately from observed ones.
3. **What is the editorial promise of the rap channel?** Is it investigative, data-led, biography, music criticism, industry/business, or a mixture? Who has final authority over controversial claims and story choice?
4. **What rights do you already hold for music, performance clips, photographs, articles, interviews, and generated likenesses?** Is the intended default licensed media, cleared fair-use analysis with counsel, original graphics, or a combination?
5. **What does “high quality” mean operationally for your first 10 releases?** Target length, voice style, visual density, acceptable manual edit time, and the two or three reference videos you would be proud to match are more useful than a single score.
6. **What software and operating constraints are fixed?** Existing repositories/services, graph/vector/CSV stores, renderer, Mac-dependent steps, cloud budget, preferred review UI, and whether upload/publish must remain manual.
7. **Which output should be implemented first:** story discovery from the corpus, commissioned-topic research and scripting, or repair of the existing 40-beat visual matching example? My recommendation is to baseline all three, then implement the claim ledger and visual contract on one commissioned story end to end.

## First implementation slice

Use **one previously reviewed rap topic** and its existing sources, script, and media pool. Produce a versioned OpportunityCard, 20–40 verified Claims, one StoryPlan, BeatSpecs for the whole script, and VisualPlans for 10 representative beats (including a cohort, a data chart, an implied subject, a missing b-roll case, and a continuity run). Have the editor mark factual and visual failures. Fix those contracts, then render one complete video. This slice tests the architecture at the point where today's systems actually meet, without requiring a full platform rebuild.
