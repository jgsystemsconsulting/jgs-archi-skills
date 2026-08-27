# Phase 1 Context — Foundations and MCP contract

**Mode:** auto (Ralph / yolo) — discuss skipped; context derived from VISION + REQUIREMENTS FOUND-*.

## Locked decisions

- Delivery: ZCode skills in-repo under `skills/`, install to `~/.zcode/skills/` via Python install script
- MCP SoT: offline inventory JSON captured from jgs-archi-mcp (69 tools, 14 resources); live MCP preferred later but not required for FOUND-*
- Validator: stdlib Python scans SKILL.md for tool-like and archimate:// refs against inventory
- No plugin modification; no ArchiMate table dumps in skills
- Phase 1 does not implement orchestrator (that is Phase 2 / OBJ-1)

## Scope fences

- In: inventory, docs/MCP.md, validator+tests, install.py, README, skills/ placeholder
- Out: orchestrator skill body, specialist skills, live Archi E2E evidence (EVID-*), any jgs-archi-mcp edits

## Requirements

FOUND-01, FOUND-02, FOUND-03
