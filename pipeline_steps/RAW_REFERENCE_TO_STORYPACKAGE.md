# Raw transcript to StoryPackage

This is the simple handoff order for adapting a reference transcript into a new
target-niche story.

| Step | Owner | Action | Output |
|---|---|---|---|
| 1 | **Content Project Manager** | Save the raw reference transcript, video URL/ID, target niche/topic and source hash. | Versioned intake |
| 2 | **Story layer** | Use the reference only for structure, pacing and narrative function. Create the new target-story outline and list research needs. | Target outline + research requests |
| 3 | **Data layer** | Research the new target story, resolve entities and return verified claims, typed values and explicit gaps. | Evidence + ClaimLedger/Data handoff |
| 4 | **Story layer** | Write the finished target-niche script from verified target-story evidence. Do not copy reference facts or entities. | Finished-script candidate |
| 5 | **Data layer** | Run `production-brief` with the finished target script plus the original reference transcript/video. Return alignment, evidence leads, B-roll briefs, animation briefs and transition notes. | Production brief marked for review |
| 6 | **Story layer + Editor** | Accept, reject or defer each brief item. Revise the script or requirements where justified. If the script changes materially, rerun Step 5. | Stable script + reconciled brief |
| 7 | **Story layer** | Build and validate the final StoryPackage with current registry, claims, obligations and typed data/media requirements. | Final versioned StoryPackage |
| 8 | **Content Project Manager** | Freeze the package hash and hand it to Matching. | Matching handoff receipt |

## Boundaries

- Data verifies facts and produces the production brief; it does not write the
  target story.
- Story owns the script and final StoryPackage.
- The production brief uses a finished script; it does not come first.
- Matching receives only the final StoryPackage, not the raw production brief.
- Production-brief evidence and footage are leads/candidates until reviewed.
- A reference video's visuals do not automatically become required treatments.

## Minimal flow

```text
raw reference transcript/video
  → Story outline
  → Data research
  → Story finished script
  → Data production brief
  → Story/editor reconciliation
  → final StoryPackage
  → Matching
```
