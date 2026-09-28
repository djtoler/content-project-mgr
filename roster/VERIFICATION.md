# Trait and vector-lead verification

Date: 2026-09-28  
Branch: `codex/entity-context-roster`

## Claims under test

1. A subjective trait is retained as a useful lens but cannot be stored as an unqualified factual claim.
2. Weak vector similarity cannot become a factual claim, observed relationship or source-attributed characterization, but it may originate an explicitly labeled interpretive branch.

## Enforced behavior

### Facts and subjective lenses travel together, separately

`factualClaims` uses a closed objective `claimType` vocabulary. The semantic validator also rejects factual predicates containing interpretive categories such as trait, personality, motive, temperament, character or framing.

Subjective context remains first-class in `characterizations`. Every characterization requires:

- an explicit `lensType`;
- a trait and statement;
- attribution;
- source-bound evidence;
- a review state.

Story bindings carry `claimIds` and `characterizationIds` in separate arrays. The resolver returns facts and `sourceCharacterizations` separately, alongside higher-priority `editorContext`.

### Vector results may feed labeled interpretive branches

Vector and lexical retrieval evidence must be marked `lead_only` and retained in `retrievalLeads`, with its query, method, score and candidate evidence. A lead may also be referenced by an `interpretiveBranch`.

The semantic validator rejects lead-only/vector evidence when used to support:

- a factual claim;
- a characterization;
- an observed relationship;
- a cohort definition or membership record.

The resolver does not include retrieval leads in facts or source characterizations. It may return a linked interpretation only in `interpretiveBranches`. Each branch carries a direct assertion and cautious formulation together. Promotion into a fact or source characterization requires separately saved source-bound evidence from the underlying material.

## Tests

The complete 27-test suite passes, including these focused regressions:

- `test_subjective_trait_cannot_be_a_factual_claim`
- `test_interpretive_predicate_cannot_hide_under_factual_type`
- `test_subjective_lens_requires_explicit_label`
- `test_story_binding_carries_fact_and_subjective_lens_separately`
- `test_underlying_characterization_is_preserved`
- `test_vector_similarity_cannot_support_characterization`
- `test_vector_similarity_cannot_support_fact`
- `test_vector_similarity_cannot_support_observed_relationship`
- `test_vector_lead_enters_only_through_labeled_interpretive_branch`
- `test_vector_similarity_can_create_direct_interpretive_assertion`
- `test_interpretive_branch_requires_direct_and_cautious_language`
- `test_interpretive_assertion_resolves_only_in_its_labeled_lane`
- `test_story_scoped_interpretive_branch_stays_in_its_story`
- `test_vector_interpretive_branch_requires_vector_lead`
- `test_interpretive_branch_cannot_be_bound_to_another_story`

The example roster also passes the command-line validator, both JSON files parse, and `git diff --check` passes.

## Boundary of verification

This verifies the contract and deterministic validator. It does not claim that software can perfectly identify every subtly subjective sentence from wording alone. Closed factual types, interpretive-predicate rejection, source requirements and separate review states make misuse fail closed in the tested routes; ambiguous new language still requires review.

The complete suite now contains 27 passing tests. No real-person characterization was created for these tests. All examples are synthetic.
