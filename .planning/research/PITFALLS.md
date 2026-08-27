# Pitfalls Research

**Domain:** Agent-guided ArchiMate skill suites
**Researched:** 2026-08-27
**Confidence:** HIGH

## Critical Pitfalls

### 1. Duplicating ArchiMate reference material into skills
- **Warning signs:** Large tables of element/relationship types in SKILL.md; stale copies vs MCP resources
- **Prevention:** Structural validator fails if skills embed reference dumps; skills must cite MCP resource names only
- **Phase:** Early skeleton + every specialist plan

### 2. Creating elements without inspecting the existing model
- **Warning signs:** Duplicate concepts across views; inconsistent names
- **Prevention:** Mandatory inspect-before-create step in specialist contracts (OBJ-4)
- **Phase:** First MCP write path and coherence work

### 3. Silent "fixes" of illegal relationships
- **Warning signs:** Agent rewrites user intent without explanation
- **Prevention:** Compliance path must explain violation and propose alternative (OBJ-5); never auto-apply invalid edges
- **Phase:** Compliance/QA phase

### 4. Fully autonomous architecture decisions
- **Warning signs:** Orchestrator skips confirmation of scope/interpretation
- **Prevention:** NG-3 gates; view plan presented before bulk modelling; user governs decisions
- **Phase:** Orchestrator (OBJ-1)

### 5. Coupling skills to a forked or modified MCP plugin
- **Warning signs:** PRs touching jgs-archi-mcp; hard-coded private tool names
- **Prevention:** NG-1; consume public tool/resource surface only; inventory from live MCP
- **Phase:** Contract inventory phase

### 6. Building a parallel diagramming stack
- **Warning signs:** SVG/HTML canvas, non-Archi exporters as primary path
- **Prevention:** NG-2/NG-5; Archi is only canvas
- **Phase:** All layout/presentation work

### 7. Skipping live evidence because structural checks pass
- **Warning signs:** Green unit tests, no `docs/evidence/` scenarios
- **Prevention:** Dual quality bar in VISION; one live E2E per specialist required for done
- **Phase:** Each specialist delivery phase

### 8. Scope explosion across all OBJ-3 specialists in milestone 1
- **Warning signs:** Roadmap tries to ship full specialist set before orchestrator works
- **Prevention:** SEED-001 / OBJ-1 first; coarse phases; later seeds for remaining OBJs
- **Phase:** Roadmap and milestone scoping

### 9. Third-party Python dependencies creeping in
- **Warning signs:** requirements.txt, poetry.lock
- **Prevention:** Stdlib-only policy; helpers stay small
- **Phase:** Helper introduction

### 10. Skill naming chaos / user-invoked specialists
- **Warning signs:** Many top-level slash commands; user must know which specialist to call
- **Prevention:** One user-facing orchestrator; specialists orchestrator-dispatched only
- **Phase:** Orchestrator + package layout
