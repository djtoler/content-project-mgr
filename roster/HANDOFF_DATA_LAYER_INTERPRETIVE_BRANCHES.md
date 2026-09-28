# Data-layer handoff: shared roster and interpretive branches

Date: 2026-09-28  
Target system: `hiphop-research-engine` / contradiction engine  
Contract source: this directory, schema version `1.1.0`  
Implementation branch: `codex/entity-context-roster`

## Outcome

Extend the existing data layer so it can export the shared entity-context roster and story bindings without creating a second research database or replacing the current event graph, hypothesis generators, branch traces, dossiers, evidence records, review states, or pgvector index.

The material change is a first-class `interpretiveBranch` lane. A vector or lexical retrieval lead may originate an interpretation such as:

- direct: `Person X was jealous.`
- cautious: `Was Person X jealous?`

Both formulations must travel together. The direct sentence is allowed to be narratively forceful. Its presence under `interpretiveBranches`—not its grammar—tells downstream systems that it is an interpretation rather than a factual claim.

## Source of truth

Use these files as the interchange contract and executable reference:

- `roster/entity-context.schema.json`
- `roster/roster.py`
- `roster/examples/example-roster.json`
- `roster/tests/test_roster.py`
- `roster/README.md`

Do not copy and then independently modify the schema inside the data layer. Import the versioned schema as a dependency, vendor it with its source commit recorded, or add a contract-export adapter whose output is validated against this exact schema.

## Fit with the existing data layer

Use the systems already present in `hiphop-research-engine`:

- `segment_embeddings` remains the semantic-retrieval index.
- Existing source/evidence records remain the evidence store.
- Existing entity and alias resolution remains the identity foundation.
- `hypothesis_generation.py` and `layered_story_analysis.py` remain hypothesis producers.
- Existing event-graph dossiers and their `editorial_question` fields remain discovery inputs.
- Existing branch traces remain provenance for how a question or hypothesis was reached.
- `discovery_hypothesis_reviews` and existing editorial review mechanisms remain the review source.

Add an adapter and durable fields/tables to the established database as needed. Do not create a parallel vector store, a second entity registry, or a replacement hypothesis engine.

## Ownership boundary

### Data layer owns

- resolving mentions to stable entity IDs or leaving them unresolved;
- retaining semantic/lexical hits as `retrievalLeads`;
- producing candidate interpretive branches from existing hypothesis and dossier outputs;
- producing both direct and cautious language for the same interpretation;
- recording branch provenance, scope, status, editor decision, and rejection history;
- exporting contract-valid entities, evidence, leads, branches, characterizations, and story bindings;
- keeping interpretations out of factual fields unless a separate factual promotion succeeds.

### Story/editor owns

- adopting, rejecting, or revising an interpretation;
- choosing `preferredNarrativeMode`: `both`, `direct`, or `cautious`;
- deciding whether an adopted branch belongs in a particular story package;
- supplying higher-authority manual framing through `editorContext`.

### Matching owns

- consuming `interpretiveBranchIds` from the story binding;
- using the selected direct and/or cautious language to understand the visual job;
- retrieving templates and media without treating the branch as an objective fact;
- preserving branch IDs in the VisualTask and final decision trace.

Matching must not generate new entity membership, factual status, or branch promotion.

## Required records

### 1. Retrieval lead

For every semantic or lexical result used to originate a branch, export:

```json
{
  "id": "retrieval-lead:stable-id",
  "method": "vector_similarity",
  "query": "the exact query",
  "entityIds": ["person:stable-id"],
  "cohortIds": [],
  "candidateEvidenceIds": ["evidence:stable-id"],
  "score": 0.81,
  "status": "candidate",
  "createdAt": "2026-09-28T12:05:00Z"
}
```

The linked evidence remains `supportLevel: lead_only`. Preserve the embedding model, index/run identity, rank, distance/score, query, filters, and source segment in the data layer's native provenance even where the interchange record exposes only the normalized fields.

### 2. Interpretive branch

Export every selected hypothesis through this required shape:

```json
{
  "id": "interpretive-branch:stable-id",
  "branchType": "motive",
  "originType": "vector_inference",
  "directStatement": "Person X was jealous.",
  "cautiousStatement": "Was Person X jealous?",
  "cautiousForm": "question",
  "preferredNarrativeMode": "both",
  "rationale": "Why the available material makes this interpretation useful to examine.",
  "status": "editor_adopted",
  "scope": {"kind": "story", "storyId": "story:stable-id"},
  "entityIds": ["person:stable-id"],
  "cohortIds": [],
  "retrievalLeadIds": ["retrieval-lead:stable-id"],
  "evidenceIds": ["evidence:stable-id"],
  "createdBy": "editor:stable-id",
  "createdAt": "2026-09-28T12:07:00Z"
}
```

Allowed values are defined by the JSON Schema. In particular:

- `branchType`: `motive`, `personality`, `dynamic`, `causal_hypothesis`, `theme`, `counter_reading`, or `other`;
- `originType`: `vector_inference`, `lexical_inference`, `editor_hypothesis`, `source_interpretation`, or `mixed`;
- `cautiousForm`: `question` or `qualified_interpretation`;
- `preferredNarrativeMode`: `both`, `direct`, or `cautious`;
- `status`: `open`, `researching`, `editor_adopted`, `source_supported`, or `rejected`.

`source_supported` means sources make the interpretation worth supporting or presenting. It does not convert a motive, personality reading, causal theory, or other interpretation into an objective fact.

### 3. Story binding

Add `interpretiveBranchIds` beside—not inside—`claimIds` and `characterizationIds`:

```json
{
  "storyId": "story:stable-id",
  "entityIds": [],
  "cohortIds": [],
  "relationshipIds": [],
  "claimIds": [],
  "characterizationIds": [],
  "interpretiveBranchIds": [],
  "evidenceIds": [],
  "editorContextIds": []
}
```

A story-scoped branch may be included only in its own story binding. Global branches may be included in any applicable story.

## Language-pair rule

Generate the direct and cautious versions from one canonical proposition, not as two independent hypotheses.

Example canonical proposition:

```text
subject: Person X
predicate: jealous_of
object: Person Y
polarity: affirmative
```

From that proposition:

```text
directStatement: Person X was jealous of Person Y.
cautiousStatement: Was Person X jealous of Person Y?
```

Before saving, deterministically verify that both formulations retain the same:

- entity IDs and roles;
- predicate or interpretive relationship;
- polarity;
- time scope, if one is stated;
- comparison target or object.

If the two formulations differ in meaning, reject the pair for review. Do not silently keep whichever version appears safer.

The direct version does not need hedging. The cautious version must genuinely be a question or qualified interpretation rather than a differently worded factual assertion.

## Pipeline sequence

1. Run the existing semantic, lexical, event-graph, hypothesis, or dossier path.
2. Preserve every selected vector/lexical result as a retrieval lead with its source-segment evidence.
3. Resolve all named people/groups to stable IDs. Unresolved identity blocks story binding but may remain in the native research review queue.
4. Convert an existing hypothesis/editorial question into one canonical interpretive proposition.
5. Generate its direct and cautious formulations together.
6. Validate semantic equivalence between both formulations.
7. Save the branch as `open` or `researching`.
8. Present the branch for editorial review with both formulations, the originating leads, rationale, sources, contrary material, and gaps visible.
9. Save the editor's decision and preferred narrative mode. An editor adoption changes status and priority, not truth type.
10. Export selected branches in the story binding.
11. Validate the complete export with `roster.validate_roster` before handing it to Story or Matching.

## Review behavior

The review surface must show, together:

- direct statement;
- cautious statement;
- branch type and origin type;
- involved entities/cohorts;
- retrieval leads and exact source passages;
- supporting and contrary material;
- rationale and unresolved research gaps;
- current scope and status;
- preferred narrative mode.

Required actions:

- adopt;
- revise direct language;
- revise cautious language;
- set preferred mode;
- continue research;
- reject.

Every revision creates durable history. Rejection must not delete the branch or its provenance, and a rerun must not silently recreate a rejected branch as new merely because wording changed.

Manual editor input has the highest editorial authority. Story-scoped editor context outranks global editor context. Both outrank model-generated framing when determining story emphasis and public presentation.

## Separation and promotion rules

### Vector/lexical material may directly create

- a retrieval lead;
- an interpretive branch;
- follow-up research queries;
- a candidate story direction.

### Vector/lexical lead-only material may not directly create

- a `factualClaim`;
- an observed relationship;
- cohort membership;
- a source-attributed `characterization`.

### Promotion paths

- If source-bound evidence supports an objective proposition, create a new `factualClaim` with its own ID and evidence. Preserve the branch.
- If a named source expresses the subjective view, create a new attributed `characterization`. Preserve the branch.
- If the editor adopts the interpretation, set the branch to `editor_adopted` and record `preferredNarrativeMode`. Do not copy it into `factualClaims`.
- If later research contradicts it, set it to `rejected` or retain a contested/source-supported interpretation as editorially decided. Do not erase its prior use or provenance.

One idea may therefore produce multiple related records with different epistemic types. Link them in native provenance, but never collapse them into one record.

## Existing-output mapping

Start with adapters, not rewrites:

| Existing data-layer output | Shared-contract destination |
|---|---|
| semantic result from `segment_embeddings` | `retrievalLead` plus `lead_only` evidence |
| layered story hypothesis | candidate `interpretiveBranch` |
| general hypothesis question | `cautiousStatement`; derive paired `directStatement` from the same canonical proposition |
| event-graph dossier `editorial_question` | candidate `interpretiveBranch` when it expresses an interpretation rather than a simple missing fact |
| branch trace | native provenance linked to `retrievalLeadIds` and the branch ID |
| approved/revised discovery hypothesis | `editor_adopted` branch with durable editor identity |
| source-attributed subjective description | `characterization`, not an interpretive branch unless the story also needs a separate editorial reading |
| verified objective proposition | `factualClaim`, never an interpretive branch replacement |

Do not bulk-convert every existing question. Exclude operational research prompts, simple factual questions, missing-data requests, and questions with unresolved entities. Begin with hypotheses already shown to an editor or included in a dossier.

## Stable IDs and deduplication

Create the branch ID from stable inputs such as:

- canonical proposition;
- resolved entity/cohort IDs;
- story scope;
- origin record IDs;
- contract version.

Wording-only changes must create a revision, not a duplicate branch. A materially different predicate, polarity, object, entity set, or story scope is a new branch.

Before inserting a candidate, check rejected and adopted history by canonical proposition, not just exact text.

## API/export expectations

The story-package export must provide four visibly separate lanes:

1. `factualClaims` / `claimIds`;
2. `characterizations` / `characterizationIds`;
3. `interpretiveBranches` / `interpretiveBranchIds`;
4. `editorContext` / `editorContextIds`.

Consumers must not infer epistemic type from prose. They must dispatch on the field and referenced record type.

For an editor-adopted branch, return both formulations even if the preferred mode is only one. `preferredNarrativeMode` is a presentation instruction, not permission to discard the alternative.

## Migration and rollout

### Phase 1: adapter-only pilot

- Select a small set of already reviewed hypotheses from existing discovery outputs.
- Resolve their entities using the existing registry.
- Build retrieval-lead and branch records without altering the original artifacts.
- Export one contract-valid roster/story package.

### Phase 2: durable review integration

- Add branch ID, language pair, status, editor identity, preferred mode, and revision history to the established review persistence.
- Reuse existing idempotency and receipt patterns.
- Prove that rejected branches are not regenerated as duplicates.

### Phase 3: story-package export

- Add `interpretiveBranchIds` to the production story binding.
- Validate every export against schema `1.1.0` and the semantic validator.
- Fail the handoff if a reference is missing, cross-story, duplicated, or semantically invalid.

Do not backfill the full corpus until the pilot demonstrates usable branches, acceptable duplicate rates, stable entity resolution, and manageable editor review time.

## Acceptance tests

The data-layer implementation is complete only when these tests pass:

1. A vector hit can create a branch whose direct statement says `Person X was jealous.`
2. The same branch also contains a semantically equivalent cautious version.
3. Removing either formulation fails validation.
4. The branch resolves only under `interpretiveBranches`.
5. Neither formulation appears under facts or source-attributed characterizations.
6. An editor can adopt direct, cautious, or both without changing the branch's epistemic type.
7. Editor adoption outranks model framing in story presentation.
8. A vector-origin branch retains its exact retrieval-lead ID and source segment.
9. Vector-only evidence still fails when used for a fact, observed relationship, cohort, or source characterization.
10. A story-scoped branch cannot enter another story binding.
11. Wording revisions preserve one branch identity and revision history.
12. Rejected branches remain suppressed across reruns.
13. Source support can create a separate factual claim or characterization without deleting the branch.
14. The exported example passes `roster.validate_roster` and the complete roster test suite.

Use synthetic people and statements in automated tests. Do not manufacture real-person motive or personality statements merely to exercise the contract.

## Definition of done

- Existing data-layer systems produce the new lane through an adapter or native export.
- No second vector store or entity registry was introduced.
- Both narrative formulations are retained for every branch.
- Editor decisions and revisions are durable and replay-safe.
- Story packages carry `interpretiveBranchIds` separately.
- Facts, source characterizations, interpretations, and editor context remain distinguishable by field and ID.
- Contract validation and all acceptance tests pass.
- One reviewed real workflow is exported successfully without modifying its original evidence artifacts.

## Explicit non-goals

- Proving interpretations objectively true.
- Forcing cautious wording into the final narration.
- Preventing direct assertions inside the interpretive lane.
- Replacing current hypothesis, event-graph, dossier, review, or vector systems.
- Automatically publishing a branch because it has a high similarity or ranking score.
- Implementing matching-layer template selection in the data layer.
