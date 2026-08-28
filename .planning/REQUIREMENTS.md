# Requirements: jgs-archi-skills

**Defined:** 2026-08-28
**Milestone:** v1.5 Structured rationale depth (SEED-006 / OBJ-6)
**Core Value:** A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## v1.5 Requirements

Requirements for this milestone only. Prior REQUIREMENTS remain under `.planning/milestones/v1.0-REQUIREMENTS.md` through `v1.4-REQUIREMENTS.md`.

### Rationale and summary helpers

- [x] **RAT-01**: Stdlib helper deepens offline rationale validation beyond bare H2 presence: required OBJ-6 sections present, non-empty body per section (after strip), stable section order optional warning; no MCP calls; no third-party deps
- [x] **RAT-02**: Helper accepts single-view rationale markdown and multi-view bundles (index + per-view files or concatenated docs) and reports per-view findings
- [x] **RAT-03**: Stdlib helper validates completion-summary structure (views touched, decisions, open questions, confirmation status, specialists run at minimum); exit non-zero on missing required blocks
- [x] **RAT-04**: Stdlib NL-change impact helper accepts a natural-language change note plus a view inventory snapshot and returns: affected view ids/names, proposed regenerate scope, shared-element IDs that must be reused (never recreated), and explicit exclusions; never mutates a model

### Contract and skill binding

- [x] **RAT-05**: `docs/CREATE_PATH.md` gains an OBJ-6 rationale / NL-change / completion-summary section: when to draft and validate rationale, how to write documentation fields via MCP after confirmation, NL-change reuse-ID rules, completion summary required fields
- [x] **RAT-06**: `archi-documentation` procedure binds deepened helpers (rationale, completion summary, NL-change impact); Step 4 NL path requires impact plan before regenerate; hand-back includes schema validation status
- [x] **RAT-07**: `archi-orchestrator` end-of-run path documents consuming documentation specialist completion summary and optional NL-change loop (no new mutating tools; user-governed)

### Evidence and freeze

- [x] **RAT-08**: Offline evidence under `docs/evidence/rationale-nl-change-offline/` shows: valid multi-view rationale pack, invalid rationale (missing/empty section), NL-change impact plan that preserves shared IDs, completion summary pass/fail samples
- [x] **RAT-09**: Full unit/structural suite green; `archi-viewpoint-select` remains frozen at the v1.1 digest; thin v1.0 `rationale_schema` heading check remains usable or is cleanly extended without breaking callers
- [x] **RAT-10**: No rework of v1.0–v1.4 shipped cores beyond rationale/documentation hooks; NG-1..5 respected

## Future Requirements (not this milestone)

### Live evidence hard gate

- **EVID-LIVE-01**: Live Archi MCP end-to-end transcript for orchestrator + multi-specialist modelling when Bridge is available
- **EVID-LIVE-02**: One live evidence scenario per specialist against a real Archi model
- **EVID-LIVE-03**: Live MCP write of rationale into view documentation fields with before/after transcript

### Advanced governance

- **GOV-V2-01**: Organisation-specific viewpoint library persistence pattern (still via model/MCP, not a side DB)
- **GOV-V2-02**: Batch compliance report across entire model (beyond slice snapshots)
- **COH-V2-01**: Fuzzy/semantic duplicate detection beyond deterministic name+type helpers
- **COMP-V2-01**: Live MCP resource refresh of allowlist fixtures as a CI job (still not skill-embedded catalogs)

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
| Rework of v1.0–v1.4 shipped cores beyond rationale hooks | Already shipped; integrate only |
| Live Archi E2E as hard gate for v1.5 | Offline fixtures sufficient; live when Bridge up |
| Silent auto-apply of NL-change or compliance fixes | NG-3; surface decision |
| LLM-based semantic NL parsing inside helpers | Helpers stay deterministic; skill interprets free text into structured impact input |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| RAT-01 | Phase 19 | Complete |
| RAT-02 | Phase 19 | Complete |
| RAT-03 | Phase 19 | Complete |
| RAT-04 | Phase 19 | Complete |
| RAT-05 | Phase 20 | Complete |
| RAT-06 | Phase 20 | Complete |
| RAT-07 | Phase 20 | Complete |
| RAT-08 | Phase 21 | Complete |
| RAT-09 | Phase 21 | Complete |
| RAT-10 | Phase 21 | Complete |

**Coverage:**

- v1.5 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0

---
