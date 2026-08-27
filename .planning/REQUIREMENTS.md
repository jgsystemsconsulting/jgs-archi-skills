# Requirements: jgs-archi-skills

**Defined:** 2026-08-27
**Core Value:** A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## v1 Requirements

Requirements for initial release / first milestone path. Each maps to roadmap phases.

### Foundation

- [ ] **FOUND-01**: Contributor can install the in-repo skill suite to `~/.zcode/skills/` via a documented install script
- [ ] **FOUND-02**: Structural validation helper fails when a skill references an MCP tool or resource name that is not on the known Archi Bridge surface
- [ ] **FOUND-03**: Repo documents the MCP endpoint default (`http://127.0.0.1:18090/mcp`) and that skills consume tools/resources only (no plugin modification)

### Orchestration (OBJ-1)

- [ ] **ORCH-01**: User can invoke a single orchestrator skill and provide architectural intent in plain language (problem, stakeholders, concerns, scope, current/target state, expected outcome)
- [ ] **ORCH-02**: Orchestrator produces a plain-language view plan naming viewpoints, layers, modelling sequence, dependencies, and validation points
- [ ] **ORCH-03**: View plan is usable without ArchiMate expertise (terms explained or avoided where possible; no assumption user knows element type catalogs)
- [ ] **ORCH-04**: Orchestrator keeps scope and architectural decisions visible for user confirmation (no fully autonomous commit of intent)

### Viewpoint Selection (OBJ-2)

- [ ] **VIEW-01**: Viewpoint choices in the plan are traceable to stakeholder, concern, purpose, and abstraction level
- [ ] **VIEW-02**: When no standard ArchiMate viewpoint fits, the system proposes a justified organisation-specific viewpoint that remains ArchiMate-compliant

### Specialists and Model Work (OBJ-3, OBJ-4)

- [ ] **SPEC-01**: Skill set includes (or clearly stubs with dispatch contracts for) the vision-enumerated responsibilities: elicitation, viewpoint selection, motivation, capability/strategy, business, application, technology/physical, implementation/migration, cross-layer traceability, model QA, layout/presentation, documentation/rationale
- [ ] **SPEC-02**: Specialists are orchestrator-dispatched, not separately user-invoked as the primary path
- [ ] **SPEC-03**: Before creating an element, the agent path inspects existing model content via MCP and reuses shared concepts when present
- [ ] **SPEC-04**: Naming stays consistent across views for the same concept; duplicate elements are minimised

### Compliance and Rationale (OBJ-5, OBJ-6)

- [ ] **COMP-01**: Compliance checks cover element types, relationship source/target combinations, permitted relationship types, abstraction levels, cross-view consistency, and naming
- [ ] **COMP-02**: On violation, the system explains the problem and proposes a compliant alternative rather than silently applying an illegal change
- [ ] **RATE-01**: Significant views carry structured rationale (purpose, stakeholders/concerns, viewpoint, questions answered, assumptions, decisions, exclusions, open questions) recorded in the model via MCP
- [ ] **RATE-02**: User can request natural-language changes that regenerate affected views without damaging shared model elements used elsewhere
- [ ] **RATE-03**: A modelling run ends with a completion summary the user can read

### Evidence

- [ ] **EVID-01**: At least one documented live end-to-end scenario for the orchestrator path is captured under `docs/evidence/` when MCP is available
- [ ] **EVID-02**: Evidence layout and naming convention exist so later specialists can add one live scenario each

## v2 Requirements

Deferred beyond the first coarse milestone; tracked for later seeds.

### Full specialist depth

- **SPEC-V2-01**: Every specialist has a complete SKILL.md body (not stub) and one live evidence scenario
- **SPEC-V2-02**: Layout/presentation specialist produces Archi-native layouts meeting agreed readability bar
- **SPEC-V2-03**: Cross-layer traceability specialist produces explicit traces across motivation→business→application→technology

### Advanced governance

- **GOV-V2-01**: Organisation-specific viewpoint library persistence pattern (still via model/MCP, not a side DB)
- **GOV-V2-02**: Batch compliance report across entire model

## Out of Scope

| Feature | Reason |
|---------|--------|
| Modify jgs-archi-mcp / Archi Bridge plugin | NG-1 |
| New diagramming or rendering engine | NG-2 |
| Fully autonomous architect (no user governance) | NG-3 |
| Duplicate ArchiMate language reference inside skills | NG-4 |
| Support for EA tools other than Archi | NG-5 |
| Skill-side database or durable local model cache as SoT | Stateless skills policy |
| Third-party Python dependencies | Stdlib-only policy |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Pending |
| FOUND-02 | Phase 1 | Pending |
| FOUND-03 | Phase 1 | Pending |
| ORCH-01 | Phase 2 | Pending |
| ORCH-02 | Phase 2 | Pending |
| ORCH-03 | Phase 2 | Pending |
| ORCH-04 | Phase 2 | Pending |
| VIEW-01 | Phase 3 | Pending |
| VIEW-02 | Phase 3 | Pending |
| SPEC-01 | Phase 3 | Pending |
| SPEC-02 | Phase 3 | Pending |
| SPEC-03 | Phase 4 | Pending |
| SPEC-04 | Phase 4 | Pending |
| COMP-01 | Phase 4 | Pending |
| COMP-02 | Phase 4 | Pending |
| RATE-01 | Phase 5 | Pending |
| RATE-02 | Phase 5 | Pending |
| RATE-03 | Phase 5 | Pending |
| EVID-01 | Phase 5 | Pending |
| EVID-02 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-08-27*
*Last updated: 2026-08-27 after roadmap creation*
