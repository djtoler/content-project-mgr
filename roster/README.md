# Shared entity-context roster

This directory defines the shared identity and context contract used by three consumers:

1. the data layer retrieves evidence about the correct people, groups, events and relationships;
2. the story-package builder hands the writing agent stable references instead of unbound names;
3. the matching layer retrieves the correct media and checks cohort coverage without inventing membership.

It extends the repository's existing entity/cohort crosswalk plan. It is not a second vector database, media catalog, claim ledger or story store.

## Authority order

The deterministic resolver uses this order:

1. story-scoped manual editor context;
2. global manual editor context;
3. editor-adopted interpretive branches;
4. reviewed factual claims and source characterizations;
5. machine-derived candidates.

Manual editor context controls the public-facing editorial interpretation. A conflicting factual or model-derived record remains preserved in `supportingFacts` or `overriddenFacts` so it can be inspected, but it cannot overwrite or outrank an applicable editor instruction.

Story-scoped editor directives outrank global editor directives for the same key. Within the same scope, the latest active directive wins. The resolver reports every shadowed directive rather than deleting it.

An editor note is not relabeled as an objective fact. This separation preserves both editorial control and evidence traceability.

## Where IDs are assigned

### Ingestion and entity resolution

The entity resolver binds mentions and aliases to stable `entityId` values when research or media is ingested. Exact reviewed aliases may bind automatically. Ambiguous matches remain unresolved for review; neither the writer nor the matcher guesses.

Research chunks should retain `mentionedEntityIds` and the narrower `aboutEntityIds`. Media records should retain `depictsEntityIds`. Both stores may additionally carry cohort, relationship and event references.

### Story-package assembly

The story-package builder selects relevant IDs from the resolved evidence graph and saves a `storyBinding` containing entity, cohort, relationship, claim, characterization, interpretive-branch and evidence references. The writing agent receives this binding with the evidence packet.

### Cohorts

- A persistent real-world group has a stable cohort ID and reviewed membership.
- A computed or story-specific group has a versioned cohort ID, an exact member list, a replayable membership rule and the exact data-snapshot ID used to produce it.

Story/Data owns cohort meaning and membership. Matching expands the supplied cohort reference to retrieve media and report missing coverage.

## Character traits and character context

Do not flatten a subjective trait into an unqualified entity fact. Store:

- documented facts as `factualClaims`;
- source-attributed subjective traits or descriptions as `characterizations`, with exact evidence and an explicit lens type;
- the editor's intended public framing as `editorContext`, with author and scope.

For example, an interview describing somebody as competitive is a source characterization. An editor instruction saying that the story should emphasize discipline over rivalry is controlling editorial context. Both remain visible.

Subjective lenses are not discarded or demoted from retrieval. They travel beside factual claims through `characterizationIds` and resolve under `sourceCharacterizations`. Their label keeps interpretation from being mistaken for objective fact. Supported lens types are self-description, source characterization, critical interpretation and audience perception.

## Interpretive branches

An `interpretiveBranch` is a first-class narrative hypothesis, lens or possible reading. Vector or lexical similarity may create one directly even when the lead cannot support a fact or source-attributed characterization. The branch may say `Alex was jealous of Blair.`; direct wording is allowed because the record's type, not its grammar, controls downstream handling.

Every branch carries both:

- `directStatement`, for forceful narrative development;
- `cautiousStatement`, expressed as a question or qualified interpretation.

`preferredNarrativeMode` records whether the editor wants both, direct or cautious presentation. Status distinguishes open research from an editor-adopted, source-supported or rejected interpretation. An editor-adopted branch receives high narrative priority but remains an interpretation and is never returned under `supportingFacts`.

## Retrieval behavior

Research and media stay in their established stores. Shared IDs provide the join:

1. apply exact entity, cohort, relationship, event and time filters;
2. apply active editor retrieval terms and directives first;
3. use semantic or lexical retrieval inside the eligible set;
4. return evidence or media with the IDs and provenance that caused the match.

Vector similarity never creates identity, cohort membership or factual truth. It may create a clearly labeled interpretive branch about motive or character.

### Retrieval-lead quarantine

Vector similarity and lexical search may save a `retrievalLead` with its query, score and candidate passage. That passage is required to remain `lead_only`. It cannot support a factual claim, observed relationship, cohort membership or source-attributed characterization. It may originate an `interpretiveBranch`, which retains the lead reference and remains labeled as interpretation.

Promotion into a fact or source-attributed characterization requires opening the underlying source, saving source-bound evidence, and creating a separately validated record. No such promotion is needed to preserve or narratively explore the idea as an interpretive branch.

`factualClaims` use a closed set of objective claim types. Interpretive predicates such as trait, personality, motive, temperament, character or framing are rejected there. Source-attributed character descriptions belong in `characterizations`; the editor's intended take belongs in `editorContext`.

## Files

- `entity-context.schema.json` — closed interchange schema.
- `roster.py` — dependency-free semantic validator and deterministic precedence resolver.
- `validate_roster.py` — command-line validation and optional resolved-context inspection.
- `examples/example-roster.json` — synthetic example; it makes no claims about real people.
- `tests/test_roster.py` — contract and precedence tests.
- `VERIFICATION.md` — focused evidence for subjective-lens separation and vector-lead quarantine.
- `PLAN.md` — ordered implementation and acceptance checks.

## Commands

```bash
python3 roster/validate_roster.py roster/examples/example-roster.json
python3 roster/validate_roster.py roster/examples/example-roster.json \
  --entity person:alex-river --story story:demo
python3 roster/validate_roster.py roster/examples/example-roster.json \
  --cohort cohort:synthetic-top-two-2026-09-28 --story story:demo
python3 -m unittest discover -s roster/tests -v
```

## Real roster population

This contract does not require the editor to hand-type the starting roster. Seed candidates from the existing Astra entity roster and resolved Data-layer entities. Preserve their source IDs. Alias collisions, uncertain identities, cohort membership and character context require review before they become authoritative.

If a curated editor roster already exists, import it as the higher-authority seed. Generated candidates must never overwrite it.
