# Milestones

## v1.2 Full specialist skill set (Shipped: 2026-08-28)

**Delivered:** OBJ-3 depth — full specialist SKILL bodies for all vision-enumerated responsibilities; shared CREATE_PATH contract; orchestrator post-confirm dispatch; offline specialist evidence (SEED-003).

**Phases completed:** 9-12 (4 plans)

**Key accomplishments:**

- docs/CREATE_PATH.md shared specialist modelling contract (confirmation gate, SPEC-02, NG-4)
- Full archi-elicit intent normalizer (non-mutating)
- Six core layer modelling specialists (motivation, capability-strategy, business, application, technology-physical, implementation-migration)
- Four cross-cutting specialists (traceability, model-qa, layout, documentation)
- archi-orchestrator Step 5 post-confirm hand-off payload + dispatch order
- docs/evidence/specialist-suite-offline fixtures; 26 tests green; viewpoint-select frozen from v1.1

**Known gaps:**

- Live Archi MCP E2E still deferred until Bridge is up (EVID-LIVE-*)
- Nested Agent unavailable this host; gates ran inline (degraded tier)

**Stats:** 4 phases, 4 plans; specialist skill docs + contract + evidence

**Git range:** docs v1.2 start → feat(9..12) → audit/closeout

**What is next:** Later seeds for live MCP evidence (OBJ-4+ coherence depth optional) when Bridge available

---

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
