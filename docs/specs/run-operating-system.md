<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Spec: Run operating system for Archi specialists

Steal five operating rules from the repo-to-archi prompt into this suite. Do not steal reverse-engineering: no repo scan, no C4 onion as product, no evidence glyphs, no ISO-25010 aspect catalogue, no Mermaid-in-Archi gate, no `/repo-to-archi` skill.

## Why

Specialists already follow `docs/CREATE_PATH.md` for confirm-before-mutate, inspect-before-create, and explain-and-propose. They still finish on a created-ID table. Silent folds, remembered IDs after compaction, notes placed before layout, and a completion summary that reads as "finished" are the failures that prompt paid for. This spec makes those failures visible and testable.

## Scope

In:

- A numbered gate manifest in `docs/CREATE_PATH.md` (hedge-free, named exceptions only)
- Working mode: the open Archi model is the checkpoint; re-query IDs
- Candidate disposition grammar and an offline helper that can fail a ledger
- Light provenance on create (`stated` / `inferred` / `existing`)
- Layout footguns and render close-out in `archi-layout` plus CREATE_PATH
- Draft close-out blocks on the completion summary
- Structural skill-contract tests so specialists cannot drop the new slots

Out:

- Changing `skills/archi-viewpoint-select/SKILL.md` (frozen digest in `tests/test_specialist_contract.py`)
- Changing eval-loop `GATES.md` or requiring `Evidence:` on eval slices
- New MCP tools, new Python dependencies, copies of ArchiMate tables
- Specializations, label glyphs, or exploded `repoToArchi.coverage.*` properties

## Constraints (bind every task)

- Python 3.10+, standard library only
- Skills consume JGS Archi Bridge MCP only; tool names must exist in `docs/mcp/archi-bridge-inventory.json`
- No ArchiMate metamodel dumps in skills (VISION NG-4)
- User governs architectural decisions (VISION NG-3)
- Durable prose: technical voice, no em dashes
- Do not present first-generation modelling as finished

## Gates (CREATE_PATH, hedge-free)

| ID | Gate | Pass condition |
|----|------|----------------|
| CP-G1 | Confirm-before-mutate | No mutating MCP call unless View Plan confirmation is `approved`. |
| CP-G2 | Fresh IDs | At the start of every specialist, and after any compaction, re-query IDs with `search-elements` / `get-view-contents`. Identify unnamed notes, images, junctions, and groups by content and geometry, never by batch order. |
| CP-G3 | Disposition complete | Every candidate in the hand-off is `captured`, `folded`, `needs-user`, or `out-of-scope`. Silence is a fail. |
| CP-G4 | No invention | Every created element has `Evidence: stated \| inferred \| existing - <source>` as the first documentation line. No on-canvas element without that citation. |
| CP-G5 | Annotate last | Notes, legends, and images are the last objects placed on a view. Omit `height` on notes. Place notes with `position: below-content`. A later geometry change re-opens CP-G6. |
| CP-G6 | Render close-out | After any add, move, resize, or style on a view, including notes, the last actions are `assess-layout` (dispose every non-pass `ratingBreakdown` dimension; `partial` and `not-checked` are unverified) and an `export-view` PNG that is inspected. |
| CP-G7 | First generation is a draft | The documentation specialist ends the run at a draft checkpoint. Do not present the model as finished. |

A gate that cannot be made green ships as a named exception: which gate, which view or element, why. "Ran long" is not an exception.

Everything else in CREATE_PATH remains guidance.

Note on the evidence line: the grade separator in documentation text is a spaced hyphen or a colon, not an em dash. Canonical form:

```
Evidence: stated | inferred | existing - <source>
```

## Disposition grammar

Allowed values, exactly these four:

- `captured`: element name and a level-appropriate view in `target` (format `element @ view`)
- `folded`: parent element in `target`, one-line reason required
- `needs-user`: question in `reason`
- `out-of-scope`: why in `reason`

Helper: `helpers/disposition.py`

- Input: markdown table or JSON list of `{candidate, disposition, target, reason}`
- Output: findings list, exit 1 if any finding
- Empty ledger is a finding (`empty_ledger`) unless the allow-empty flag is set
- Unknown disposition is a finding
- Missing required target/reason per row is a finding
- Duplicate candidate names are a finding

`archi-model-qa` treats an undispositioned hand-off candidate as a finding (same severity band as an illegal edge: report, do not silent-fix).

Layer specialists that create content (motivation, capability-strategy, business, application, technology-physical, implementation-migration, traceability) must include a **Candidate disposition** table in the Specialist Result template.

## Provenance

On create, first documentation line:

```
Evidence: <grade> - <source>
```

Grades:

- `stated`: user or View Plan said it
- `inferred`: specialist deduced it (carry the elicit inference, do not upgrade)
- `existing`: already in the model, reused

Never write a bare `Rationale:` line for an inferred why. Either omit Rationale or write `Rationale (inferred):`.

Do not add «documented» / «inferred» specializations or label glyphs.

`helpers/docs_coverage.py` stays unchanged for the eval-loop path. Do not require `Evidence:` on eval slices.

`archi-elicit` already has an Inferences table. CREATE_PATH must say that inferred fields survive into specialist evidence lines; elicit skill restates that in Return to orchestrator.

## Layout footguns

Teach in CREATE_PATH and `archi-layout` only. Do not copy a layout textbook. Recipes remain source of truth.

Must state:

- Grouped or nested default for structure views with more than about 10 elements; flat needs a recorded reason
- Annotate last (CP-G5)
- Omit `height` on `add-note-to-view` / note `update-view-object`
- `position: below-content`, never `above-content`
- Junctions about 14 by 14; do not pass a layer-folder `folderId` for a Junction
- Nested hub (six or more connections): resize the hub, then `auto-route-connections`; re-route alone is inert
- Walk `ratingBreakdown`; do not sign off on `overallRating` alone
- Last action includes `export-view`; the PNG is authoritative where the metric under-counts
- Literal `&` in names and labels, never `&amp;`

Inventory: `export-view`, `update-view-object`, `add-note-to-view` already exist in `docs/mcp/archi-bridge-inventory.json`. Cite them in `archi-layout` MCP tools.

## Draft close-out

`helpers/completion_summary_schema.py` required blocks become:

1. Views Touched
2. Decisions
3. Open Questions
4. Confirmation Status
5. Specialists Run
6. Deliberately Deferred
7. Improve Next

Keep existing aliases. Add aliases: `deferred` / `deliberately deferred` → Deliberately Deferred; `improve next` / `next` → Improve Next.

Empty new blocks fail the same way empty old blocks fail. A legitimate none is the word `none`.

`archi-documentation` template and CREATE_PATH OBJ-6 text must list all seven.

`archi-orchestrator` after documentation returns must stop and ask the user to confirm, deepen, or stop. First generation is a draft (CP-G7). Decide-and-log: ask only when the choice is costly to reverse, evidence is missing, and a wrong guess wastes significant work; otherwise decide, log, and continue. More than about five open questions means under-deciding.

## Tests (offline, unittest)

- `tests/test_specialist_contract.py` asserts CREATE_PATH contains `CP-G1` through `CP-G7`, disposition tokens, and provenance line; mutating layer skills contain `Candidate disposition`; layout contains omit-height and `export-view`; documentation and orchestrator contain draft close-out markers
- `tests/test_disposition.py` covers helper pass, empty, unknown, missing fields, duplicates, markdown parse, allow-empty flag
- `tests/test_completion_summary_schema.py` updated for seven blocks; old five-block fixtures must fail
- Full `python -m unittest discover -s tests -q` stays green
- `python helpers/validate_skill_mcp_refs.py` stays exit 0
- Do not touch viewpoint-select frozen digest

## Success

A later agent following CREATE_PATH cannot treat a created-ID table as done, cannot skip note-height, and cannot call the first model finished. Helpers fail those shapes offline. No live MCP required for this change.
