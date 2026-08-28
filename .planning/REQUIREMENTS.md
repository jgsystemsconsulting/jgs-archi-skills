# Requirements: jgs-archi-skills

**Defined:** 2026-08-28
**Milestone:** v1.4 Compliance validation (SEED-005 / OBJ-5)
**Core Value:** A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## v1.4 Requirements

Requirements for this milestone only. Prior REQUIREMENTS remain under `.planning/milestones/v1.0-REQUIREMENTS.md` through `v1.3-REQUIREMENTS.md`.

### Compliance validation helpers

- [x] **COMP-03**: Stdlib helper deepens offline compliance beyond boolean checklist: accepts a model-slice snapshot (elements, relationships, optional view usages) plus an allowlist/fixture of known types and permitted relationship patterns; returns structured findings; no MCP calls inside the helper; no third-party deps
- [x] **COMP-04**: Validator checks element types against the fixture allowlist (unknown/illegal type → finding); fixture is a captured reference snapshot under `docs/` or `helpers/fixtures/`, not a skill-owned ArchiMate catalog dump (NG-4)
- [x] **COMP-05**: Validator checks relationship source/target type combinations and relationship type permission against the fixture; illegal combo or type → finding
- [x] **COMP-06**: Validator checks abstraction-level consistency signals and cross-view naming consistency (may call or mirror `naming_convention` helpers); inconsistent abstraction or naming → finding
- [x] **COMP-07**: Every finding includes: check id, object refs, problem explanation, and at least one proposed compliant alternative; helper never mutates the model or auto-applies fixes (COMP-02 / NG-3)

### Contract and skill binding

- [x] **COMP-08**: `docs/CREATE_PATH.md` gains an OBJ-5 compliance-depth section: when to run offline validator vs live MCP resource checks; findings must explain-and-propose; never silent-apply
- [x] **COMP-09**: `archi-model-qa` procedure binds the deepened validator (and retains coherence helpers); mutating specialists document optional pre-create/post-create compliance check + hand-back of compliance findings
- [x] **COMP-10**: `archi-orchestrator` hand-off/summary path documents consuming model-qa compliance findings (no new mutating tools)

### Evidence and freeze

- [ ] **COMP-11**: Offline evidence under `docs/evidence/compliance-validation-offline/` shows pass and fail slices with explain-and-propose findings (types, illegal relationship, naming/abstraction)
- [ ] **COMP-12**: Full unit/structural suite green; `archi-viewpoint-select` remains frozen at the v1.1 digest; existing `compliance_checklist` thin gate remains usable or is clearly superseded without breaking callers
- [ ] **COMP-13**: No rework of v1.0–v1.3 shipped cores beyond compliance hooks; NG-1..5 respected

## Future Requirements (not this milestone)

### Live evidence hard gate

- **EVID-LIVE-01**: Live Archi MCP end-to-end transcript for orchestrator + multi-specialist modelling when Bridge is available
- **EVID-LIVE-02**: One live evidence scenario per specialist against a real Archi model

### Advanced governance

- **GOV-V2-01**: Organisation-specific viewpoint library persistence pattern (still via model/MCP, not a side DB)
- **GOV-V2-02**: Batch compliance report across entire model (beyond slice snapshots)
- **COH-V2-01**: Fuzzy/semantic duplicate detection beyond deterministic name+type helpers
- **COMP-V2-01**: Live MCP resource refresh of allowlist fixtures as a CI job (still not skill-embedded catalogs)
- **RAT-01+**: OBJ-6 structured rationale depth and natural-language change regeneration

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
| Rework of v1.0–v1.3 shipped cores beyond compliance hooks | Already shipped; integrate only |
| Live Archi E2E as hard gate for v1.4 | Offline fixtures sufficient; live when Bridge up |
| Silent auto-apply of compliance fixes | NG-3; surface decision |
| Full metamodel completeness in fixture | Minimal fixture covering OBJ-5 check dimensions; MCP remains live SoT |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| COMP-03 | Phase 16 | Complete |
| COMP-04 | Phase 16 | Complete |
| COMP-05 | Phase 16 | Complete |
| COMP-06 | Phase 16 | Complete |
| COMP-07 | Phase 16 | Complete |
| COMP-08 | Phase 17 | Complete |
| COMP-09 | Phase 17 | Complete |
| COMP-10 | Phase 17 | Complete |
| COMP-11 | Phase 18 | Pending |
| COMP-12 | Phase 18 | Pending |
| COMP-13 | Phase 18 | Pending |

**Coverage:**

- v1.4 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---
