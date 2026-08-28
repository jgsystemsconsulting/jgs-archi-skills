# ITERATION 0 — Baseline (unattended run against frozen scenario)

Date: 2026-08-28. Model: `JGS Eval Loop` (wiped to verified-empty before the
run; see `transcript-reset-rename.json`, `transcript-reset.json`). Input:
`docs/eval/reference-scenario.md` (FROZEN v1.0). Orchestrator flow per
`skills/archi-orchestrator/SKILL.md`: view plan + viewpoint trace
(schema-checked), then specialists motivation → capability-strategy →
business → application → technology → traceability → model-qa → layout →
documentation.

## Scores

| Dimension | Instrument | Result | Exit code |
|---|---|---|---|
| Metamodel fidelity | `helpers/compliance_validate.py --json slice.json` | **40 findings** | 1 |
| Naming | `helpers/naming_convention.py conflicts usages.json` | **0 conflicts** | 0 |
| Documentation coverage | `helpers/docs_coverage.py --json slice.json` | **0 findings** (after backfill, see F3) | 0 |
| Layout | `helpers/layout_check.py --json views.json` | **0 findings** (after skill escalation, see F2) | 0 |
| Rationale bundle | `helpers/rationale_schema.py --bundle rationale --json` | **0 findings** | 0 |
| Completion summary | `helpers/completion_summary_schema.py` | pass | 0 |
| Orphan elements | slice degree analysis | **0 orphans** | n/a |
| Motivation-to-technology chain | traceability view contents | **complete** (9 elements, 8 connections) | n/a |
| Bridge layout ratings (final) | `assess-layout` per view | 4 excellent, 2 good | n/a |

### F1 — Metamodel: 40 findings, all offline-allowlist gaps

The bridge's own live validator (ArchiMate 3.2 rules, error
`RELATIONSHIP_NOT_ALLOWED`) accepted every relationship in the final model;
during the build it rejected exactly one attempted edge
(Realization Goal→Outcome, valid alternatives: Influence, Association), which
was corrected to Influence in the plan. The 40 offline findings are the
fixture being narrower than the live reference:

- `element_type_known`: Assessment, Outcome missing from allowlist (4 findings)
- `relationship_endpoints_valid` (36 findings): Assessment-Inf→Driver,
  Goal-Inf→Outcome, Requirement-Real→Goal, Resource-Serv→Capability,
  Capability-Real→Requirement, BusinessProcess-Acc→BusinessObject,
  BusinessProcess-Real→Capability, ApplicationFunction-Real→ApplicationService,
  ApplicationComponent-Serv→BusinessProcess, ApplicationFunction-Real→Capability,
  Node-Assign→Artifact, Artifact-Real→ApplicationComponent

Same class as the smoke run's finding 3 (live MCP reference is the SoT; the
fixture is a captured snapshot). Fix: widen
`helpers/fixtures/compliance_allowlist.json` with these live-verified
patterns, citing the transcripts.

### F2 — Layout: skill escalation was needed and worked

First pass (`auto-layout-and-route` only): 5 of 6 views rated `fair` by the
bridge assessor (diagonal terminal segments from ELK). Following
`archi-layout` procedure with the assessor's own suggestions:
`auto-route-connections mode=terminals-only` (insufficient alone), then full
`auto-route-connections` → 4 excellent, 2 good; re-layout attempts on the 2
remaining views did not reduce their (small, structurally inherent)
crossing counts. Final state clean under `layout_check`. Fix: bake the
escalation order into the `archi-layout` skill so every run reaches
good/excellent without live discovery.

### F3 — Documentation coverage: harness gap found and fixed

12 of 73 relationships initially exported without documentation: an aborted
first build overwrote its transcript, and `get-relationships`-based
resume logic silently skipped 5 relationships (bridge query pagination
anomaly under investigation; all 73 verified present and now documented).
Fixes: builder post-build verification (every planned edge exists exactly
once and every documentation update is logged), backfill transcript retained.
Also fixed harness bugs: `export_eval_slice.py` joined geometry by the wrong
key (visualMetadata is keyed by elementId); `layout_check.py` treated
`null` geometry as present.

### F4 — Instrument gap: no coverage/layout checkers existed

New stdlib-only helpers `helpers/docs_coverage.py` (missing/placeholder/
too-short/name-restating documentation on every element and relationship)
and `helpers/layout_check.py` (overlap, containment, backward flow, layer
interleave, bridge assessor hard counts) with unit tests, proposed for the
gate set (G6, G7).

## Skill Changes (planned for iteration 1)

1. `helpers/fixtures/compliance_allowlist.json`: add Assessment, Outcome and
   the 12 live-verified relationship patterns with evidence note. (instrument)
2. `skills/archi-layout/SKILL.md`: encode the escalation sequence
   (assess → layout → route → re-assess; terminals-only when diagonal
   terminals flagged; full route when terminals-only insufficient).
3. `docs/CREATE_PATH.md`: record that `create-relationship` takes no
   documentation parameter; documentation must be set via
   `update-relationship`; require post-build existence + documentation
   verification before specialist hand-back.
4. `docs/eval/build_model.py`: post-build verification (harness).

## Evidence

- `iter-0/build-plan.json` — full decision record (59 elements, 73 relationships, 6 views)
- `iter-0/view-plan.md`, `iter-0/viewpoint-trace.md` — schema-valid
- `iter-0/transcript-*.json` — every MCP mutation recorded
- `iter-0/slice.json`, `iter-0/usages.json`, `iter-0/views.json` — exports
- `iter-0/findings-{compliance,naming,docs,layout,rationale}.json` — raw instrument output
- `iter-0/rationale/*.md` — validated bundle; `iter-0/completion-summary.md`
- `iter-0/png/` — final view exports
