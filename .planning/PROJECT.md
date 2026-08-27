# jgs-archi-skills

## What This Is

A suite of ZCode skills that turn the existing JGS Archi Bridge MCP into a governed, agent-guided architecture-development capability inside Archi. One user-invoked orchestrator elicits architectural intent and produces a plain-language view plan; orchestrator-dispatched specialists create ArchiMate elements, relationships, and views through the MCP without requiring ArchiMate expertise from the user.

## Core Value

A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Orchestrator elicits architectural intent (problem, stakeholders, concerns, scope, current/target state, expected outcome) and produces a plain-language view plan (viewpoints, layers, modelling sequence, dependencies, validation points).
- [ ] Viewpoint selection is grounded in the ArchiMate viewpoint framework (stakeholder, concern, purpose, abstraction level), with justified organisation-specific viewpoints only when no standard fit exists.
- [ ] Specialist skill set covers elicitation, viewpoint selection, motivation, capability/strategy, business, application, technology/physical, implementation/migration, cross-layer traceability, model QA, layout/presentation, and documentation/rationale.
- [ ] Model coherence and reuse: inspect existing model content before create; reuse shared concepts; consistent naming; minimise duplicates.
- [ ] Compliance validation for element types, relationship combinations, permitted types, abstraction levels, cross-view consistency, and naming, with explained alternatives instead of silent fixes.
- [ ] Structured rationale on significant views, natural-language change requests that regenerate views without damaging the shared model, and completion summaries.
- [ ] Structural validation helper proves skills reference only real MCP tools/resources; one documented live end-to-end scenario per specialist with evidence under `docs/evidence/`.
- [ ] Install path: skills live in-repo and install to `~/.zcode/skills/` via an install script.

### Out of Scope

- Modify jgs-archi-mcp / JGS Archi Bridge plugin — skills consume tools and resources only (NG-1)
- New diagramming or rendering engine — Archi is the only canvas (NG-2)
- Fully autonomous architect — user governs scope, interpretation, and decisions (NG-3)
- Duplicate ArchiMate language reference material inside skills — MCP resources are SoT (NG-4)
- Support for EA tools other than Archi (NG-5)
- Database or durable skill-side persistence — skills are stateless; model holds content

## Context

- Greenfield skills repo. No application source yet. Owner-authored VISION.md is the product brief.
- Runtime dependency: JGS Archi Bridge MCP at default `http://127.0.0.1:18090/mcp` (69 tools, 14 resources including archimate-layers, archimate-relationships, archimate-specializations, archimate-view-patterns, viewpoint recipes).
- Delivery form: one SKILL.md per skill; Python 3.10+ stdlib-only helpers for viewpoint matrix, compliance asserts, and suite structural validation.
- First milestone seed SEED-001 targets OBJ-1 (orchestrator intent elicitation and view plan). Later seeds cover OBJ-2..OBJ-6.
- Quality bar is dual: structural checks plus live MCP evidence captures.

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
| YOLO + coarse granularity + parallel plans | Ralph non-interactive bootstrap; recommended auto-mode defaults | — Pending |
| Adaptive model profile | Role-based cost/quality balance across GSD agents | — Pending |
| Research on for project init | Domain (ArchiMate skill orchestration) benefits from explicit stack/features/architecture/pitfalls | — Pending |
| MVP phase mode | Vertical slices that leave runnable skill/capability increments | — Pending |
| Skill naming deferred to planner | VISION leaves naming open | — Pending |
| First milestone focuses OBJ-1 orchestrator | SEED-001 / BACKLOG priority; remaining OBJs later seeds | — Pending |

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
*Last updated: 2026-08-27 after initialization*
