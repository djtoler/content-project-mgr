# Raw reference transcript to final StoryPackage

## Purpose

This is the controlled pipeline for adapting an existing reference-channel
transcript into a new target-niche story, generating the Data layer's production
brief, and publishing the final StoryPackage consumed by Matching.

The reference transcript is structural and editorial evidence. It is not factual
authority for the target story. The production brief is downstream of a finished
target-script candidate; it does not discover the angle or write the script.

## Ownership summary

| Owner | Owns | Does not own |
|---|---|---|
| **Content Project Manager** | Run identity, stage order, artifact hashes, handoffs, blockers, receipts and release gates | Story judgment, factual verification, template selection or rendering |
| **Story layer** | Target-story thesis, structure, beat map, narration, StoryIR, claims-to-narration links, editorial VisualTasks and final StoryPackage | Treating unverified leads as facts, sourcing media or selecting templates |
| **Data layer** | Entity registry, evidence retrieval, claim verification, typed measurements and finished-script production brief | Rewriting the target script, deciding its argument or selecting templates |
| **Editor** | Target niche/topic, story and script approval, disputed claims, production-brief decisions and final editorial acceptance | Fabricating evidence or bypassing contract gates |
| **Matching layer** | Capability-based template candidates and treatment feasibility from the final StoryPackage | Reading the raw production brief as an undocumented admission signal |
| **Media layer** | Asset discovery, provenance, rights and technical readiness from typed briefs | Changing Story meaning or template capability truth |

## Required inputs

The Content Project Manager creates a versioned intake containing:

- the immutable raw reference transcript;
- the reference video URL or stable video ID;
- optional matching video metadata;
- the target niche, topic or subject;
- desired runtime, voice and tone;
- editorial constraints and prohibited treatments;
- source hashes and an intake/run ID.

If the target topic or evidence packet is absent, Story may produce a structural
blueprint and research request, but not a finished target script.

## Pipeline

### Step 0 — Register and freeze the intake

**Primary owner:** Content Project Manager  
**Consulted:** Editor  
**Inputs:** Raw transcript, reference-video identity and target-story direction.  
**Actions:**

1. Store the raw transcript without rewriting it.
2. Record its SHA-256, source video ID/URL, provenance and target brief.
3. Create the run ID and declare the expected stages.
4. Reject or pause if the transcript and video identity conflict.

**Output:** Immutable reference-intake receipt.  
**Gate:** Every downstream artifact must bind this exact intake or explicitly
supersede it.

### Step 1 — Extract reusable story structure

**Primary owner:** Story layer  
**Consulted:** Editor  
**Inputs:** Frozen reference intake.  
**Actions:**

1. Identify the hook, setup, escalation, reversals, re-hooks and payoff.
2. Describe each section by narrative function rather than reference subject.
3. Record pacing and section proportions as optional guidance.
4. Separate reference facts, entities and quotations from reusable structure.
5. Do not select templates or treat the reference video's visuals as required.

**Output:** Source-bound structural analysis/blueprint.  
**Gate:** The target story can use the structure without copying reference facts
or entities.

### Step 2 — Define the target story and research needs

**Primary owner:** Story layer  
**Consulted:** Editor, Data layer  
**Inputs:** Structural analysis, target niche/topic and available evidence.  
**Actions:**

1. Propose the target thesis, strongest alternative, tension and audience promise.
2. Draft the target beat/argument map.
3. List every factual claim, measurement, entity and unresolved research need.
4. Flag visual feasibility risks at outline level.

**Output:** Draft StoryIR, claim requests and research brief.  
**Gate:** No unsupported pivotal claim advances as narration.

### Step 3 — Research and verify target-story claims

**Primary owner:** Data layer  
**Consulted:** Story layer, Editor  
**Inputs:** Claim/research requests and shared entity registry.  
**Actions:**

1. Resolve entities and aliases against the shared registry.
2. Retrieve evidence and typed measurements with source receipts.
3. Mark claims supported, contradicted, qualified, unresolved or rejected.
4. Return missing evidence and material caveats to Story.

**Output:** Evidence records, ClaimLedger updates, typed values and explicit gaps.  
**Gate:** High-impact factual narration must have adequate evidence or be revised,
qualified or removed.

### Step 4 — Write the target-niche script

**Primary owner:** Story layer  
**Consulted:** Data layer, Editor  
**Inputs:** Target StoryIR and verified Data outputs.  
**Actions:**

1. Write the voice-ready target script.
2. Link factual narration spans to ClaimLedger entries.
3. Mark interpretation, question, setup and transition spans.
4. Maintain the target story's own entities and meaning; do not transplant the
   reference subject matter.
5. Run outline/script-level visual feasibility checks.

**Output:** Finished-script candidate and updated StoryIR.  
**Gate:** Editor approves the story promise, argument, counterevidence, voice and
read-through before production-brief generation.

### Step 5 — Generate the finished-script production brief

**Primary owner:** Data layer  
**Consulted:** Story layer, Media layer  
**Inputs:**

- approved target-script candidate;
- original frozen reference transcript;
- matching reference-video URL/ID;
- optional video metadata or previously bound visual-analysis artifact;
- configured evidence and B-roll providers.

**Actions:**

1. Verify that reference transcript, URL and metadata identify the same video.
2. Parse the target script into sections and the reference transcript into
   timecoded segments.
3. Analyze the reference video's editing and motion language when authorized.
4. Align reference editorial functions to target-script sections.
5. Produce evidence leads, B-roll briefs/candidates, data-animation briefs and
   transition notes.
6. Label web evidence as unverified leads and footage as uncleared candidates.

**Existing implementation:** `contradiction production-brief` in
`hiphop-research-engine`.  
**Output:** Source-bound production-brief JSON and optional Markdown view with
status `needs_editor_review`.  
**Gate:** A production brief is invalid if it is bound to a different target
script or mismatched reference-video identity.

### Step 6 — Validate and normalize the production brief

**Primary owner:** Story layer  
**Consulted:** Data layer, Media layer, Editor  
**Inputs:** Production brief and the exact finished-script candidate.  
**Actions:**

1. Accept, reject or defer every proposed production item with a reason.
2. Send evidence leads back to Data for verification; never promote a lead merely
   because it appears in the brief.
3. Convert verified data-animation needs into typed data requirements.
4. Convert B-roll needs into typed Media requirements without claiming that an
   asset is available or cleared.
5. Convert useful transition/visual observations into editorial context or
   presentation requirements without copying the reference design as a mandate.
6. Preserve Story's beat meaning and claim boundaries.

**Output:** Production-brief reconciliation and proposed StoryIR/script changes.  
**Gate:** Raw production-brief prose never enters Matching as candidate-admission
or approval evidence.

### Step 7 — Revise and stabilize the target script

**Primary owner:** Story layer  
**Consulted:** Data layer, Editor  
**Inputs:** Reconciled brief and verified follow-up evidence.  
**Actions:**

1. Revise narration, claims or visual requirements only where justified.
2. Preserve stable beat and claim IDs when their meaning has not changed.
3. Create explicit supersession records for material semantic changes.
4. If narration, section boundaries or pivotal claims materially change, return
   to Step 5 and regenerate the production brief against the new script hash.

**Output:** Stable final script candidate and current reconciliation receipt.  
**Gate:** Production brief and script hashes agree, and every brief item has a
recorded disposition.

### Step 8 — Finalize Data and registry bindings

**Primary owner:** Data layer  
**Consulted:** Story layer  
**Inputs:** Stable script, ClaimLedger, typed requirements and shared registry.  
**Actions:**

1. Resolve registry additions and aliases.
2. Bind verified typed values and their exact receipts.
3. Preserve unresolved values as explicit gaps; never coerce absence to zero.
4. Publish the Data handoff revision consumed by the final package.

**Output:** Registry-pinned entity context, verified ClaimLedger and typed Data
handoff.  
**Gate:** Final StoryPackage may contain explicit unresolved non-pivotal gaps, but
must not mislabel them as verified.

### Step 9 — Publish the final StoryPackage

**Primary owner:** Story layer  
**Consulted:** Data layer, Editor  
**Inputs:** Stable script, StoryIR, ClaimLedger, registry/Data handoff and
production-brief reconciliation.  
**Actions:**

1. Build the final versioned StoryPackage deterministically.
2. Include beats, claims, narration spans, obligations, prohibitions, continuity,
   data/media requirements and source references.
3. Bind the exact script, registry, evidence and applicable production artifacts.
4. Validate the package and reproduce it byte-identically.

**Output:** Final StoryPackage plus validation and build receipts.  
**Gate:** Editor approves publication to downstream consumers. Draft StoryIR or an
unreconciled production brief is not a final StoryPackage.

### Step 10 — Freeze and hand off to Matching

**Primary owner:** Content Project Manager  
**Consulted:** Story layer, Data layer, Matching layer  
**Inputs:** Final validated StoryPackage and all required receipts.  
**Actions:**

1. Record the final package hash and upstream dependency versions.
2. Confirm all required stages ran in order and no receipt is stale.
3. Declare whether the package is calibration, regression or untouched held-out
   evidence before Matching sees it.
4. Hand only the final package and its declared contracts to Matching.

**Output:** Immutable downstream handoff receipt.  
**Gate:** Matching rejects incomplete, stale or out-of-order upstream contracts.

### Step 11 — Match, source and render through existing gates

**Primary owners:** Matching layer → Media layer → Editor/render pipeline  
**Inputs:** Final StoryPackage.  
**Actions:**

1. Matching derives/validates coherent VisualTasks and evaluates every relevant
   existing template candidate through the required contract stages.
2. Matching preserves no-template/B-roll routes and returns typed gaps.
3. Media sources and verifies requested assets.
4. Editor approves choices; rendering uses only established gated systems.

**Output:** Reviewable VisualPlan, Media assignments and—only after approval—
render receipts.  
**Gate:** Production-brief guidance, ranking scores and historical choices do not
authorize selection or rendering.

## Loop and stop rules

- **Research loop:** Steps 2–4 repeat until pivotal claims are adequately
  supported or removed.
- **Production loop:** Steps 5–7 repeat only when the target script changes
  materially after production-brief reconciliation.
- **Registry loop:** Step 8 may return to Story when unresolved identity changes
  narration meaning or obligations.
- **Stop condition:** Script hash, production-brief binding, registry, ClaimLedger
  and final StoryPackage all agree; required receipts are current; editor approval
  is recorded.
- **No silent loop:** Every return to an earlier step records the cause, changed
  artifacts and superseded versions.

## Required provenance chain

```text
reference transcript/video hash
  → structural analysis
  → target StoryIR and research requests
  → verified ClaimLedger/Data receipts
  → finished target-script hash
  → production-brief hash
  → production-brief reconciliation
  → final script + registry/Data revision
  → final StoryPackage hash
  → Matching handoff receipt
```

## Non-negotiable boundaries

- Data does not write the target story or silently rewrite its script.
- Story does not promote unverified evidence leads or claim sourced media exists.
- Matching does not read the raw production brief as hidden candidate evidence.
- The reference video's subject matter and visuals do not become mandatory target
  content merely because they appear in the reference.
- No score, brief, prior choice or model confidence authorizes template selection
  or rendering.
- A held-out package remains untouched only until its first Matching exposure;
  feedback after exposure becomes regression evidence for the next version.
