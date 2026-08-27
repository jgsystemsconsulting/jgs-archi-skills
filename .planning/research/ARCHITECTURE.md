# Architecture Research

**Domain:** ZCode skill suite over Archi Bridge MCP
**Researched:** 2026-08-27
**Confidence:** HIGH

## Major Components

| Component | Boundary | Talks to |
|-----------|----------|----------|
| Orchestrator skill | User-invoked entry; intent + view plan; dispatches specialists | User, MCP resources (read), specialist skills |
| Specialist skills | One responsibility each; not user-invoked | Orchestrator, MCP tools/resources |
| Helper scripts (Python stdlib) | Offline/deterministic: viewpoint matrix, compliance asserts, suite structural validation | Skill sources, optional MCP manifest snapshot |
| JGS Archi Bridge MCP | External SoT for tools + ArchiMate resources | Archi model |
| Archi model | Persistent elements, views, documentation/rationale fields | MCP only |
| Evidence store (`docs/evidence/`) | Captured live scenario artifacts | Humans / CI review |
| Install script | Publish skills to `~/.zcode/skills/` | Repo tree, user home |

## Data Flow

1. User → Orchestrator: architectural intent in plain language.
2. Orchestrator → MCP resources: layers, relationships, specializations, view patterns, viewpoint recipes (read-only reference).
3. Orchestrator → user: plain-language view plan (viewpoints, layers, sequence, deps, validation points).
4. Orchestrator → specialists: scoped work packages aligned to the plan.
5. Specialist → MCP tools: inspect existing model → create/reuse elements, relationships, views → write rationale fields.
6. Compliance/QA path: validate proposed changes; on violation, explain + propose compliant alternative (no silent apply).
7. Helpers: static validation of skill manifests against known MCP tool/resource names; checklist asserts for compliance rules.
8. Evidence: live runs produce transcripts under `docs/evidence/`.

## Build Order (implications for roadmap)

1. Repo skeleton + install path + MCP contract inventory for structural validator.
2. Orchestrator (OBJ-1): elicitation + view plan — first user-visible value; SEED-001.
3. Viewpoint selection grounding (OBJ-2) as skill or orchestrator submodule.
4. Core layer specialists + create/reuse path (OBJ-3/4) behind MCP.
5. Compliance + model QA (OBJ-5).
6. Rationale, NL regen, completion summary (OBJ-6).
7. Remaining specialists (layout, docs, migration, etc.) and full evidence matrix.

## Suggested Internal Layout (non-binding)

```
skills/<name>/SKILL.md
helpers/*.py
tests/test_*.py
docs/evidence/<scenario>/
```

Exact skill names: planner decides per VISION.

## Integration Constraints

- Skills never vendor ArchiMate tables; always query MCP resources.
- No writes to plugin code.
- Stateless skills: all durable state in Archi model via MCP.
