# Project Research Summary

**Project:** jgs-archi-skills
**Domain:** Agent-guided ArchiMate viewpoint creation via ZCode skills + Archi MCP
**Researched:** 2026-08-27
**Confidence:** HIGH

## Executive Summary

This product is not a new modelling tool. It is a governed skill layer on top of the existing JGS Archi Bridge MCP and Archi canvas. Experts in this niche build thin orchestration skills that read ArchiMate resources from the MCP, elicit intent in plain language, then create and reuse model content through MCP tools while keeping the human in charge of scope and decisions.

The recommended approach is a single user-invoked orchestrator plus orchestrator-dispatched specialists, Python 3.10+ stdlib helpers for deterministic validation, and a dual quality bar (structural skill↔MCP checks plus live evidence under `docs/evidence/`). First value is OBJ-1: intent elicitation and a plain-language view plan without requiring ArchiMate expertise.

Key risks are metamodel drift (copying ArchiMate tables into skills), duplicate model elements, silent invalid relationship "fixes", and milestone-1 scope explosion across the full specialist set. Non-goals NG-1..NG-5 are hard stops.

## Key Findings

### Recommended Stack

ZCode `SKILL.md` packages, existing Archi + JGS Archi Bridge MCP (`http://127.0.0.1:18090/mcp`), and Python 3.10+ standard library helpers only. No new renderer, no skill-side database, no PyPI deps, no plugin forks.

**Core technologies:**
- ZCode skills: delivery and install surface
- Archi Bridge MCP: tools + ArchiMate resources (SoT)
- Archi: only canvas and model store
- Python stdlib helpers: viewpoint/compliance/suite validation

### Table Stakes

- Intent elicitation and plain-language view plan (OBJ-1)
- Framework-grounded viewpoint selection (OBJ-2)
- MCP create path with inspect-before-create reuse (OBJ-3/4)
- Compliance with explained alternatives (OBJ-5)
- View rationale, NL regen, completion summary (OBJ-6)
- Structural validator + live evidence + install script

### Watch Out For

- Duplicating ArchiMate reference into skills (NG-4)
- Creating without model inspection (OBJ-4)
- Silent illegal relationship fixes (OBJ-5)
- Autonomous decisions bypassing the user (NG-3)
- Shipping all specialists before orchestrator works (SEED-001 first)

## Implications for Roadmap

1. Phase for repo skeleton, MCP contract inventory, install + structural validator foundation.
2. Phase for orchestrator OBJ-1 (elicitation + view plan) as first user-visible slice — aligns SEED-001.
3. Phase for viewpoint selection grounding (OBJ-2) feeding the plan.
4. Phase for initial specialist create/reuse path and coherence (partial OBJ-3/4).
5. Later phases or later seeds: full specialist set, compliance QA depth, rationale/NL regen, evidence matrix.

Coarse granularity: 3-5 phases for the initial milestone focused on OBJ-1 readiness with foundations that unblock OBJ-2+.

## Sources

- Owner VISION.md and AGENTS.md (binding product brief)
- Existing `.planning/` Ralph seed SEED-001 → OBJ-1
- Known JGS Archi Bridge MCP surface (69 tools, 14 resources; default localhost:18090)
- GSD new-project research templates (structure only)

---
*Research synthesized: 2026-08-27*
