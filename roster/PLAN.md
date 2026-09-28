# Entity-context roster implementation plan

Date: 2026-09-28  
Branch: `codex/entity-context-roster`

## Objective

Create one versioned entity-context contract shared by research retrieval, story packages, and media matching. Extend the existing entity-registry direction in this repository; do not create a competing media catalog, research store, or unreviewed roster of real people.

Manual editor context is the controlling editorial interpretation. Data-derived facts and their evidence remain preserved for traceability, but they cannot overwrite or outrank an applicable editor instruction.

## Required stages and acceptance checks

### 1. Freeze the contract and authority order

Define stable entities, aliases, evidence-linked factual claims, evidence-linked characterizations, persistent and computed cohorts, story-package references, and manual editor context.

Acceptance:

- Authority is deterministic: story-scoped editor context, global editor context, reviewed factual context, then machine-derived candidates.
- Manual editor context remains visibly separate from factual evidence.
- Subjective traits cannot be stored as unqualified facts.

### 2. Publish a closed JSON Schema

Add a JSON Schema for the roster document and its nested records.

Acceptance:

- Entity, cohort, claim, evidence, and editor-context IDs are required and typed.
- Computed cohorts retain a replayable rule and data-snapshot ID.
- Factual claims and source characterizations require evidence references.
- Editor context records author, scope, instruction, and optional overridden claim IDs.

### 3. Implement deterministic validation and resolution

Add a dependency-free Python validator/resolver for repository and pipeline use.

Acceptance:

- Reject duplicate IDs, dangling references, alias collisions, missing evidence, invalid cohort membership, and invalid override references.
- Resolve applicable context without a model call.
- Prove that applicable editor context wins editorial precedence while preserved facts remain inspectable.

### 4. Provide story-package and retrieval guidance

Document where IDs are assigned and how the same IDs bind research chunks, story packages, and media.

Acceptance:

- Ingestion/entity resolution owns mention-to-ID binding.
- Story/Data owns cohort meaning and exact membership or a replayable membership rule.
- Matching consumes cohort/entity IDs, retrieves media, and reports missing coverage without inventing membership.
- Research retrieval and media retrieval remain separate stores connected through shared IDs.

### 5. Test and publish

Use synthetic fixtures so no example is mistaken for a factual claim about a real person.

Acceptance:

- Unit tests cover precedence, scoping, temporal activity, validation failures, persistent cohorts, and computed cohorts.
- The example roster passes the command-line validator.
- All files are committed on the non-main branch and pushed to GitHub.

## Execution review

| Stage | Evidence | Result |
|---|---|---|
| 1. Contract and authority | `README.md`; editor-first order encoded in both resolvers | Passed |
| 2. Closed schema | `entity-context.schema.json`; JSON parsing and closed-root test | Passed |
| 3. Validation and resolution | `roster.py`, `validate_roster.py`; person and cohort precedence tests | Passed |
| 4. Handoff guidance | `README.md`; synthetic story binding and computed cohort fixture | Passed |
| 5. Test and publish | 13 unit tests, Python compilation, JSON parsing, CLI validation and `git diff --check`; branch `codex/entity-context-roster` | Passed; committed and pushed |

No real-person roster was generated, no existing entity source was modified, and no model call or external data transfer occurred. Real population remains a later import from the existing Astra roster, resolved Data-layer entities, or a higher-authority curated editor roster.

## Follow-up verification: trait separation and vector-lead quarantine

User-required follow-up, 2026-09-28:

1. Subjective personality, character and motive descriptions must not enter `factualClaims` as permanent entity facts. They belong in evidence-linked `characterizations` or manual `editorContext`.
2. Vector similarity is discovery evidence only. A vector hit must not become a factual claim, relationship, motive or personality characterization until independent source-bound evidence supports that record.

Acceptance checks:

- The schema and semantic validator reject interpretive `claimType` values in `factualClaims`.
- Subjective traits remain available as explicitly labeled, attributed `characterizations`; facts, subjective lenses and editor context all travel separately.
- A characterization supported only by vector-similarity/lead-only evidence is rejected.
- A reviewed fact or observed relationship supported only by vector-similarity/lead-only evidence is rejected.
- Vector results can be retained in a separate `retrievalLeads` collection without appearing in resolved facts or characterizations.
- A source-bound characterization with attribution and direct/contextual support continues to pass.
- New regression tests run with the original editor-precedence, cohort and reference-integrity tests.

Follow-up result: passed. The complete suite now contains 21 passing tests. Focused evidence and the verification boundary are recorded in `VERIFICATION.md`.
