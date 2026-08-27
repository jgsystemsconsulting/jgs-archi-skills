# jgs-archi-skills

## What This Is

A suite of ZCode skills that turn the existing JGS Archi Bridge MCP into a governed, agent-guided architecture-development capability inside Archi. One user-invoked orchestrator (`archi-orchestrator`) elicits architectural intent and produces a plain-language view plan; orchestrator-dispatched specialists cover the vision responsibility set through MCP without requiring ArchiMate expertise from the user.

## Core Value

A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## Requirements

### Validated

- ✓ Installable skill suite with MCP inventory + structural validator — v1.0
- ✓ Orchestrator intent elicitation and plain-language view plan with confirmation gate — v1.0
- ✓ Viewpoint trace contracts and specialist dispatch set (12 specialists) — v1.0
- ✓ Inspect-before-create and compliance checklist path — v1.0
- ✓ Rationale schema, completion summary pattern, evidence layout — v1.0
- ✓ Viewpoint selection matrix helper (axes/keys only, NG-4) — v1.1
- ✓ Full archi-viewpoint-select Trace Table + org-specific path — v1.1
- ✓ Orchestrator Step 2b viewpoint grounding before confirmation — v1.1
- ✓ Offline viewpoint-selection evidence fixture — v1.1

### Active

- [ ] Live Archi MCP E2E evidence for orchestrator + viewpoint-select (when Bridge available)
- [ ] Full specialist modelling bodies beyond contract stubs (non-viewpoint specialists)
- [ ] One live evidence scenario per specialist

### Out of Scope

- Modify jgs-archi-mcp / JGS Archi Bridge plugin — skills consume tools and resources only (NG-1)
- New diagramming or rendering engine — Archi is the only canvas (NG-2)
- Fully autonomous architect — user governs scope, interpretation, and decisions (NG-3)
- Duplicate ArchiMate language reference material inside skills — MCP resources are SoT (NG-4)
- Support for EA tools other than Archi (NG-5)
- Database or durable skill-side persistence — skills are stateless; model holds content
- Persisted organisation-specific viewpoint library as a side store (GOV-V2-01 stays future)

## Context

- v1.0 shipped 2026-08-28: foundations, orchestrator, specialist contracts, compliance helpers, rationale/evidence conventions.
- v1.1 shipped 2026-08-28 (SEED-002 / OBJ-2): matrix + trace schema helpers, full viewpoint-select, orchestrator wiring, offline evidence.
- Runtime dependency: JGS Archi Bridge MCP at default `http://127.0.0.1:18090/mcp`.
- Delivery: skills under `skills/`, install via `python install.py` to `~/.zcode/skills/`.
- Python 3.10+ stdlib-only helpers include viewpoint_selection_matrix and viewpoint_trace_schema.
- Archives: `.planning/milestones/v1.0-*`, `v1.1-*`.

## Constraints

- **Tech stack**: ZCode skills + Python 3.10+ standard library only — no third-party Python deps
- **Interface**: Call existing Archi Bridge MCP only; never copy ArchiMate reference content into skills
- **Canvas**: Archi only; no alternate renderers or EA tools
- **Governance**: User remains in the loop for scope and architectural decisions
- **Persistence**: No database; model documentation fields via MCP hold rationale and content
- **Repo role**: Skills, helpers, tests, and `docs/evidence/` only

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| YOLO + coarse + parallel + adaptive | Ralph non-interactive bootstrap | ✓ Good |
| Skill name archi-orchestrator | Clear user entrypoint | ✓ Good |
| Specialists orchestrator-dispatched only | SPEC-02 / governance | ✓ Good |
| Offline inventory allowlist | CI without live Archi | ✓ Good |
| Specialist stubs in v1.0 | Unblock suite structure; depth later | ✓ Good — revisit per seed |
| Live MCP E2E deferred | Archi availability | ⚠️ Revisit when Bridge up |
| v1.1 deepens OBJ-2 only | SEED-002; leave other specialist bodies to later seeds | ✓ Good |
| Matrix holds selection axes + fixture keys, not metamodel tables | NG-4; MCP recipes remain SoT | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-08-28 after v1.1 milestone*
