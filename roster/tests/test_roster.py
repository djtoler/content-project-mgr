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
        with self.assertRaisesRegex(RosterError, "requires evidence"):
            validate_roster(data)

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
