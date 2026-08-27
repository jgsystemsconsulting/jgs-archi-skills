# Milestones

## v1.1 Viewpoint selection grounding (Shipped: 2026-08-28)

**Delivered:** OBJ-2 depth — deterministic viewpoint matrix, full archi-viewpoint-select body, orchestrator Step 2b wiring, offline multi-stakeholder evidence (SEED-002).

**Phases completed:** 6-8 (3 plans)

**Key accomplishments:**

- helpers/viewpoint_selection_matrix.py ranks viewpoint keys from intent axes (no metamodel copy)
- helpers/viewpoint_trace_schema.py validates Trace Table H2 + columns
- Full archi-viewpoint-select skill (trace, org-specific path, rejected alternatives)
- archi-orchestrator Step 2b dispatch before View Plan confirmation
- docs/evidence/viewpoint-selection-offline fixture + 21 tests green

**Known gaps:**

- Live Archi MCP E2E for viewpoint-select still deferred until Bridge is up
- Remaining specialist SKILL bodies still stubs (later seeds / OBJ-3+)

**Stats:** 3 phases, 3 plans; stdlib helpers + skill docs + evidence

**Git range:** feat(6) matrix helpers → docs v1.1 audit/closeout

**What's next:** Later seeds for remaining specialist depth (OBJ-3+) and live MCP evidence when available

---

## v1.0 Initial skill suite (Shipped: 2026-08-28)

**Phases completed:** 5 phases, 5 plans

**Key accomplishments:**

- MCP inventory (69 tools / 14 resources), structural skill ref validator, install.py
- User-invoked archi-orchestrator with view-plan schema and confirmation gate (OBJ-1)
- archi-viewpoint-select plus 11 other orchestrator-dispatched specialist contracts
- Create-path + compliance checklist (inspect-before-create, no silent illegal fixes)
- Rationale schema, evidence layout convention, offline orchestrator smoke

**Known gaps:**

- Live Archi MCP end-to-end transcript (EVID-01 live) still to capture when Bridge is up
- Specialist SKILL bodies are contracts/stubs; full modelling depth is v2

---
