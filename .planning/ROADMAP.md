# Roadmap: jgs-archi-skills

## Milestones

- ✅ **v1.0 Initial skill suite** — Phases 1-5 (shipped 2026-08-28)
- ✅ **v1.1 Viewpoint selection grounding** — Phases 6-8 (shipped 2026-08-28)
- 🚧 **v1.2 Full specialist skill set** — Phases 9-12 (SEED-003 / OBJ-3)

## Overview

v1.2 deepens OBJ-3: replace remaining specialist contract stubs with complete modelling bodies that create elements, relationships, and views through the Archi MCP under user confirmation. Do not rework v1.0 foundations or v1.1 viewpoint-select. Phase numbering continues from v1.1 (last phase was 8).

## Phases

<details>
<summary>✅ v1.0 Initial skill suite (Phases 1-5) — SHIPPED 2026-08-28</summary>

- [x] Phase 1: Foundations and MCP contract
- [x] Phase 2: Orchestrator intent and view plan
- [x] Phase 3: Viewpoint grounding and specialist contracts
- [x] Phase 4: Coherence, create path, and compliance
- [x] Phase 5: Rationale, summary, and live evidence

Archive: `.planning/milestones/v1.0-*` and `v1.0-phases/`

</details>

<details>
<summary>✅ v1.1 Viewpoint selection grounding (Phases 6-8) — SHIPPED 2026-08-28</summary>

- [x] Phase 6: Viewpoint matrix and trace schema
- [x] Phase 7: Viewpoint-select skill and orchestrator wiring
- [x] Phase 8: Offline evidence and regression

Archive: `.planning/milestones/v1.1-*` and `v1.1-phases/`

</details>

- [x] **Phase 9: Shared specialist contract and elicit body** — Shared create-path binding across specialists; full `archi-elicit`; freeze viewpoint-select as done (completed 2026-08-28)
- [x] **Phase 10: Core layer modelling specialists** — Full bodies for motivation, capability/strategy, business, application, technology/physical, implementation/migration (completed 2026-08-28)
- [x] **Phase 11: Cross-cutting specialists** — Full bodies for traceability, model-qa, layout, documentation/rationale (completed 2026-08-28)
- [x] **Phase 12: Orchestrator dispatch, evidence, regression** — Post-confirm dispatch sequence, offline evidence fixtures, green suite (completed 2026-08-28)

## Phase Details

### Phase 9: Shared specialist contract and elicit body

**Goal**: Lock the shared modelling contract every specialist must follow, ship full `archi-elicit`, and explicitly leave `archi-viewpoint-select` untouched.
**Depends on**: v1.1 complete
**Requirements**: SPEC-D-01, SPEC-D-12, SPEC-D-13, SPEC-D-14, SPEC-D-15, SPEC-D-20
**Success Criteria** (what must be TRUE):

  1. A single shared create-path / governance section exists (docs and/or skill fragment) that every mutating specialist references
  2. `archi-elicit` SKILL.md is a complete procedure (not stub) and declares no MCP mutations
  3. Specialist skills still state orchestrator-dispatched only; MCP-ref validator remains green
  4. `archi-viewpoint-select` content is unchanged from v1.1 (no drive-by edits)

**Plans**: 1 plan

Plans:

- [x] 09-01: Shared specialist contract + full archi-elicit; leave viewpoint-select frozen

### Phase 10: Core layer modelling specialists

**Goal**: Replace layer-oriented stubs with complete MCP modelling procedures for the six core modelling specialists.
**Depends on**: Phase 9
**Requirements**: SPEC-D-02, SPEC-D-03, SPEC-D-04, SPEC-D-05, SPEC-D-06, SPEC-D-07
**Success Criteria** (what must be TRUE):

  1. Each of the six skills has Purpose, Inputs, MCP tools/resources, Procedure, Output/return-to-orchestrator sections
  2. Each procedure includes inspect-before-create, recipe read before non-trivial views, and compliance explain-and-propose
  3. No skill invents tool/resource names outside the inventory
  4. Structural MCP-ref check passes on the whole suite

**Plans**: 1 plan

Plans:

- [x] 10-01: Full bodies for motivation, capability-strategy, business, application, technology-physical, implementation-migration

### Phase 11: Cross-cutting specialists

**Goal**: Ship full bodies for traceability, model QA, layout/presentation, and documentation/rationale.
**Depends on**: Phase 10
**Requirements**: SPEC-D-08, SPEC-D-09, SPEC-D-10, SPEC-D-11
**Success Criteria** (what must be TRUE):

  1. Traceability skill defines how cross-layer traces are created and gap-reported
  2. Model-qa skill defines check sequence and explain-and-propose output (no silent illegal fixes)
  3. Layout skill uses inventory layout tools only (Archi canvas)
  4. Documentation skill binds rationale schema + completion summary and MCP doc-field write path

**Plans**: 1 plan

Plans:

- [x] 11-01: Full bodies for traceability, model-qa, layout, documentation

### Phase 12: Orchestrator dispatch, evidence, regression

**Goal**: Wire post-confirm specialist dispatch on the orchestrator, add offline evidence fixtures for specialist paths, keep tests green.
**Depends on**: Phase 11
**Requirements**: SPEC-D-16, SPEC-D-17, SPEC-D-18, SPEC-D-19
**Success Criteria** (what must be TRUE):

  1. Orchestrator documents post-confirm hand-off payload and specialist order/decision rules
  2. `docs/evidence/` contains offline fixtures covering deepened specialist paths (index updated)
  3. Full unit/structural suite green
  4. README points at specialist evidence layout

**Plans**: 1 plan

Plans:

- [x] 12-01: Orchestrator post-confirm dispatch + offline evidence + regression lock

## Progress

**Execution Order:** 9 → 10 → 11 → 12

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 9. Shared specialist contract and elicit body | 1/1 | Complete    | 2026-08-28 |
| 10. Core layer modelling specialists | 1/1 | Complete    | 2026-08-28 |
| 11. Cross-cutting specialists | 1/1 | Complete    | 2026-08-28 |
| 12. Orchestrator dispatch, evidence, regression | 1/1 | Complete    | 2026-08-28 |

---
*Roadmap created: 2026-08-28 for milestone v1.2 (SEED-003 / OBJ-3)*
