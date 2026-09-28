#!/usr/bin/env python3
"""Validate a roster file and optionally inspect resolved editor-first context."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from roster.roster import RosterError, load_roster, resolve_cohort_context, resolve_context


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roster", type=Path)
    parser.add_argument("--entity")
    parser.add_argument("--cohort")
    parser.add_argument("--story")
    parser.add_argument("--as-of")
    args = parser.parse_args()
    try:
        value = load_roster(args.roster)
        if args.entity and args.cohort:
            parser.error("choose either --entity or --cohort")
        if args.entity:
            print(json.dumps(
                resolve_context(value, args.entity, story_id=args.story, as_of=args.as_of),
                indent=2,
                ensure_ascii=False,
            ))
        elif args.cohort:
            print(json.dumps(
                resolve_cohort_context(value, args.cohort, story_id=args.story, as_of=args.as_of),
                indent=2,
                ensure_ascii=False,
            ))
        else:
            print(json.dumps({
                "valid": True,
                "registryId": value["registryId"],
                "registryVersion": value["registryVersion"],
                "entities": len(value["entities"]),
                "cohorts": len(value["cohorts"]),
                "interpretiveBranches": len(value["interpretiveBranches"]),
                "editorContext": len(value["editorContext"]),
                "storyBindings": len(value["storyBindings"]),
            }))
        return 0
    except (OSError, json.JSONDecodeError, RosterError) as exc:
        print(f"invalid roster: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
