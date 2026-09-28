# Handoff: data, matching and media layers

**Date:** 2026-09-27
**Scope:** the data layer, the matching layer and the media layer only. The story writer is covered only where it connects to them.

**Sources read:**
- `djtoler/content-project-mgr/issues_2026-09-27`
- `Polish/hiphop-research-engine/issues_data_layer.md`
- `automation-data/GAPS.md`
- `astra-visual-selector/grammar/issues_matching_layer.json`, plus `JOBS.md`, `GRAMMAR-v2.md` and `SCOPE.md`
- `Polish/issues_media_layer.md`
- This repo's `youtube_doc_analysis/synthesis/` (the story writer's structure library)

**Status:** architectural recommendations. None of this has been built or measured.

---

## 0. The one structural change

Today each layer passes loosely typed text to the next: chunks to the writer, beats to the matcher, entity lists to media. Every issue listed in the four documents is a symptom of that:
- chunks related only because they share words;
- Drake merged into all 40 beats;
- "ninety-three rappers" resolving to nobody;
- one job per beat;
- templates offered that no available media can fill.

The fix is two shared contracts that every layer reads and writes.

1. **A canonical entity registry.** One ID per artist, label, song, album, person and organization. It includes aliases, Wikidata, MusicBrainz and Spotify IDs, face-cluster IDs and cohort memberships (for example, the XXL class of 2010 maps to its 11 member IDs).
   - The data layer binds events to these IDs.
   - The matcher resolves "the 2010 class" to member IDs.
   - Media tags and faces point at the same IDs.
   - Today three separate lists exist: `entity-roster.json` (297 names), the cohort CSVs and the face clusters.
2. **A claim ledger (the story contract).** The story writer never hands off prose. It hands off beats, and each beat holds typed claims.
   - Example claim: `{claim_id, type, subject_ids[], object_ids[], value, unit, basis, time_range, comparison, source_receipts[], caveats[], confidence}`.
   - The claim `type` is chosen from a closed list that deliberately mirrors the matcher's communication jobs (`one_vs_aggregate`, `entity_vs_benchmark`, `proportion_of_cohort`, `narrate_an_event`, and so on).
   - With typed claims, choosing a job becomes a lookup instead of a paid classification step, and a beat with two claims naturally has two jobs (PI-05).

```
data layer ──(verified events + metrics, keyed by entity ID)──▶ story writer
story writer ──(Story IR: beats → claims → entity IDs, roles, timing)──▶ matching
matching ──(template choice + typed media briefs)──▶ media
media ──(assets keyed by entity ID + kind + attributes)──▶ matching / render
```

---

## 1. Data layer

### Feedback

- **What works:** retrieval, receipts, cost limits, hop limits, and abstaining on negative controls. Keep all of it.
- **What doesn't:** the engine invents relationships at query time from keyword co-occurrence. Its hypothesis templates then turn those weak matches into specific motives, which is how "clean up Future's image" happened.
- **Root cause:** events are never pulled out into structured records bound to an entity and a time, so the graph connects text chunks instead of facts.
- **The stats side is in good shape.** GAPS.md is an excellent contract, but it is prose. The same rules need to be machine-enforced.

### Plan

1. **Entity registry first.** Seed it from the cohort CSVs, the discography data and Wikidata.
   - Resolve aliases (Curren$y, Nicki Minaj and so on) with deterministic rules plus human review of collisions.
   - This fixes issues in all three layers.
2. **Extract structured events once, when content is ingested, not at query time.**
   - For each segment, extract `{event_type, actor_ids, target_ids, date|date_range, polarity, quote_span, source_id}` and store it in Postgres next to the vectors.
   - This is a one-time model run per segment. Run it on the ~9.7k source documents in priority order, starting with the rap entities the channel will cover first.
   - Validate every extraction against a JSON Schema, the same discipline this repo uses for its analyses. Reject any event that has no date or no resolved actor.
3. **Relationships only from paired events.**
   - "Conflict", "incentive" and "pressure" become derived edges. Each requires two or more events with resolved actors, a time ordering and explicit polarity, never a keyword match.
   - Every edge carries its evidence event IDs, so any edge can be traced back to its sources.
4. **Find stories by pattern.** Turn each blueprint and signature in `synthesis/pattern_library.json` into an evidence query over the event graph. For example:
   - **Acceptance Treadmill:** entity X has three or more (milestone → rejection → response) triples, in time order.
   - **Vindication Ledger:** a claim by X at time t1, and confirming evidence from an independent source at t2 > t1.
   - **Contested Ranking:** four or more entities, where two or more metrics disagree on the leader.
   - **Worst Case First / Downfall:** a peak event followed by a cascade of negative events that each have their own receipts.
   - An idea supplied as a topic runs the same queries, restricted to that topic's entities.
   - A pattern whose required evidence is incomplete does not generate a hypothesis. It abstains, and the missing pieces become targeted follow-up searches for the deep research service.
5. **Machine-enforced stats contract.**
   - Build the master metrics table (GAPS #10), keyed by entity ID.
   - Every metric gets comparability metadata: `basis` (RIAA units / Spotify streams / iTunes rank), `valid_era`, `coverage`, `not_comparable_with`.
   - A claim checker runs on the Story IR and rejects, or forces a stated caveat on, claims that break GAPS rules. Examples: comparing Spotify totals across eras before about 2015, mixing iTunes rank with stream counts, feature share with no stated basis, Grammy counts without a receipt.
   - Each caveat GAPS requires becomes a line of narration: a disclosed limitation is a beat.
6. **The deep research service writes back.** Grounded findings are stored as events with receipts, after passing the same schema and entity binding. Otherwise every run starts cold.
7. **Tests that check the story, not just the stages.** Keep a small gold set, 20–30 known true connections and 20–30 known false ones. Include the Future case as a permanent negative control, and track precision and recall on every change.

---

## 2. Matching layer

### Feedback

- **The foundation is right:** binding templates to 20 domain-independent jobs, rotating within each job's templates, rules produced by a pipeline rather than by hand, and scope restrictions. The job set ports across niches, which is the key to expanding.
- **Most issues come from what goes in, not the grammar.**
  - PI-01, PI-02 and PI-05 come from a beat format with no per-claim entities and no cohort expansion.
  - PI-03, PI-07 and PI-08 come from templates without machine-readable requirements.
  - PI-09 comes from choosing templates one beat at a time.
- **Make the unit of matching the claim, which is roughly a shot, not the beat.**

### Plan

1. **Take the Story IR as input.**
   - The job is derived from the claim type, so there's no paid re-classification.
   - Entities come from the claim's IDs. A beat-level `_subject` is used only when the claim marks it as an implied subject. That fixes PI-01 while keeping beat 01-01 correct.
   - Cohort labels expand through the registry, which fixes PI-02.
2. **Give every template a requirements spec, in the same style as `media-kind-rules.json`:**
   - slot count, minimum and maximum entities;
   - media kind per slot, and whether a slot requires a single person (PI-08);
   - era spread or distinct years (24-24);
   - text length limits, duration range and aspect ratio.
3. **Check feasibility before offering a template.** For each candidate template, check whether the media library can satisfy its spec for this claim's entities.
   - If it can, offer it.
   - If it can't, still show it, marked unfillable. Emit a typed media brief such as `{entity_ids, kind, count, era_spread, framing}` to the media layer's sourcing queue (PI-07). That turns stalled beats into concrete requests.
4. **Routing rules:** 20 or more entities, or any comparative intent, means offer all spatial templates (PI-03, the rule you gave). Re-bind the 75 unbound pool records before any re-binding run (PI-04, then PI-06, in the dependency order the issues file already states).
5. **Plan the whole sequence** after picking per claim. A dynamic-programming pass across the video's claims adds:
   - **continuity runs:** the same template carries across consecutive claims when they share a treatment (PI-09);
   - **"mandatory" markers,** which the user can override explicitly;
   - **rotation and variety limits** outside those runs;
   - **fixed tie-breaks**, so the same Story IR always produces the same edit decision list.
6. **Record media and template verdicts separately.** A media verdict like "right media, no template" is stored by itself (PI-10).
7. **Measure from the review notes, don't ask for scores (PI-11).**
   - Turn the prose notes into a fixed set of reasons, automatically:
     - wrong entity
     - missing cohort
     - needs a second template
     - needs b-roll
     - unfillable
     - continuity
     - ugly
   - Track the share of claims accepted on the first slate, and review minutes per video.
8. **Use the storytelling structure (this repo).** Each Story IR beat carries `beat_role`, `retention_function` and `device` from the analysis schema.
   - The matcher can use them as tie-breakers only, never as the main signal. A reveal can prefer a template that builds up before showing its value; a hook can prefer motion-heavy templates.
   - This keeps storytelling separate from visual intent, as you decided.

---

## 3. Media layer

### Feedback

- **The gating is right:** exception-driven automation, lifecycle gates, run receipts and never guessing an identity.
- **The problem is that supply is reactive.** Media arrives from saved folders and ad-hoc searches, and the matcher discovers shortfalls during review, as with 07-07, 24-24 and the b-roll beats.
- **Rendering and storage run on one Mac.** That caps throughput well below 5–10 videos a day.

### Plan

1. **Source on demand.** The sourcing queue is fed by the matcher's typed media briefs and by a pre-script check: once the Story IR exists, list every entity × kind the video will need before review starts.
2. **Per-artist media kits.**
   - For the top roughly 150–300 rap entities in the registry, maintain a standing kit: 3+ solo portraits across eras, a cutout and glow version, album and single covers, 2+ performance b-roll clips, and 1+ interview clip.
   - At 2–3 videos a week, kits make sourcing reusable across videos and reduce each video's sourcing to exceptions.
3. **Identity by agreement between signals.** Auto-accept an identity only when two or more independent signals agree on the same registry ID:
   - the face cluster;
   - a caption or OCR entity;
   - the source context, such as the artist's own account or an article about them.
   Calibrate a face threshold per identity on labeled data, and make the false-match test part of the gate. Everything else stays a suggestion, as it is now.
4. **Classification:**
   - Keep 65% top-1 accuracy as a ranking signal. Auto-file only when there is a clear margin over the second choice and the result agrees with the source metadata.
   - Everything else goes to the review queue. Track the queue size per video.
5. **Video understanding:** run automatic transcription and shot detection (for example Whisper and PySceneDetect) on b-roll when it's ingested.
   - This gives b-roll searchable entities and "performance", "interview" or "crowd" tags, which the b-roll beats need (PI-12).
6. **Infrastructure:**
   - A durable job queue (a Postgres-backed queue is enough).
   - Object storage mirrored with checksums.
   - Mac-only steps (the Apple face and cutout pieces) isolated behind worker interfaces, so they can be replaced or run on more machines.
   - Rendering through nexrender or aerender workers fed by the edit decision list.
7. **Rights metadata on every asset:** source, license basis, date sourced and whether it's safe to use in a monetized video. See the questions below. This gates Production Ready alongside quality.

---

## 4. How the story writer (this repo) plugs in

1. **Structure selection:** the writer picks a blueprint from `synthesis/pattern_library.json`. The data layer's pattern queries (section 1, step 4) supply candidate stories along with the evidence that fills each blueprint beat.
2. **Output:** Story IR, meaning beats (`beat_role`, `target_pct`, loops opened and closed, device) containing claims (typed, entity IDs, receipts).
   - It is validated against a JSON Schema, using the same validator discipline as `youtube_doc_analysis/tools/validate.py`.
3. **Structural check on generated scripts.** Run the same analysis prompt and schema on the system's own scripts, then compare the result to the blueprint targets, for example:
   - hook within the first ~1% of runtime;
   - central question paid off at around 96%;
   - a re-hook roughly every 12%;
   - the close calls back to the opening.
   The prompt that analyzed 24 top videos becomes the QA gate for our own output.
4. **Fact gate:** every claim must have a receipt, and the stats-contract checker must pass before anything reaches matching.

---

## 5. Build order

Each step unblocks the next.

1. **Entity registry**, plus cohort expansion. This unblocks PI-01, PI-02, media identity and event binding.
2. **Claim ledger and Story IR schema**, plus the stats-contract checker.
3. **Template requirements specs**, the feasibility check and typed media briefs (PI-07, PI-08, PI-10).
4. **Event extraction at ingest** for priority entities, and edges built only from paired events.
5. **Pattern-first story discovery** from the pattern library, with a gold set and precision/recall tracking.
6. **Sequence-level matching** (continuity runs), plus measurement from review notes.
7. **Media kits, identity by agreement, and ingest-time b-roll processing.**
8. **Job queue, storage mirror and render workers.** Scale from 2–3 videos a week toward 5–10 a day.

**Metrics that decide whether the system is ready for more volume:**
- human review minutes per video;
- share of claims accepted on the first slate;
- share of claims with a verified receipt;
- precision on the connection gold set;
- sourcing requests per video.

---

## 6. Open questions

### Cross-cutting
1. **Model budget:** earlier the plan was no LLM API calls at 20 videos a day. What is the budget per video now, and is a one-time model run to extract events from the corpus acceptable?
2. **Human time:** how many review minutes per video are acceptable at 2–3 a week, and at 5–10 a day?
3. **Existing IDs:** does any canonical entity ID exist yet, or is `entity-roster.json` the closest thing?

### Data
4. **Story discovery:** should the system start from the anomaly worklist, from the pattern-library queries, or from both?
5. **Research write-back:** does the deep research service write findings back to the corpus today, with receipts?
6. **Fact approval:** who signs off on facts before narration? Is a receipt enough on its own?

### Matching
7. **Template count:** there are 445 pool records, 75 of them unbound, versus the "50 templates" mentioned earlier. What's the real number of distinct templates, and how many are AE versus Remotion or other?
8. **Paid re-classification:** is that an LLM call? With typed claims it may become unnecessary.
9. **Continuity rules:** should they come from you as explicit rules, or be learned from review decisions?

10. **B-roll sources:** where does performance and interview footage come from?
11. **Infrastructure budget:** is there a budget for cloud GPUs and storage, or must everything stay local?
