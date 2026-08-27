# Requirements: jgs-archi-skills

**Defined:** 2026-08-28
**Milestone:** v1.1 Viewpoint selection grounding (SEED-002 / OBJ-2)
**Core Value:** A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## v1.1 Requirements

Requirements for this milestone only. v1.0 REQUIREMENTS remain archived under `.planning/milestones/v1.0-REQUIREMENTS.md`.

### Viewpoint matrix (deterministic helper)

- [ ] **VSEL-01**: Contributor can run a stdlib helper that accepts structured intent axes (stakeholder roles, concerns, purpose, abstraction level) and returns ranked candidate viewpoint keys without embedding ArchiMate element/relationship catalogs
- [ ] **VSEL-02**: Matrix data is fixture/key-based (IDs and axes only); full viewpoint definitions stay on MCP resources (`archimate://recipes/*`, `archimate://reference/archimate-view-patterns`)
- [ ] **VSEL-03**: Helper exits non-zero on malformed input and prints a clear error; valid input exits 0 with stable, testable output (JSON and/or markdown table)

### Trace table and org-specific path

- [ ] **VSEL-04**: `archi-viewpoint-select` produces a Viewpoint Trace Table with columns for Viewpoint, Stakeholder, Concern, Purpose, Abstraction, Standard?, Justification
- [ ] **VSEL-05**: A stdlib schema helper validates a Trace Table markdown/JSON artifact the same way `view_plan_schema.py` validates View Plans
- [ ] **VSEL-06**: When no standard candidate fits above a documented threshold, the skill proposes an organisation-specific viewpoint with explicit justification and ArchiMate-compliance constraints (no illegal layer/element mixes; no silent metamodel invention)
- [ ] **VSEL-07**: Rejected alternatives are listed so the user can see why other viewpoints were not chosen (NG-3 visibility)

### Orchestrator integration

- [ ] **VSEL-08**: `archi-orchestrator` dispatches (or documents the exact hand-off to) `archi-viewpoint-select` after intent elicitation and before final View Plan confirmation
- [ ] **VSEL-09**: View Plan **Proposed Viewpoints** section is consistent with the Trace Table (same viewpoint names and abstraction levels); schema check still passes
- [ ] **VSEL-10**: Viewpoint selection path performs **no MCP mutations** (read resources only); user confirmation gate remains before any model creates

### Evidence and regression

- [ ] **VSEL-11**: Offline fixture under `docs/evidence/` demonstrates intent axes → matrix → trace table → view-plan headings for at least one multi-stakeholder scenario
- [ ] **VSEL-12**: Unit tests cover matrix ranking, schema validation (pass and fail), and skill MCP-ref structural check; full suite remains green

## Future Requirements (not this milestone)

### Other specialist depth

- **SPEC-V2-01**: Every remaining specialist has a complete SKILL.md body and one live evidence scenario
- **SPEC-V2-02**: Layout/presentation specialist produces Archi-native layouts meeting agreed readability bar
- **SPEC-V2-03**: Cross-layer traceability specialist produces explicit traces across motivation→business→application→technology

### Advanced governance

- **GOV-V2-01**: Organisation-specific viewpoint library persistence pattern (still via model/MCP, not a side DB)
- **GOV-V2-02**: Batch compliance report across entire model

### Live evidence

- **EVID-LIVE-01**: Live Archi MCP end-to-end transcript for orchestrator + viewpoint-select when Bridge is available

## Out of Scope

| Feature | Reason |
|---------|--------|
| Modify jgs-archi-mcp / Archi Bridge plugin | NG-1 |
| New diagramming or rendering engine | NG-2 |
| Fully autonomous architect (no user governance) | NG-3 |
| Duplicate ArchiMate language reference inside skills/helpers | NG-4 |
| Support for EA tools other than Archi | NG-5 |
| Skill-side database or durable local model cache as SoT | Stateless skills policy |
| Third-party Python dependencies | Stdlib-only policy |
| Full bodies for non-viewpoint specialists | Later seeds (OBJ-3+) |
| Live Archi E2E as hard gate for v1.1 | Offline fixtures sufficient; live when Bridge up |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| VSEL-01 | Phase 6 | Pending |
| VSEL-02 | Phase 6 | Pending |
| VSEL-03 | Phase 6 | Pending |
| VSEL-04 | Phase 7 | Pending |
| VSEL-05 | Phase 6 | Pending |
| VSEL-06 | Phase 7 | Pending |
| VSEL-07 | Phase 7 | Pending |
| VSEL-08 | Phase 7 | Pending |
| VSEL-09 | Phase 7 | Pending |
| VSEL-10 | Phase 7 | Pending |
| VSEL-11 | Phase 8 | Pending |
| VSEL-12 | Phase 8 | Pending |

**Coverage:**
- v1.1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0

---
*Requirements defined: 2026-08-28*
*Last updated: 2026-08-28 after SEED-002 new-milestone*
