# Milestones

## v1.5 Structured rationale depth (Shipped: 2026-08-28)

**Delivered:** OBJ-6 depth — offline rationale validation beyond bare headings, completion-summary schema, deterministic NL-change impact with must-reuse IDs; CREATE_PATH + documentation/orchestrator binding; offline evidence pack (SEED-006).

**Phases completed:** 19-21 (3 plans)

**Key accomplishments:**

- helpers/rationale_schema.py deepens empty-section + multi-view bundle checks; thin missing_headings retained
- helpers/completion_summary_schema.py (RATE-03 required blocks)
- helpers/nl_change_impact.py (affected views + must_reuse_element_ids; never mutates)
- docs/CREATE_PATH.md OBJ-6 section; archi-documentation + archi-orchestrator wiring
- docs/evidence/rationale-nl-change-offline; 59 tests green; viewpoint-select freeze held

**Known gaps:**

- Live Archi MCP E2E still deferred until Bridge is up (EVID-LIVE-*)
- Nested Agent unavailable this host; gates ran inline (degraded tier)
- Live rationale write transcript remains EVID-LIVE-03; LLM semantic NL parsing out of helper scope

**Stats:** 3 phases, 3 plans; stdlib helpers + skill docs + evidence

**Git range:** docs v1.5 start → feat(19..21) → audit/closeout

**What is next:** Live MCP evidence when Bridge available (VISION objectives 1-6 offline complete)

---

## v1.4 Compliance validation (Shipped: 2026-08-28)

**Delivered:** OBJ-5 depth — offline compliance_validate over model-slice snapshots; explain-and-propose findings; CREATE_PATH + model-qa/specialist/orchestrator binding; offline pass/fail evidence (SEED-005).

**Phases completed:** 16-18 (3 plans)

**Key accomplishments:**

- helpers/compliance_validate.py (types, relationship legality, abstraction, cross-view naming; findings with problem + proposed_alternative)
- helpers/fixtures/compliance_allowlist.json (minimal offline fixture; MCP remains live SoT)
- Thin compliance_checklist retained; 46 tests green
- docs/CREATE_PATH.md OBJ-5 section; model-qa/specialist/orchestrator compliance hooks
- docs/evidence/compliance-validation-offline pass/fail slices; viewpoint-select freeze held

**Known gaps:**

- Live Archi MCP E2E still deferred until Bridge is up (EVID-LIVE-*)
- Nested Agent unavailable this host; gates ran inline (degraded tier)
- Full metamodel completeness in fixture out of scope; batch whole-model COMP-V2-01 future

**Stats:** 3 phases, 3 plans; stdlib helper + skill docs + evidence

**Git range:** docs v1.4 start → feat(16..18) → audit/closeout

**What is next:** Later seeds for live MCP evidence and/or OBJ-6 rationale depth when Bridge available

---

## v1.3 Model coherence and reuse (Shipped: 2026-08-28)

**Delivered:** OBJ-4 depth — deterministic reuse inspect + naming helpers; CREATE_PATH coherence binding; specialist/orchestrator reuse registry; offline multi-view reuse evidence (SEED-004).

**Phases completed:** 13-15 (3 plans)

**Key accomplishments:**

- helpers/reuse_inspect.py (reuse|create|ambiguous from inventory snapshot)
- helpers/naming_convention.py (title-collapse-v1 normalize + cross-view conflict detect)
- docs/CREATE_PATH.md OBJ-4 section (reuse registry, naming policy, no silent ambiguous merge)
- Orchestrator hand-off fields reuse_registry + naming_policy; specialist + model-qa coherence hooks
- docs/evidence/coherence-reuse-offline multi-view same-ID fixtures; 38 tests green; viewpoint-select frozen

**Known gaps:**

- Live Archi MCP E2E still deferred until Bridge is up (EVID-LIVE-*)
- Nested Agent unavailable this host; gates ran inline (degraded tier)
- Fuzzy/semantic duplicate detection remains COH-V2-01 future

**Stats:** 3 phases, 3 plans; stdlib helpers + skill docs + evidence

**Git range:** docs v1.3 start → feat(13..15) → audit/closeout

**What is next:** Later seeds for live MCP evidence and/or OBJ-5 compliance depth when Bridge available

---

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
