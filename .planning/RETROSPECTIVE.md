# Retrospective

## Milestone: v1.0 — Initial skill suite

**Shipped:** 2026-08-28
**Phases:** 5 | **Plans:** 5

### What Was Built

- Foundations: MCP inventory, structural validator, install path, docs
- Orchestrator skill with view-plan schema and confirmation gate
- Viewpoint-select + 11 specialist contract skills
- Create-path docs + compliance checklist helper
- Rationale schema + evidence layout + offline smoke

### What Worked

- Coarse vertical MVP phases mapped cleanly to OBJ-1 then foundations for OBJ-2..6
- Stdlib-only helpers with unittest gave fast offline gates
- Dual quality bar (structural + evidence convention) kept NG constraints visible

### What Was Inefficient

- Nested Agent tool unavailable on Ralph worker host; plan/execute/review ran inline
- Phase complete required padded 0N-VERIFICATION.md frontmatter before ledger accepted status
- Milestone accomplishments auto-extract was weak (SUMMARY one-liners too thin)

### Patterns Established

- Inventory JSON as offline MCP allowlist
- Schema helpers for View Plan and rationale section titles
- Specialist stubs with explicit orchestrator-only dispatch
- Confirmation gate before any MCP mutation

### Key Lessons

- Always write VERIFICATION with YAML status: passed frontmatter and dual N- / 0N- names on this GSD build
- Keep specialist depth out of first milestone if OBJ-1 is the seed
- Capture live MCP evidence as soon as Archi is available; offline smoke is not a substitute forever

### Cost Observations

- Model mix: single worker host (inline gates); specialist Agent spawns not available
- Sessions: 1 Ralph worker kick through closeout
- Notable: auto_advance_phases completed 5 phases in one kick after new-project

## Cross-Milestone Trends

| Milestone | Phases | Plans | Notes |
|-----------|--------|-------|-------|
| v1.0 | 5 | 5 | First ship; specialist depth deferred |
