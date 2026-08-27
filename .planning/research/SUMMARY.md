# Project Research Summary

**Project:** jgs-archi-skills
**Domain:** Agent-guided ArchiMate viewpoint creation via ZCode skills + Archi MCP
**Researched:** 2026-08-28 (v1.2 refresh for SEED-003 / OBJ-3)
**Confidence:** HIGH

## Executive Summary

v1.0 and v1.1 already shipped the orchestrator, viewpoint grounding, shared create-path docs, compliance helpers, and twelve specialist contracts. OBJ-3 still needs full modelling bodies for the eleven non-viewpoint specialists so each can create elements, relationships, and views through the Archi MCP after user confirmation.

No stack change. Stay on ZCode skills, Archi Bridge MCP inventory, Python 3.10+ stdlib helpers, offline structural gates, and offline evidence fixtures. Live MCP E2E remains soft until Bridge is up.

## Key Findings

### Recommended Stack

Unchanged from v1.0:

- ZCode SKILL.md packages installed via install.py
- JGS Archi Bridge MCP (http://127.0.0.1:18090/mcp) as sole model I/O
- Archi as only canvas
- Stdlib helpers for schema/compliance/manifest/MCP-ref validation

### Table Stakes for v1.2

- Full specialist bodies for elicit + six layer specialists + four cross-cutting specialists
- Shared create-path binding (inspect-before-create, recipe reads, explain-and-propose)
- Orchestrator post-confirm dispatch sequence and hand-off payload
- Offline evidence fixtures per specialist path
- Green MCP-ref + unit suite; viewpoint-select frozen

### Watch Out For

- Reworking v1.0/v1.1 surfaces instead of extending them
- Copying ArchiMate tables into skill bodies (NG-4)
- Making specialists user-invoked (SPEC-02)
- Treating live MCP as a hard gate while Bridge is unavailable
- Silent illegal relationship fixes in model-qa or layer skills

## Implications for Roadmap

1. Phase 9: shared contract + elicit + freeze viewpoint-select
2. Phase 10: six core layer modelling specialists
3. Phase 11: traceability, model-qa, layout, documentation
4. Phase 12: orchestrator dispatch wiring + offline evidence + regression

Coarse granularity matches prior milestones (one plan per phase).

## Sources

- VISION.md OBJ-3 and NG-1..NG-5
- Existing skills stubs + archi-viewpoint-select gold body
- docs/CREATE_PATH.md, docs/MCP.md, inventory JSON
- v1.0/v1.1 archives and retrospectives

---
*Research synthesized: 2026-08-28 for v1.2*
