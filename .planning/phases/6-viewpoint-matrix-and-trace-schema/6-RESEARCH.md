# Phase 6 Research — Viewpoint matrix and trace schema

**Date:** 2026-08-28
**Scope:** VSEL-01..03, VSEL-05

## Findings

- v1.0 shipped contract-only `archi-viewpoint-select` and no matrix helper despite VISION/Implementation Direction naming "viewpoint selection matrix".
- Existing helper pattern: small stdlib CLI + `tests/test_*.py` (view_plan_schema, rationale_schema, compliance_checklist).
- MCP SoT for viewpoint definitions: `archimate://recipes/*`, `archimate://reference/archimate-view-patterns`. Matrix must store **keys + axis tags only**, not element catalogs (NG-4).
- Intent axes for OBJ-2: stakeholder, concern, purpose, abstraction_level.
- Trace Table columns already fixed in skill stub: Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Standard? | Justification.

## Approach

1. `helpers/viewpoint_selection_matrix.py` — load built-in candidate table (keys/axes), score intent JSON, emit ranked JSON.
2. `helpers/viewpoint_trace_schema.py` — validate markdown Trace Table has required H2 + header columns (mirror view_plan_schema).
3. Unit tests with pass/fail fixtures; no live MCP.

## Non-goals this phase

Skill body expansion and orchestrator wiring (Phase 7). Evidence pack (Phase 8).
