<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# ITERATION 1: Retest after skill and instrument improvements

Date: 2026-08-28. Fresh run: `JGS Eval Loop` wiped to verified-empty
(`transcript-reset.json`), full unattended build from the same frozen
scenario and decision record (`build-plan.json`, unchanged in content),
layout per the updated `archi-layout` skill, documentation phase, export.

## Scores (before → after)

| Dimension | Instrument | Iter-0 | Iter-1 | Exit |
|---|---|---|---|---|
| Metamodel fidelity | `compliance_validate --json` | 40 | **0** | 0 |
| Naming | `naming_convention conflicts` | 0 | **0** | 0 |
| Documentation coverage | `docs_coverage --json` | 0 (after backfill) | **0** (first pass, no backfill) | 0 |
| Layout | `layout_check --json` | 0 (after live discovery) | **0** (deterministic escalation) | 0 |
| Rationale bundle | `rationale_schema --bundle --json` | 0 | **0** | 0 |
| Completion summary | `completion_summary_schema` | pass | pass | 0 |
| Orphan elements | slice degree analysis | 0 | **0** | n/a |
| Motivation-to-technology chain | traceability view | complete | **complete** (9 objects, 8 connections) | n/a |
| Bridge layout ratings | `assess-layout` | 4 excellent, 2 good | 4 excellent, 2 good | n/a |

Measurable gains over baseline:

1. Metamodel 40 → 0: allowlist widened with live-verified types/patterns
   (instrument fix, evidence cited in fixture notes); the model itself was
   already bridge-legal, and the one illegal edge the bridge rejected during
   the baseline was corrected in the plan before this run.
2. Documentation coverage reached zero in the builder's own verified pass:
   CREATE_PATH now mandates `update-relationship` documentation and
   pre-hand-back verification; `build_model.py` enforces both
   (`verify ok: 59 elements, 73 relationships all present and documented`).
   The baseline's 12-doc backfill gap cannot recur silently.
3. Layout escalation is now encoded in the `archi-layout` skill; the run
   reproduced the good/excellent endpoint deterministically without live
   discovery.

## Skill Changes (applied since iter-0)

1. `helpers/fixtures/compliance_allowlist.json`: +14 element types,
   +12 relationship patterns, each live-verified by the bridge validator
   during iter-0; evidence note embedded in the fixture.
2. `skills/archi-layout/SKILL.md` Step 3: encoded the route escalation
   (assess → layout → terminals-only route → full route → single retry;
   target excellent, accept good only with recorded residual reason).
3. `docs/CREATE_PATH.md` live sequence: +relationship documentation rule
   (`create-relationship` has no documentation parameter; set via
   `update-relationship`), +post-condition verification rule before
   specialist hand-back.
4. `docs/eval/build_model.py`: documentation applied on reuse as well as
   create; hard post-build verification (existence + documentation) that
   fails the run instead of silently skipping.
5. `docs/eval/export_eval_slice.py`: geometry join fixed (visualMetadata is
   keyed by elementId). `helpers/layout_check.py`: null geometry handled.
   `docs/eval/reset_model.py`: correct delete parameter names.

No changes to the frozen scenario.

## Evidence

- `iter-1/transcript-reset.json`: verified-empty precondition
- `iter-1/build-plan.json`: decision record; build + verify pass (console: `verify ok: 59 elements, 73 relationships all present and documented`). Note: the confirmation run reuses the same plan path, so its transcript overwrote `iter-1/transcript-specialists.json`; the retained copy is `iter-confirm/transcript-specialists.json` (identical builder, identical plan).
- `iter-1/transcript-layout.json`: escalation steps and ratings per view
- `iter-1/findings-{compliance,naming,docs,layout,rationale}.json`: all zero/pass
- `iter-1/slice.json`, `iter-1/usages.json`, `iter-1/views.json`, `iter-1/png/`
- `iter-1/rationale/*.md`, `iter-1/completion-summary.md`
