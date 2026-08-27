# Features Research

**Domain:** Agent-guided ArchiMate viewpoint creation
**Researched:** 2026-08-27
**Confidence:** HIGH

## Table stakes (v1 expected)

| Feature | Complexity | Notes |
|---------|------------|-------|
| Intent elicitation (problem, stakeholders, concerns, scope, as-is/to-be, outcome) | M | OBJ-1 core |
| Plain-language view plan (viewpoints, layers, sequence, dependencies, validation points) | M | OBJ-1 output; no ArchiMate expertise required of user |
| Viewpoint selection grounded in ArchiMate framework | M | OBJ-2; stakeholder/concern/purpose/abstraction |
| Organisation-specific viewpoint proposal when no standard fit | S | Must stay ArchiMate-compliant and justified |
| Specialist coverage for listed responsibilities | L | OBJ-3 full set; phased delivery OK |
| MCP-mediated create of elements, relationships, views | M | All specialists |
| Pre-create model inspection and concept reuse | M | OBJ-4 |
| Compliance checks with explained alternatives | M | OBJ-5 |
| Structured view rationale recorded via MCP | M | OBJ-6 |
| NL change request → regenerate views without breaking shared model | L | OBJ-6 |
| Completion summary after modelling run | S | OBJ-6 |
| Structural suite validator (skills ↔ real MCP tools/resources) | M | Quality bar |
| Live E2E evidence capture per specialist | M | Quality bar; `docs/evidence/` |
| Install script to `~/.zcode/skills/` | S | Delivery form |

## Differentiators (vision-driven)

| Feature | Complexity | Notes |
|---------|------------|-------|
| Orchestrator dispatches specialists (not user-invoked) | M | Governance and sequencing |
| Cross-layer traceability specialist | M | OBJ-3 |
| Layout/presentation specialist | M | OBJ-3; Archi canvas only |
| Model QA specialist as first-class skill | M | Separates creation from critique |

## Anti-features (do not build)

| Anti-feature | Reason |
|--------------|--------|
| Patch/extend jgs-archi-mcp | NG-1 |
| Alternate renderer or non-Archi EA tool | NG-2, NG-5 |
| Silent auto-fix of invalid relations | OBJ-5 requires explanation + alternative |
| Fully autonomous architecture decisions | NG-3 |
| In-skill ArchiMate reference dump | NG-4 |
| Skill-side database | Stateless policy |

## Dependencies

- Elicitation + view plan → viewpoint selection → layer specialists
- Coherence/reuse and compliance gate every create path
- Rationale and completion summary wrap significant views
- Structural validator can precede live MCP evidence
- Install script after skill tree exists
