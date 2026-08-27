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

## Milestone: v1.1 — Viewpoint selection grounding

**Shipped:** 2026-08-28
**Phases:** 6-8 | **Plans:** 3
**Seed:** SEED-002 / OBJ-2

### What Was Built

- viewpoint_selection_matrix + viewpoint_trace_schema stdlib helpers
- Full archi-viewpoint-select skill body (trace, org-specific, rejected alternatives)
- Orchestrator Step 2b grounding before confirmation gate
- Offline multi-stakeholder evidence under docs/evidence/viewpoint-selection-offline/
- 21 unit tests green; MCP ref validator clean

### What Worked

- Continuing phase numbers (6-8) kept archive continuity with v1.0
- Axis/key-only matrix avoided NG-4 metamodel copy while still testable offline
- Reusing view_plan_schema pattern for trace schema kept helper UX consistent
- autoCloseout audit-passed checkpoint unblocked close without inventing verdicts

### What Was Inefficient

- Nested Agent tool still unavailable; all gates ran inline (degraded tier)
- Shell/heredoc quoting friction writing multi-file helpers on Windows
- milestone.complete auto-extract of accomplishments was weak (complete x3); fixed manually in MILESTONES.md
- Skill name in backticks tripped MCP tool scanner (false positive)

### Patterns Established

- Matrix helper + schema helper pair for deterministic OBJ slices
- Orchestrator Step 2b specialist hand-off before confirmation
- Offline evidence pack: intent JSON to matrix JSON to trace md to view-plan md
- Avoid backtick-wrapping internal skill names that match tool-name regex

### Key Lessons

- Prefer labels over skill-name backticks when scanner treats hyphenated tokens as MCP tools
- Always dual-write N-VERIFICATION.md and 0N-VERIFICATION.md with status: passed frontmatter before phase.complete
- milestone.complete needs human polish of MILESTONES accomplishments after auto archive

### Cost Observations

- Model mix: single worker host inline (no nested Agent tokens)
- Sessions: SEED-002 kick + resume after complete checkpoint

## Cross-Milestone Trends

| Milestone | Phases | Plans | Notes |
|-----------|--------|-------|-------|
| v1.0 | 5 | 5 | First ship; specialist depth deferred |
| v1.1 | 3 | 3 | OBJ-2 depth; offline-only evidence |

## Milestone: v1.2 — Full specialist skill set

**Shipped:** 2026-08-28
**Phases:** 9-12 | **Plans:** 4
**Seed:** SEED-003 / OBJ-3

### What Was Built

- Shared CREATE_PATH specialist modelling contract
- Full archi-elicit body (non-mutating)
- Six core layer specialist modelling bodies
- Four cross-cutting specialists (traceability, model-qa, layout, documentation)
- Orchestrator Step 5 post-confirm dispatch + hand-off payload
- Offline specialist-suite evidence; 26 tests; viewpoint-select frozen

### What Worked

- Template-driven layer skills kept inventory tool names consistent
- Freeze hash test prevented accidental v1.1 rework
- autoCloseout audit-passed checkpoint again unblocked closeout
- Phase numbering continued 9-12 without reset

### What Was Inefficient

- Nested Agent still unavailable; entire master-flow degraded inline
- Shell heredoc/quoting friction on Windows for multi-file writes
- Skill-name backticks still trip MCP-ref scanner (fixed again)
- milestone.complete auto-accomplishments weak (manual polish)

### Patterns Established

- CREATE_PATH as single shared mutating contract
- Specialist Result hand-back template across layer skills
- Post-confirm default dispatch order on orchestrator
- Offline specialist evidence pack under docs/evidence/specialist-suite-offline/

### Key Lessons

- Never backtick internal skill package names if TOOL_BT regex scans them as MCP tools
- Keep SPEC-D freeze requirements with a content hash test
- Dual N-/0N-VERIFICATION.md with status: passed remains required before phase.complete

### Cost Observations

- Model mix: single worker host inline (no nested Agent tokens)
- Sessions: SEED-003 kick + resume after complete checkpoint

## Cross-Milestone Trends

| Milestone | Phases | Plans | Notes |
|-----------|--------|-------|-------|
| v1.0 | 5 | 5 | First ship; specialist depth deferred |
| v1.1 | 3 | 3 | OBJ-2 depth; offline-only evidence |
| v1.2 | 4 | 4 | OBJ-3 full specialist bodies; live MCP still deferred |
