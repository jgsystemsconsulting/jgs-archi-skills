
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
