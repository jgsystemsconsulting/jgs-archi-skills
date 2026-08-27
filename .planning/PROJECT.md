# jgs-archi-skills

## What This Is

A suite of ZCode skills that turn the existing JGS Archi Bridge MCP into a governed, agent-guided architecture-development capability inside Archi. One user-invoked orchestrator (`archi-orchestrator`) elicits architectural intent and produces a plain-language view plan; orchestrator-dispatched specialists cover the vision responsibility set through MCP without requiring ArchiMate expertise from the user.

## Core Value

A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## Current Milestone: v1.1 Viewpoint selection grounding

**Goal:** Deliver OBJ-2 in depth: viewpoint choices are framework-grounded (stakeholder, concern, purpose, abstraction), validated offline, and wired through orchestrator dispatch, beyond the v1.0 contract stub.

**Target features:**
- Deterministic viewpoint selection matrix helper (stdlib) that scores/maps intent axes to candidate standard viewpoints without copying ArchiMate reference tables
- Full `archi-viewpoint-select` skill body producing a schema-valid Viewpoint Trace Table, with organisation-specific proposals when no standard fit
- Orchestrator dispatch + consumption of viewpoint traces into the View Plan
- Offline fixtures and tests proving VIEW-depth requirements without live Archi

**SEED:** SEED-002 (VISION OBJ-2)

## Requirements

### Validated

- ✓ Installable skill suite with MCP inventory + structural validator — v1.0
- ✓ Orchestrator intent elicitation and plain-language view plan with confirmation gate — v1.0
- ✓ Viewpoint trace contracts and specialist dispatch set (12 specialists) — v1.0
- ✓ Inspect-before-create and compliance checklist path — v1.0
- ✓ Rationale schema, completion summary pattern, evidence layout — v1.0

### Active

- [ ] Viewpoint selection matrix helper (deterministic, stdlib, no metamodel copy)
- [ ] Full archi-viewpoint-select skill body with schema-valid trace table
- [ ] Organisation-specific viewpoint proposal path with compliance constraints
- [ ] Orchestrator wires viewpoint-select and embeds traces in the View Plan
- [ ] Offline fixture evidence for viewpoint selection (no live Archi required)
- [ ] Live Archi MCP E2E evidence for orchestrator (when Bridge available) — deferred if offline-only
- [ ] Full specialist modelling bodies beyond contract stubs (other specialists) — later seeds
- [ ] One live evidence scenario per specialist — later seeds

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
- v1.1 (SEED-002 / OBJ-2): deepen viewpoint selection from contract stub to working matrix + skill + orchestrator integration + offline evidence.
- Runtime dependency: JGS Archi Bridge MCP at default `http://127.0.0.1:18090/mcp`.
- Delivery: skills under `skills/`, install via `python install.py` to `~/.zcode/skills/`.
- Python 3.10+ stdlib-only helpers: validate_skill_mcp_refs, view_plan_schema, specialist_manifest, compliance_checklist, rationale_schema; v1.1 adds viewpoint selection matrix + trace schema.
- Archive: `.planning/milestones/v1.0-*`.

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
| v1.1 deepens OBJ-2 only | SEED-002; leave other specialist bodies to later seeds | Active |
| Matrix holds selection axes + fixture keys, not metamodel tables | NG-4; MCP recipes remain SoT | Active |

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
*Last updated: 2026-08-28 after starting v1.1 milestone*
