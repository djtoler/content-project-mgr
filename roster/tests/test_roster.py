import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from roster.roster import RosterError, resolve_cohort_context, resolve_context, validate_roster


EXAMPLE = ROOT / "roster" / "examples" / "example-roster.json"


def fixture():
    return json.loads(EXAMPLE.read_text())


class RosterTests(unittest.TestCase):
    def test_example_validates(self):
        self.assertEqual(validate_roster(fixture())["registryId"], "registry:synthetic-example")

    def test_story_editor_context_wins_over_global_and_fact(self):
        result = resolve_context(fixture(), "person:alex-river", story_id="story:demo")
        self.assertEqual(result["effectiveDirectives"]["character_framing"]["value"], "preparation")
        self.assertEqual(
            result["effectiveDirectives"]["character_framing"]["editorContextId"],
            "editor-context:alex-demo-story",
        )
        self.assertEqual([item["id"] for item in result["overriddenFacts"]],
                         ["claim:alex-career-framing"])
        self.assertEqual(result["supportingFacts"], [])
        self.assertIn("preparation", result["retrievalTerms"])

    def test_global_editor_context_wins_without_story(self):
        result = resolve_context(fixture(), "person:alex-river")
        self.assertEqual(result["effectiveDirectives"]["character_framing"]["value"], "discipline")
        self.assertEqual(len(result["controllingEditorContext"]), 1)

    def test_underlying_characterization_is_preserved(self):
        result = resolve_context(fixture(), "person:alex-river", story_id="story:demo")
        self.assertEqual(result["sourceCharacterizations"][0]["trait"], "competitive")
        self.assertEqual(result["sourceCharacterizations"][0]["lensType"], "self_description")
        self.assertEqual(result["overriddenFacts"][0]["claimType"], "role")

    def test_story_binding_carries_fact_and_subjective_lens_separately(self):
        binding = fixture()["storyBindings"][0]
        self.assertEqual(binding["claimIds"], ["claim:alex-career-framing"])
        self.assertEqual(binding["characterizationIds"], ["characterization:alex-competitive"])

    def test_subjective_lens_requires_explicit_label(self):
        data = fixture()
        del data["entities"][0]["characterizations"][0]["lensType"]
        with self.assertRaisesRegex(RosterError, "lensType"):
            validate_roster(data)

    def test_story_editor_context_controls_group_framing(self):
        result = resolve_cohort_context(
            fixture(), "cohort:synthetic-top-two-2026-09-28", story_id="story:demo"
        )
        self.assertEqual(result["effectiveDirectives"]["group_framing"]["value"], "collaboration")
        self.assertEqual(result["cohort"]["memberEntityIds"],
                         ["person:alex-river", "person:blair-stone"])

    def test_expired_editor_context_does_not_apply(self):
        data = fixture()
        data["editorContext"][0]["activeTo"] = "2025-01-01"
        data["editorContext"][1]["activeTo"] = "2025-01-01"
        result = resolve_context(data, "person:alex-river", story_id="story:demo", as_of="2026-09-28")
        self.assertEqual(result["controllingEditorContext"], [])
        self.assertEqual(result["supportingFacts"][0]["id"], "claim:alex-career-framing")

    def test_alias_collision_fails(self):
        data = fixture()
        data["entities"][1]["aliases"].append(
            {"value": "A River", "kind": "nickname", "reviewState": "candidate"}
        )
        with self.assertRaisesRegex(RosterError, "alias collision"):
            validate_roster(data)

    def test_dangling_cohort_member_fails(self):
        data = fixture()
        data["cohorts"][0]["memberEntityIds"].append("person:missing")
        with self.assertRaisesRegex(RosterError, "unknown members"):
            validate_roster(data)

    def test_computed_cohort_requires_replay_inputs(self):
        data = fixture()
        data["cohorts"][1]["dataSnapshotId"] = None
        with self.assertRaisesRegex(RosterError, "membershipRule and dataSnapshotId"):
            validate_roster(data)

    def test_factual_claim_requires_evidence(self):
        data = fixture()
        data["entities"][0]["factualClaims"][0]["evidenceIds"] = []
        with self.assertRaisesRegex(RosterError, "requires source-bound evidence"):
            validate_roster(data)

    def test_subjective_trait_cannot_be_a_factual_claim(self):
        data = fixture()
        claim = data["entities"][0]["factualClaims"][0]
        claim["claimType"] = "personality"
        claim["predicate"] = "character_trait"
        claim["value"] = "competitive"
        with self.assertRaisesRegex(RosterError, "invalid factual claimType"):
            validate_roster(data)

    def test_interpretive_predicate_cannot_hide_under_factual_type(self):
        data = fixture()
        claim = data["entities"][0]["factualClaims"][0]
        claim["claimType"] = "status"
        claim["predicate"] = "personality_trait"
        claim["value"] = "competitive"
        with self.assertRaisesRegex(RosterError, "interpretive"):
            validate_roster(data)

    def test_vector_similarity_cannot_support_characterization(self):
        data = fixture()
        data["entities"][0]["characterizations"][0]["evidenceIds"] = ["evidence:vector-neighbor-1"]
        with self.assertRaisesRegex(RosterError, "retrieval-lead evidence"):
            validate_roster(data)

    def test_vector_similarity_cannot_support_fact(self):
        data = fixture()
        data["entities"][0]["factualClaims"][0]["evidenceIds"] = ["evidence:vector-neighbor-1"]
        with self.assertRaisesRegex(RosterError, "retrieval-lead evidence"):
            validate_roster(data)

    def test_vector_similarity_cannot_support_observed_relationship(self):
        data = fixture()
        data["relationships"][0]["evidenceIds"] = ["evidence:vector-neighbor-1"]
        with self.assertRaisesRegex(RosterError, "retrieval-lead evidence"):
            validate_roster(data)

    def test_vector_lead_is_quarantined_from_resolved_context(self):
        data = fixture()
        validate_roster(data)
        result = resolve_context(data, "person:alex-river", story_id="story:demo")
        serialized = json.dumps(result)
        self.assertNotIn("retrieval-lead:alex-ambition", serialized)
        self.assertNotIn("evidence:vector-neighbor-1", serialized)
        self.assertEqual(data["retrievalLeads"][0]["status"], "candidate")

    def test_editor_override_must_reference_known_claim(self):
        data = fixture()
        data["editorContext"][0]["overridesClaimIds"] = ["claim:missing"]
        with self.assertRaisesRegex(RosterError, "overrides an unknown claim"):
            validate_roster(data)

    def test_story_binding_cannot_use_another_story_note(self):
        data = fixture()
        data["editorContext"][1]["scope"]["storyId"] = "story:other"
        with self.assertRaisesRegex(RosterError, "another story"):
            validate_roster(data)

    def test_json_schema_is_valid_json_and_closed_at_root(self):
        schema = json.loads((ROOT / "roster" / "entity-context.schema.json").read_text())
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
