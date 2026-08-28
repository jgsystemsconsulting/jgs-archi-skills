# Roadmap: jgs-archi-skills

## Milestones

- ✅ **v1.0 Initial skill suite** — Phases 1-5 (shipped 2026-08-28)
- ✅ **v1.1 Viewpoint selection grounding** — Phases 6-8 (shipped 2026-08-28)
- ✅ **v1.2 Full specialist skill set** — Phases 9-12 (shipped 2026-08-28)
- ✅ **v1.3 Model coherence and reuse** — Phases 13-15 (shipped 2026-08-28)
- 🚧 **v1.4 Compliance validation** — Phases 16-18 (SEED-005 / OBJ-5)

## Overview

v1.4 deepens OBJ-5: offline-deterministic compliance validation of element types, relationship source/target combinations, permitted relationship types, abstraction levels, cross-view consistency, and naming. Violations are explained with a compliant alternative proposed; never silently applied. Build on the thin v1.0 checklist and v1.3 coherence helpers. Do not rework v1.0–v1.3 shipped cores beyond compliance hooks. Phase numbering continues from v1.3 (last phase was 15).

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

<details>
<summary>✅ v1.2 Full specialist skill set (Phases 9-12) — SHIPPED 2026-08-28</summary>

- [x] Phase 9: Shared specialist contract and elicit body
- [x] Phase 10: Core layer modelling specialists
- [x] Phase 11: Cross-cutting specialists
- [x] Phase 12: Orchestrator dispatch, evidence, regression

Archive: `.planning/milestones/v1.2-*` and `v1.2-phases/`

</details>

<details>
<summary>✅ v1.3 Model coherence and reuse (Phases 13-15) — SHIPPED 2026-08-28</summary>

- [x] Phase 13: Reuse and naming helpers
- [x] Phase 14: Contract and skill coherence binding
- [x] Phase 15: Offline evidence and regression lock

Archive: `.planning/milestones/v1.3-*` and `v1.3-phases/`

</details>

- [x] **Phase 16: Compliance validation helpers** — Deterministic offline validator + findings schema + unit tests (COMP-03..07) (completed 2026-08-28)
- [x] **Phase 17: Contract and skill compliance binding** — CREATE_PATH OBJ-5; model-qa / specialists / orchestrator wiring (COMP-08..10) (completed 2026-08-28)
- [ ] **Phase 18: Offline evidence and regression lock** — Compliance evidence pack; green suite; freeze viewpoint-select (COMP-11..13)

## Phase Details

### Phase 16: Compliance validation helpers

**Goal**: Ship offline-deterministic compliance validation over model-slice snapshots with explain-and-propose findings, without calling MCP or embedding full ArchiMate catalogs.
**Depends on**: v1.3 complete
**Requirements**: COMP-03, COMP-04, COMP-05, COMP-06, COMP-07
**Success Criteria** (what must be TRUE):

  1. Helper accepts elements/relationships/(optional) view usages + fixture allowlist and returns structured findings
  2. Checks cover element types, relationship endpoints/types, abstraction signals, cross-view naming
  3. Each finding explains the violation and proposes a compliant alternative; no silent apply; stdlib unittest coverage

**Plans**: 1 plan

Plans:

- [x] 16-01: Implement compliance validator + fixture + tests

### Phase 17: Contract and skill compliance binding

**Goal**: Bind the validator into CREATE_PATH and live skill surfaces so modelling and QA paths explain-and-propose instead of silent-fixing.
**Depends on**: Phase 16
**Requirements**: COMP-08, COMP-09, COMP-10
**Success Criteria** (what must be TRUE):

  1. CREATE_PATH documents OBJ-5 offline validator + live MCP resource checks and no silent apply
  2. model-qa and mutating specialists reference the validator / findings hand-back
  3. Orchestrator documents consumption of compliance findings in hand-off/summary

**Plans**: 1 plan

Plans:

- [x] 17-01: CREATE_PATH + model-qa/specialist/orchestrator compliance wiring

### Phase 18: Offline evidence and regression lock

**Goal**: Prove compliance validation offline and keep the suite green without reworking frozen surfaces.
**Depends on**: Phase 17
**Requirements**: COMP-11, COMP-12, COMP-13
**Success Criteria** (what must be TRUE):

  1. `docs/evidence/compliance-validation-offline/` shows pass/fail slices with explain-and-propose output
  2. Full unit/structural suite green; viewpoint-select digest unchanged; thin checklist still usable or cleanly superseded
  3. No NG violations; no rework of v1.0–v1.3 cores beyond compliance hooks

**Plans**: 1 plan

Plans:

- [ ] 18-01: Compliance offline evidence + regression lock

## Progress

**Execution Order:** 16 → 17 → 18

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 16. Compliance validation helpers | 1/1 | Complete    | 2026-08-28 |
| 17. Contract and skill compliance binding | 1/1 | Complete    | 2026-08-28 |
| 18. Offline evidence and regression lock | 0/1 | Not started | - |

---
*Roadmap created: 2026-08-28 for milestone v1.4 (SEED-005 / OBJ-5)*
