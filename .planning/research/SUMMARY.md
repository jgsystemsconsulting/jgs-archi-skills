# Project Research Summary

**Project:** jgs-archi-skills
**Domain:** Agent-guided ArchiMate viewpoint creation via ZCode skills + Archi MCP
**Researched:** 2026-08-28 (v1.3 refresh for SEED-004 / OBJ-4)
**Confidence:** HIGH

## Executive Summary

v1.0–v1.2 shipped orchestrator, viewpoint grounding, full specialist suite, CREATE_PATH inspect-before-create guidance, and offline evidence. OBJ-4 needs *deterministic* coherence depth: inspect existing model content before create, reuse one element across views, minimise duplicates, keep naming consistent. Live MCP remains soft until Bridge is up.

## Key Findings

### Recommended Stack

Unchanged:

- ZCode SKILL.md + install.py
- JGS Archi Bridge MCP inventory tools only (`search-elements`, `get-or-create-element`, `find-concept-usage`, …)
- Python 3.10+ stdlib helpers for deterministic match/normalize logic
- Offline fixtures under `docs/evidence/`

### Table Stakes for v1.3

- `reuse_inspect` helper: given candidate name/type + element inventory snapshot → `reuse` | `create` | `ambiguous` with matched IDs
- `naming_convention` helper: normalize labels + detect cross-view naming conflicts
- CREATE_PATH section for reuse registry / naming policy binding
- Specialist + orchestrator hooks to call helpers and pass reuse registry in hand-off
- model-qa procedure depth for duplicates/naming using helpers
- Offline multi-view reuse evidence pack + unit tests

### Watch Out For

- Reworking v1.0–v1.2 cores beyond coherence hooks
- Embedding ArchiMate metamodel tables (NG-4)
- Silent merge of ambiguous near-matches (must surface to user)
- Skill-side durable model cache as SoT (stateless policy)
- Treating live MCP as hard gate

## Implications for Roadmap

1. Helpers first (testable offline)
2. Contract + skill wiring second
3. model-qa + evidence + regression third
