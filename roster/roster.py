"""Semantic validation and deterministic editor-first context resolution."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any


class RosterError(ValueError):
    """Raised when a roster violates the shared contract."""


ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
ROOT_LISTS = (
    "sources",
    "evidence",
    "entities",
    "relationships",
    "cohorts",
    "editorContext",
    "storyBindings",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RosterError(message)


def _id_map(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        _require(isinstance(item, dict), f"{label} entries must be objects")
        item_id = item.get("id")
        _require(isinstance(item_id, str) and ID_RE.fullmatch(item_id) is not None,
                 f"{label} entry has invalid id: {item_id!r}")
        _require(item_id not in result, f"duplicate {label} id: {item_id}")
        result[item_id] = item
    return result


def _normalize_alias(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def _parse_date(value: str | None, field: str) -> date | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise RosterError(f"{field} must be an ISO date") from exc


def _parse_datetime(value: str, field: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise RosterError(f"{field} must be an ISO date-time") from exc


def _active(record: dict[str, Any], as_of: date) -> bool:
    start = _parse_date(record.get("activeFrom", record.get("validFrom")), "start date")
    end = _parse_date(record.get("activeTo", record.get("validTo")), "end date")
    return (start is None or start <= as_of) and (end is None or as_of <= end)


def validate_roster(roster: dict[str, Any]) -> dict[str, Any]:
    """Validate references and semantics that JSON Schema cannot enforce alone."""

    _require(isinstance(roster, dict), "roster must be an object")
    _require(roster.get("schemaVersion") == "1.0.0", "unsupported schemaVersion")
    for field in ("registryId", "registryVersion", "generatedAt"):
        _require(isinstance(roster.get(field), str) and roster[field], f"missing {field}")
    _parse_datetime(roster["generatedAt"], "generatedAt")
    for field in ROOT_LISTS:
        _require(isinstance(roster.get(field), list), f"{field} must be an array")

    sources = _id_map(roster["sources"], "source")
    evidence = _id_map(roster["evidence"], "evidence")
    entities = _id_map(roster["entities"], "entity")
    relationships = _id_map(roster["relationships"], "relationship")
    cohorts = _id_map(roster["cohorts"], "cohort")
    editor = _id_map(roster["editorContext"], "editorContext")

    all_ids: dict[str, str] = {}
    for kind, mapping in (
        ("source", sources), ("evidence", evidence), ("entity", entities),
        ("relationship", relationships), ("cohort", cohorts), ("editorContext", editor),
    ):
        for item_id in mapping:
            _require(item_id not in all_ids,
                     f"id {item_id} is reused by {all_ids.get(item_id)} and {kind}")
            all_ids[item_id] = kind

    for item in evidence.values():
        _require(item.get("sourceId") in sources,
                 f"evidence {item['id']} references unknown source {item.get('sourceId')}")
        _require(bool(item.get("locator")) and bool(item.get("quote")),
                 f"evidence {item['id']} requires locator and quote")

    claim_map: dict[str, dict[str, Any]] = {}
    characterization_map: dict[str, dict[str, Any]] = {}
    alias_owner: dict[str, str] = {}
    for entity in entities.values():
        _require(entity.get("type") in {"person", "organization", "work", "place", "event", "other"},
                 f"entity {entity['id']} has invalid type")
        _require(bool(entity.get("canonicalName")), f"entity {entity['id']} requires canonicalName")
        for alias in [{"value": entity["canonicalName"]}, *entity.get("aliases", [])]:
            value = alias.get("value")
            _require(isinstance(value, str) and value.strip(), f"entity {entity['id']} has empty alias")
            normalized = _normalize_alias(value)
            _require(normalized, f"entity {entity['id']} has unusable alias {value!r}")
            owner = alias_owner.get(normalized)
            _require(owner in (None, entity["id"]),
                     f"alias collision for {value!r}: {owner} and {entity['id']}")
            alias_owner[normalized] = entity["id"]

        for claim in entity.get("factualClaims", []):
            claim_id = claim.get("id")
            _require(isinstance(claim_id, str) and ID_RE.fullmatch(claim_id) is not None,
                     f"entity {entity['id']} has invalid claim id")
            _require(claim_id not in claim_map and claim_id not in all_ids,
                     f"duplicate claim id: {claim_id}")
            _require(claim.get("status") in {"reviewed", "machine_candidate", "contested"},
                     f"claim {claim_id} has invalid status")
            refs = claim.get("evidenceIds")
            _require(isinstance(refs, list) and refs, f"claim {claim_id} requires evidence")
            _require(all(ref in evidence for ref in refs), f"claim {claim_id} has unknown evidence")
            _active(claim, date.today())
            claim_map[claim_id] = {**claim, "entityId": entity["id"]}

        for item in entity.get("characterizations", []):
            item_id = item.get("id")
            _require(isinstance(item_id, str) and ID_RE.fullmatch(item_id) is not None,
                     f"entity {entity['id']} has invalid characterization id")
            _require(item_id not in characterization_map and item_id not in claim_map and item_id not in all_ids,
                     f"duplicate characterization id: {item_id}")
            _require(item.get("status") in {"reviewed", "machine_candidate", "contested"},
                     f"characterization {item_id} has invalid status")
            refs = item.get("evidenceIds")
            _require(isinstance(refs, list) and refs,
                     f"characterization {item_id} requires evidence")
            _require(all(ref in evidence for ref in refs),
                     f"characterization {item_id} has unknown evidence")
            _require(bool(item.get("trait")) and bool(item.get("statement")) and bool(item.get("attributedTo")),
                     f"characterization {item_id} requires trait, statement and attribution")
            _active(item, date.today())
            characterization_map[item_id] = {**item, "entityId": entity["id"]}

    for relation in relationships.values():
        entity_refs = relation.get("sourceEntityIds", []) + relation.get("targetEntityIds", [])
        _require(entity_refs and all(ref in entities for ref in entity_refs),
                 f"relationship {relation['id']} has unknown or missing entity references")
        evidence_refs = relation.get("evidenceIds")
        _require(isinstance(evidence_refs, list) and evidence_refs,
                 f"relationship {relation['id']} requires evidence")
        _require(all(ref in evidence for ref in evidence_refs),
                 f"relationship {relation['id']} has unknown evidence")
        _active(relation, date.today())

    for cohort in cohorts.values():
        members = cohort.get("memberEntityIds")
        _require(isinstance(members, list) and len(members) == len(set(members)),
                 f"cohort {cohort['id']} memberEntityIds must be unique")
        _require(all(ref in entities for ref in members),
                 f"cohort {cohort['id']} has unknown members")
        _require(bool(cohort.get("definition")) and bool(cohort.get("version")),
                 f"cohort {cohort['id']} requires definition and version")
        _require(all(ref in evidence for ref in cohort.get("evidenceIds", [])),
                 f"cohort {cohort['id']} has unknown evidence")
        if cohort.get("kind") in {"computed", "story_specific"}:
            _require(bool(cohort.get("membershipRule")) and bool(cohort.get("dataSnapshotId")),
                     f"cohort {cohort['id']} requires membershipRule and dataSnapshotId")

    for note in editor.values():
        _require(note.get("status") in {"active", "superseded"},
                 f"editor context {note['id']} has invalid status")
        _require(bool(note.get("author")) and bool(note.get("instruction")),
                 f"editor context {note['id']} requires author and instruction")
        _parse_datetime(note.get("createdAt"), f"editor context {note['id']} createdAt")
        _require(all(ref in entities for ref in note.get("entityIds", [])),
                 f"editor context {note['id']} has unknown entity")
        _require(all(ref in cohorts for ref in note.get("cohortIds", [])),
                 f"editor context {note['id']} has unknown cohort")
        scope = note.get("scope", {})
        _require(scope.get("kind") in {"global", "story"},
                 f"editor context {note['id']} has invalid scope")
        if scope.get("kind") == "story":
            _require(bool(scope.get("storyId")),
                     f"story-scoped editor context {note['id']} requires storyId")
        directives = note.get("directives")
        _require(isinstance(directives, list), f"editor context {note['id']} directives must be an array")
        keys = [item.get("key") for item in directives if isinstance(item, dict)]
        _require(len(keys) == len(directives) and all(isinstance(key, str) and key for key in keys),
                 f"editor context {note['id']} has invalid directive")
        _require(len(keys) == len(set(keys)),
                 f"editor context {note['id']} repeats a directive key")
        _require(all(ref in claim_map for ref in note.get("overridesClaimIds", [])),
                 f"editor context {note['id']} overrides an unknown claim")
        _active(note, date.today())

    story_ids: set[str] = set()
    for binding in roster["storyBindings"]:
        story_id = binding.get("storyId")
        _require(isinstance(story_id, str) and ID_RE.fullmatch(story_id) is not None,
                 "story binding has invalid storyId")
        _require(story_id not in story_ids, f"duplicate story binding: {story_id}")
        story_ids.add(story_id)
        checks = (
            ("entityIds", entities), ("cohortIds", cohorts),
            ("relationshipIds", relationships), ("claimIds", claim_map),
            ("characterizationIds", characterization_map), ("evidenceIds", evidence),
            ("editorContextIds", editor),
        )
        for field, known in checks:
            refs = binding.get(field)
            _require(isinstance(refs, list) and len(refs) == len(set(refs)),
                     f"story {story_id} {field} must be a unique array")
            _require(all(ref in known for ref in refs),
                     f"story {story_id} {field} contains an unknown reference")
        for note_id in binding["editorContextIds"]:
            scope = editor[note_id]["scope"]
            _require(scope["kind"] == "global" or scope.get("storyId") == story_id,
                     f"story {story_id} references editor context for another story")

    return roster


def resolve_context(
    roster: dict[str, Any],
    entity_id: str,
    *,
    story_id: str | None = None,
    as_of: str | date | None = None,
) -> dict[str, Any]:
    """Resolve editor-first context while preserving factual evidence."""

    validate_roster(roster)
    entities = {item["id"]: item for item in roster["entities"]}
    _require(entity_id in entities, f"unknown entity: {entity_id}")
    if as_of is None:
        active_date = date.today()
    elif isinstance(as_of, date):
        active_date = as_of
    else:
        active_date = _parse_date(as_of, "as_of")
        assert active_date is not None

    entity = entities[entity_id]
    facts = [item for item in entity["factualClaims"] if _active(item, active_date)]
    characterizations = [item for item in entity["characterizations"] if _active(item, active_date)]

    notes = []
    for note in roster["editorContext"]:
        if note["status"] != "active" or entity_id not in note["entityIds"] or not _active(note, active_date):
            continue
        scope = note["scope"]
        if scope["kind"] == "story" and scope.get("storyId") != story_id:
            continue
        notes.append(note)

    def note_rank(note: dict[str, Any]) -> tuple[int, datetime, str]:
        return (1 if note["scope"]["kind"] == "story" else 0,
                _parse_datetime(note["createdAt"], "createdAt"), note["id"])

    notes.sort(key=note_rank, reverse=True)
    overridden_claim_ids = {claim_id for note in notes for claim_id in note["overridesClaimIds"]}
    directive_winners: dict[str, dict[str, Any]] = {}
    shadowed_directives: list[dict[str, Any]] = []
    for note in notes:
        for directive in note["directives"]:
            enriched = {**directive, "editorContextId": note["id"], "scope": note["scope"]}
            if directive["key"] not in directive_winners:
                directive_winners[directive["key"]] = enriched
            else:
                shadowed_directives.append(enriched)

    reviewed_facts = [item for item in facts if item["status"] == "reviewed"]
    machine_facts = [item for item in facts if item["status"] == "machine_candidate"]
    contested_facts = [item for item in facts if item["status"] == "contested"]
    return {
        "entityId": entity_id,
        "storyId": story_id,
        "asOf": active_date.isoformat(),
        "authorityOrder": [
            "story_scoped_editor_context",
            "global_editor_context",
            "reviewed_factual_context",
            "machine_derived_candidates",
        ],
        "controllingEditorContext": notes,
        "effectiveDirectives": directive_winners,
        "shadowedEditorDirectives": shadowed_directives,
        "retrievalTerms": list(dict.fromkeys(
            term for note in notes for term in note.get("retrievalTerms", [])
        )),
        "supportingFacts": [item for item in reviewed_facts if item["id"] not in overridden_claim_ids],
        "overriddenFacts": [item for item in facts if item["id"] in overridden_claim_ids],
        "machineCandidates": machine_facts,
        "contestedFacts": contested_facts,
        "sourceCharacterizations": characterizations,
    }


def resolve_cohort_context(
    roster: dict[str, Any],
    cohort_id: str,
    *,
    story_id: str | None = None,
    as_of: str | date | None = None,
) -> dict[str, Any]:
    """Resolve manual editor context for a persistent or computed group."""

    validate_roster(roster)
    cohorts = {item["id"]: item for item in roster["cohorts"]}
    _require(cohort_id in cohorts, f"unknown cohort: {cohort_id}")
    if as_of is None:
        active_date = date.today()
    elif isinstance(as_of, date):
        active_date = as_of
    else:
        active_date = _parse_date(as_of, "as_of")
        assert active_date is not None

    notes = []
    for note in roster["editorContext"]:
        if note["status"] != "active" or cohort_id not in note["cohortIds"] or not _active(note, active_date):
            continue
        scope = note["scope"]
        if scope["kind"] == "story" and scope.get("storyId") != story_id:
            continue
        notes.append(note)

    def note_rank(note: dict[str, Any]) -> tuple[int, datetime, str]:
        return (1 if note["scope"]["kind"] == "story" else 0,
                _parse_datetime(note["createdAt"], "createdAt"), note["id"])

    notes.sort(key=note_rank, reverse=True)
    directive_winners: dict[str, dict[str, Any]] = {}
    shadowed_directives: list[dict[str, Any]] = []
    for note in notes:
        for directive in note["directives"]:
            enriched = {**directive, "editorContextId": note["id"], "scope": note["scope"]}
            if directive["key"] not in directive_winners:
                directive_winners[directive["key"]] = enriched
            else:
                shadowed_directives.append(enriched)

    return {
        "cohortId": cohort_id,
        "storyId": story_id,
        "asOf": active_date.isoformat(),
        "authorityOrder": [
            "story_scoped_editor_context",
            "global_editor_context",
            "reviewed_cohort_definition",
            "machine_derived_candidates",
        ],
        "cohort": cohorts[cohort_id],
        "controllingEditorContext": notes,
        "effectiveDirectives": directive_winners,
        "shadowedEditorDirectives": shadowed_directives,
        "retrievalTerms": list(dict.fromkeys(
            term for note in notes for term in note.get("retrievalTerms", [])
        )),
    }


def load_roster(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        value = json.load(handle)
    return validate_roster(value)
