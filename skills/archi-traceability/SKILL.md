---
name: archi-traceability
description: "Cross-layer traceability specialist; orchestrator-dispatched. Creates explicit traces and reports gaps after View Plan confirmation."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# archi-traceability

## When to use

Orchestrator-dispatched after View Plan confirmation when cross-layer traces must be created or gaps reported.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Establish explicit cross-layer traces (motivation to business to application to technology, plus strategy/implementation when in scope) via MCP relationships, and report missing links as gaps (SPEC-D-08 / OBJ-3).

## Hard rules

1. **Mutations only after View Plan confirmation** (SPEC-D-15 / NG-3).
2. **Orchestrator-dispatched only** (SPEC-02 / SPEC-D-13).
3. **Follow `docs/CREATE_PATH.md`** (OBJ-4 coherence + OBJ-5 compliance explain-and-propose).
4. **No ArchiMate metamodel table dumps** (NG-4).
5. Prefer relating existing elements; create relationship-only structure unless hand-off authorizes new bridging elements.
6. Optional offline: `python helpers/compliance_validate.py slice.json` on proposed/created edges; never silent-apply illegal combos.

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Confirmation status | yes | approved |
| Intent summary | yes | |
| Layer element IDs/names | yes | From prior specialists or model search |
| Trace policy | optional | Required chain hops; critical paths |

## MCP resources

- `archimate://recipes/index`
- `archimate://reference/archimate-relationships`
- `archimate://reference/archimate-layers`
- `archimate://reference/archimate-view-patterns`

## MCP tools

Discover: `search-elements`, `get-element`, `get-relationships`, `find-concept-usage`, `get-views`, `get-view-contents`  
Relate: `create-relationship`, `get-or-create-element` (only if hand-off allows bridge elements)  
Views: `create-view`, `add-to-view` for a traceability/overview view when requested

## Procedure

OBJ-4 coherence: before each create, search existing elements; run `helpers/reuse_inspect.py` on the snapshot when useful; apply `helpers/naming_convention.py` normalize; update run-scoped `reuse_registry`; never auto-merge `ambiguous`. Hand-back must list **reused** vs **created** IDs.


### Step 0 — Gate
Stop if confirmation is not approved.

### Step 1 — Inventory endpoints
Search model for motivation, business, application, technology (and strategy/implementation) concepts named in the hand-off. Record IDs.

### Step 2 — Expected traces
Build the expected chain from the View Plan modelling sequence.

### Step 3 — Existing edges
Use `get-relationships` / `find-concept-usage` to list current links between endpoints.

### Step 4 — Fill gaps
For each missing hop: propose relationship type from MCP relationship reference; create with `create-relationship` when on the approved path. Illegal combo → explain + alternative (COMP-02 / OBJ-5), never silent-apply. Optional: validate proposed edges via `helpers/compliance_validate.py` on a slice before create.

- Set the first documentation line to `Evidence: stated | inferred | existing - <source>` (CP-G4). Do not write a bare Rationale for an inferred why.

### Step 5 — Gap report
List untraceable endpoints and broken chains without inventing business meaning.

### Step 6 — Optional trace view
If hand-off requests a trace view: create/update view and add traced elements/relationships.

### Step 7 — Hand-back
CREATE_PATH payload plus a Trace Gap Table.

## Output template

```markdown
## Specialist Result: archi-traceability

**Status:** completed | blocked | needs-user

### Traces established
| From | To | Relationship | ID |
|------|----|--------------|----|
| … | … | … | … |

### Trace Gap Table
| Endpoint | Expected hop | Gap reason |
|----------|--------------|------------|
| … | … | … |

### Views touched
- …

### Open questions
- …

### Candidate disposition
| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| … | captured \| folded \| needs-user \| out-of-scope | element @ view, or parent | one line |
```

## Return to orchestrator

1. Specialist Result with Trace Gap Table
2. IDs of new relationships
3. Whether critical paths are complete
4. Candidate disposition table (every hand-off candidate; validate with `python helpers/disposition.py` when a file artifact exists)
