# Phase 1 Research — Foundations and MCP contract

**Researched:** 2026-08-27
**Confidence:** HIGH

## Domain notes

Phase is greenfield scaffolding. The load-bearing external contract is jgs-archi-mcp:

- 69 MCP tools (README Available Tools catalog)
- 14 MCP resources under `archimate://` (ResourceHandler.java)
- Default HTTP MCP endpoint `http://127.0.0.1:18090/mcp`

Structural validation must be offline-capable (Archi may be down). Prefer a checked-in inventory over live tools/list during CI.

## Patterns

- One `SKILL.md` per skill directory (ZCode convention)
- Stdlib-only helpers with `unittest`
- Install script copies into `~/.zcode/skills/<name>/`

## Pitfalls for this phase

- Drifting inventory (tool renamed upstream) — document refresh procedure in docs/MCP.md
- False-positive unknown tools from hyphenated English words in skills — keep matching conservative (backticks + archimate:// URIs primarily)
- Accidentally editing jgs-archi-mcp — out of scope / NG-1

## Sources

- VISION.md, AGENTS.md
- Sibling repo jgs-archi-mcp README + ResourceHandler.java
- .planning/research/* from project init
