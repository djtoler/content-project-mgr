# Comparison: `documentary_system_handoff.md` vs `HANDOFF_data_matching_media.md`

**Date:** 2026-09-27

**The two documents:**
- **Theirs:** `documentary_system_handoff.md`, the uploaded end-to-end architecture handoff.
- **Mine:** `architecture/HANDOFF_data_matching_media.md`, the data, matching and media handoff written earlier in this session.

**Scope difference.** Mine was deliberately limited to three layers. Theirs covers the whole pipeline: topic selection through publication and learning. Some of the "misses" below are only scope. I label each one as a real miss or scope, so the difference is clear.

---

## 1. Verdict

**Use theirs as the master architecture, and use mine as the implementation detail for three layers.**

**What theirs does better:**
- Contracts at every stage.
- Gated, phased rollout.
- A test of every stage on one real project before building the platform.
- Human judgment placed where it matters most.

**What mine does better:**
- Concrete mechanisms at the points where the layers meet:
  - claim types that line up with the matching jobs;
  - story blueprints turned into evidence queries;
  - GAPS.md turned into a checker;
  - per-artist media kits;
  - identity accepted only when independent signals agree.
- It is the only one of the two that says how this repo's story library actually connects to the data layer.

Neither is complete without the other.

---

## 2. Where we agree

Both of us reached these independently, so they're the safest decisions:

| Topic | Both documents say |
|---|---|
| Core unit | A sourced, typed claim, passed between stages as an inspectable artifact |
| Entity registry | One shared ID registry, explicit aliases, and uncertainty kept as an output rather than resolved to the nearest match |
| Data layer failure | Keyword co-occurrence is being turned into motives. Relationships must be bound to entities and time, and the system should abstain when evidence is thin. |
| Matching | Several jobs per beat; implied subjects vs explicit ones (PI-01); versioned cohort expansion (PI-02); slot requirements and a feasibility check; typed media gap requests; continuity runs; media verdicts stored apart from template choice |
| Measurement | Build the evaluation set from the 31 prose reviews; don't ask for 1–5 scores (PI-11) |
| Media | Keep the review-only-exceptions design and the lifecycle gates. Classifier and face scores are suggestions until calibrated. Move to backed-up storage before distributing work. |
| Stats | Every statistical claim carries its cohort, denominator, time range, source and method |
| Deep research | A grounded answer is a lead. The underlying source passage is the evidence. |

---

## 3. What theirs showed me I missed

### Real misses (these should change my handoff)

1. **The writer and visual planner must iterate before the script is locked.**
   - My flow ran one way: story, then matching, then media. An unfillable template produced a media brief but never went back to the writer.
   - Theirs is right: if a pivotal beat can't be shown or sourced, *rewrite the beat* instead of attaching irrelevant media. Checking story and visual feasibility together is a better contract than a media shortfall surfacing at review time.
   - This is the most important thing I missed.
2. **Counter-evidence and claim status.**
   - Mine had `confidence` and `caveats`.
   - Theirs requires links to contradicting evidence, a status (`supported`, `contested`, `inferred` or `unverified`), a counter-evidence search the editor can see for high-impact claims, and a red-team pass for accusations and motives.
   - For the kind of claims these videos make, such as "Jay-Z's plan to destroy Drake" or the Ellen exposé, that's essential.
3. **Observed facts vs interpretations as separate stores.**
   - I required interpretive links ("conflict", "incentive") to be built only from paired events. Theirs goes further: speculative edges live in a separate namespace and *cannot be narrated* without review. It's cleaner and safer.
4. **YouTube monetization risk from reused or mass-produced content.**
   - A system built on templates, aimed at 5–10 videos a day, is exactly the profile that guidance targets. I treated rights as a per-asset copyright question. It's also a question at the channel level: how original each video is.
   - This affects how much the templates should vary and why each video needs its own point of view.
   - I haven't checked the linked policy pages myself. Verify their current wording before relying on it.
5. **AI disclosure for realistic synthetic media.** This is a per-asset release decision, stored with the asset and checked at upload.
6. **Treating my own playbook as rules.**
   - My section 4.3 proposed checking scripts against blueprint targets: hook at 1% of runtime, re-hooks about every 12%, act one ending near 13%.
   - Theirs correctly says those are review prompts, not required timestamps, and that sponsor placement and CTAs are business decisions. Enforcing averages from a sample of 24 videos, 9 of them from one creator, would make every video formulaic, which feeds straight back into the originality risk in point 4.
   - I agree and am withdrawing the enforcement framing.
7. **Measure before fixing.**
   - I put the entity registry first. Theirs freezes a baseline first: turn the 31 reviews into an evaluation set, plus 10–15 real story cases.
   - Theirs is right. Without a baseline, no fix can be shown to help, and the matching issues file itself labels its diagnoses "plausible, not verified". I treated the PI diagnoses as established.
8. **Versioning and lineage on every artifact.** Producer version, input IDs and review state, plus a record at render time, so a corrected claim re-renders only the scenes it affects.
9. **Original visuals as a planned supply.** Purpose-made charts, maps, typographic evidence and licensed original graphics, so that every beat doesn't depend on scraped photos of artists.
10. **Asking about the channel's editorial promise and what "high quality" means in practice**: target length, voice, visual density, acceptable edit time, and 2–3 reference videos. I asked about budgets. I should also have asked what the channel is for.

### Scope differences (mine didn't cover these by design)

Neither of these are errors in mine:
- **Topic selection:** opportunity cards built from the 30-channel analysis, with performance normalized for video age and channel size.
- **The rest of the pipeline:** audio, render, final QC and publication gates (full watch-through by a person, draft upload before publishing), and orchestration as a per-video state machine.

They belong in the master document.

---

## 4. Where I disagree, or where mine should be kept

1. **The story library needs a concrete link to the data layer.**
   - Theirs calls the blueprints and signatures "a planning library". Mine turns each one into an evidence query with required pieces. For example, the Acceptance Treadmill requires three or more milestone → rejection → response triples, in time order.
   - A pattern with missing evidence abstains and becomes a research task. This is what makes discovery driven by data rather than by hunches, and theirs has no equivalent.
   - **Keep it**, with their caveat: a query that matches means the story is *possible*, not that it's true, and it still goes through the claim ledger.
2. **Claim types should line up with the matching jobs.**
   - Theirs has each beat spec carry "one or more communication jobs" but doesn't say where those jobs come from.
   - In mine, claim types are drawn from the 20 existing jobs, so choosing a job is a lookup. That removes the paid re-classification step from issue PI-05 and makes matching reproducible.
   - **Keep it**, with a fallback: beats with no claim (mood, transitions, questions) still get a job from the writer.
3. **PI-03, the spatial templates.**
   - Theirs says "do not expose every spatial template blindly if its slots cannot be filled." The user's recorded instruction is to show all of them, "period", whenever a beat names 20+ entities or compares things.
   - Mine does both: show every spatial template, mark the unfillable ones, and turn each gap into a sourcing request.
   - The user's explicit rule should win. Theirs should adopt "show all and flag", not "hide".
4. **Per-artist media kits over purely gap-driven sourcing.**
   - Theirs sources in response to specific gaps, prioritizing the ones that recur. That's right in general.
   - For rap at 2–3 videos a week, a standing kit per top artist costs less over time: the same 150–300 artists recur constantly. Kits handle the predictable demand and gap requests handle the rest.
   - **Keep both.**
5. **Identity accepted only when independent signals agree.**
   - Theirs says "calibrate before automatic assignment." Mine gives the rule for what to auto-accept: face match, caption or OCR entity, and source context all naming the same registry ID.
   - These fit together: the calibration sets the face threshold used inside that agreement rule.
6. **GAPS.md as a checker.**
   - Theirs lists generic requirements for statistical claims. Mine turns the specific, already-documented traps into comparability metadata and checker rules:
     - comparing Spotify totals across eras before about 2015;
     - comparing RIAA units across eras;
     - mixing iTunes rank with stream counts;
     - feature share with no stated basis;
     - Grammy counts without a receipt.
   - Those are known failure modes in this corpus. **Keep them**, as the rap-niche plug-in to their generic gate.
7. **When to extract events.** Mine says to extract once when content is ingested, validated against a schema, in priority order. Theirs doesn't say. Extracting at query time repeats cost and gives different answers on reruns. This is a real design decision, so keep mine unless their cost figures argue otherwise.
8. **Too many new objects up front.** Theirs introduces seven handoff objects at once. That's the right target, but with fully required fields it could hold up the pilot. Their own "first implementation slice" is the right counterweight: build each object with only the fields that slice needs, and grow the schemas from the failures it exposes.

---

## 5. How to update each document

### Theirs: add these

1. **Section 3 (story):** add pattern-first discovery.
   - Each blueprint and signature in `youtube_doc_analysis/synthesis/pattern_library.json` becomes an evidence query with required pieces; missing pieces produce a research task.
   - Link the file by path.
2. **Claim and BeatSpec:** add `claim.type`, drawn from the communication-job vocabulary. BeatSpec jobs default to the job derived from each claim, with an override for beats that have no claim.
3. **Section 2 (data):**
   - Add "extract events and relations when content is ingested, validated against a schema, priority entities first".
   - Add a rap-niche stats plug-in: the GAPS.md rules as comparability metadata plus a checker.
4. **Section 4 (matching), step 5:** replace "do not expose every spatial template blindly" with "show all spatial templates on 20+ entity or comparative beats, mark the unfillable ones, and emit gap requests", following the user's recorded rule.
5. **Section 5 (media):**
   - Add per-artist media kits for the recurring roster.
   - Add the independent-signals rule for identity, with calibrated per-identity face thresholds as one of the signals.

### Mine: change these

1. **Section 0 flow:** add a loop from story to visual feasibility before the script is locked. An unfillable pivotal beat goes back to the writer for revision, not only to sourcing.
2. **Claim ledger fields:**
   - add `status` (`supported`, `contested`, `inferred` or `unverified`) and `contradicting_receipts[]`;
   - add a counter-evidence search step for high-impact claims;
   - store interpretive edges in a separate namespace that can't be narrated without review.
3. **Section 4.3:** replace "compare to blueprint targets" with "surface deviations from the blueprints as review prompts". Nothing is enforced. Remove the sponsor and CTA defaults.
4. **Build order (section 5):**
   - Insert a new step 0: freeze the baseline. That means the evaluation set from the 31 reviews, 10–15 story cases including negative controls, and an inventory of the 30-channel analysis.
   - Validate each PI diagnosis against it before fixing.
5. **Media:**
   - Add original graphics as a planned supply.
   - Add a per-asset field for disclosure of realistic AI-generated media.
   - Add a channel-level originality check (the reused-content risk) to the release gate.
6. **Questions:** add questions on the channel's editorial promise, the operational definition of quality with reference videos, and who has final authority over contested claims.

### The story library in this repo: change these

1. Retitle the rules table in `synthesis/playbook.md` as *observed tendencies, used as review prompts*, and add the originality caveat.
2. Add an `evidence_requirements` field to each blueprint beat in `pattern_library.json`: the claim types and counts needed, such as "3+ milestone→rejection pairs". This lets the blueprints run as data-layer queries and is still pure storytelling.
3. Add a `counterthesis` slot to every blueprint. Their story plan requires a real opposing reading, and our strongest videos already do this: 011 concedes to its critics before answering, 019 complicates its own critique, 021 addresses the strongest counter-evidence.

---

## 6. Recommended next step

Follow their "first implementation slice", with my mechanisms plugged in:

1. **Freeze the baseline.** Turn the 31 reviews into an evaluation set and pick one rap topic that was already reviewed.
2. **Build a minimal claim ledger** for it: 20–40 claims, each with a type from the job vocabulary, a status, and supporting and contradicting receipts.
3. **Choose a blueprint** from `pattern_library.json`, and run its evidence query against the claims.
4. **Write beat specs** for the whole script. Run the story/visual feasibility loop on 10 representative beats:
   - a cohort beat;
   - a data chart;
   - an implied subject;
   - a beat missing b-roll;
   - a continuity run.
5. **Have the editor mark failures**, fix the contracts, and render one complete video.

**What I need from you:**
1. Which topic to use for the slice. The existing 40-beat Drake / Year Seventeen script is the obvious choice, since it already has reviews.
2. Whether I should apply the updates to my handoff and to the story library (section 5) now.
