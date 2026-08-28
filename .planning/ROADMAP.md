# Roadmap: jgs-archi-skills

## Milestones

- ✅ **v1.0 Initial skill suite** — Phases 1-5 (shipped 2026-08-28)
- ✅ **v1.1 Viewpoint selection grounding** — Phases 6-8 (shipped 2026-08-28)
- ✅ **v1.2 Full specialist skill set** — Phases 9-12 (shipped 2026-08-28)
- 🔄 **v1.3 Model coherence and reuse** — Phases 13-15 (in progress)

## Overview

v1.3 deepens OBJ-4: deterministic inspect-before-create, cross-view element reuse, duplicate minimisation, and naming consistency on top of the existing suite. Do not rework v1.0 foundations, v1.1 viewpoint-select, or v1.2 specialist modelling cores beyond coherence hooks. Phase numbering continues from v1.2 (last phase was 12).

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

- [x] **Phase 13: Reuse and naming helpers** — completed 2026-08-28 — Deterministic reuse_inspect + naming_convention stdlib helpers and unit tests (COH-01..03)
- [x] **Phase 14: Contract and skill coherence binding** — completed 2026-08-28 — CREATE_PATH OBJ-4 section; specialist + orchestrator + model-qa wiring (COH-04..07)
- [x] **Phase 15: Offline evidence and regression lock** — completed 2026-08-28 — Multi-view reuse evidence pack; green suite; freeze viewpoint-select (COH-08..10)

## Phase Details

### Phase 13: Reuse and naming helpers

**Goal**: Ship offline-deterministic helpers that decide reuse vs create and enforce naming consistency without calling MCP.
**Depends on**: v1.2 complete
**Requirements**: COH-01, COH-02, COH-03
**Success Criteria** (what must be TRUE):

  1. `helpers/reuse_inspect.py` returns reuse|create|ambiguous with match IDs for inventory snapshots
  2. `helpers/naming_convention.py` normalizes names and flags cross-view conflicts
  3. Unit tests cover the decision matrix; no third-party deps

**Plans**: 1 plan

Plans:

- [x] 13-01: Implement reuse_inspect + naming_convention helpers and tests

### Phase 14: Contract and skill coherence binding

**Goal**: Bind helpers into CREATE_PATH and the live skill surfaces so every mutating path inspects, reuses, and names consistently.
**Depends on**: Phase 13
**Requirements**: COH-04, COH-05, COH-06, COH-07
**Success Criteria** (what must be TRUE):

  1. CREATE_PATH documents reuse registry, naming policy, and no silent ambiguous merge
  2. Mutating specialists reference the coherence helpers/steps and report reused vs created
  3. Orchestrator hand-off carries reuse_registry + naming_policy
  4. model-qa documents helper-backed duplicate/naming checks

**Plans**: 1 plan

Plans:

- [x] 14-01: CREATE_PATH + specialist/orchestrator/model-qa coherence wiring

### Phase 15: Offline evidence and regression lock

**Goal**: Prove multi-view reuse offline and keep the suite green without reworking frozen surfaces.
**Depends on**: Phase 14
**Requirements**: COH-08, COH-09, COH-10
**Success Criteria** (what must be TRUE):

  1. `docs/evidence/coherence-reuse-offline/` shows shared element ID across views + naming checks
  2. Full unit/structural suite green; viewpoint-select digest unchanged
  3. Evidence index/README updated; no NG violations

**Plans**: 1 plan

Plans:

- [x] 15-01: Coherence offline evidence + regression lock

## Progress

**Execution Order:** 13 → 14 → 15

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 13. Reuse and naming helpers | 1/1 | Complete    | 2026-08-28 |
| 14. Contract and skill coherence binding | 1/1 | Complete    | 2026-08-28 |
| 15. Offline evidence and regression lock | 1/1 | Complete    | 2026-08-28 |

---
*Roadmap created: 2026-08-28 for milestone v1.3 (SEED-004 / OBJ-4)*
