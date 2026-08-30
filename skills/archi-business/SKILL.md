---
name: archi-business
description: "Business layer specialist; orchestrator-dispatched modelling via Archi MCP after View Plan confirmation."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# archi-business

## When to use

Orchestrator-dispatched after View Plan confirmation when the run needs business-layer modelling.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Model the **business** concern set: Business actors, roles, processes, services, objects, and events that realize capabilities.

Create or reuse elements, relationships, and views through the JGS Archi Bridge MCP after the user approves the View Plan (SPEC-D layer body / OBJ-3).

## Hard rules

1. **Mutations only after View Plan confirmation** (SPEC-D-15 / NG-3). If confirmation is missing, stop with hand-back; no mutating tools.
2. **Orchestrator-dispatched only** (SPEC-02 / SPEC-D-13).
3. **Follow `docs/CREATE_PATH.md`** end to end (inspect-before-create, OBJ-4 coherence/reuse registry, OBJ-5 compliance explain-and-propose via compliance_validate when useful, inventory tools only).
4. **No ArchiMate metamodel table dumps** (NG-4 / SPEC-D-14). Read MCP resources; do not paste catalogs into the skill or chat.
5. **Consume-only** toward jgs-archi-mcp (NG-1). Default endpoint: see `docs/MCP.md`.

## Inputs

From the orchestrator hand-off:

| Field | Required | Notes |
|-------|----------|-------|
| Confirmation status | yes | Must be `approved` |
| Intent summary | yes | Problem, stakeholders, concerns, scope |
| Target viewpoints | yes | Names + abstraction from Trace Table / View Plan |
| Layer scope | yes | This specialist owns **business** (and explicit adjacencies only when hand-off says so) |
| Existing model hints | optional | Known element names/IDs to reuse |
| reuse_registry | optional | Run-scoped concept_key → element_id from orchestrator |
| naming_policy | optional | Default title-collapse-v1 |
| Constraints | optional | Naming, folders, exclusions |

## MCP resources (read before non-trivial views)

When Bridge is connected, read as needed:

- `archimate://recipes/index`
- `archimate://recipes/behaviour-process-flow`
- `archimate://reference/archimate-view-patterns`
- `archimate://reference/archimate-layers`
- `archimate://reference/archimate-relationships`

Offline: state what you would read and continue with plain-language types consistent with inventory policy.

## MCP tools (inventory only)

Typical sequence (names must exist in `docs/mcp/archi-bridge-inventory.json`):

1. Discover: `search-elements`, `get-element`, `get-views`, `get-view-contents`, `find-concept-usage`, `get-relationships`
2. Reuse/create elements: `get-or-create-element`, `create-element`, `update-element`
3. Structure: `create-relationship`, `create-view`, `add-to-view`, `update-view`
4. Optional batch: `begin-batch` / `end-batch` / `bulk-mutate` when many safe creates are confirmed

Never invent tool names.

## Procedure

### Step 0 — Gate

If confirmation status is not approved: return status `blocked` and stop.

### Step 1 — Orient

1. Restate layer scope and target viewpoints (Business process / business cooperation views).
2. Read recipe/index resources for patterns (no table dumps).
3. Search existing model for concepts named in the intent and hand-off.

### Step 2 — Element set

For each concept in scope:

1. `search-elements` (and `get-or-create-element` when appropriate).
2. Reuse IDs when the same real-world concept already exists.
3. Create only when missing; keep names consistent across views.
4. Prefer types appropriate to the **business** layer per MCP reference resources.
5. Set the first documentation line to `Evidence: stated | inferred | existing - <source>` (CP-G4). Do not write a bare Rationale for an inferred why.

### Step 3 — Relationships

1. Connect elements with inventory-legal relationship tools.
2. Before each edge, confirm source/target types against MCP relationship reference when unsure.
3. On illegal combination: explain, propose compliant alternative, do **not** silent-apply.

### Step 4 — Views

1. `create-view` or update an existing confirmed view.
2. `add-to-view` for elements/relationships needed for the viewpoint purpose.
3. Do not clear unrelated user content unless the hand-off explicitly requests a rebuild of that view.

### Step 5 — Self-check

1. Every created element appears in at least one intended view (or is justified as shared structure).
2. Naming consistent; duplicates minimised.
3. Optional compliance: build a small model-slice JSON and run `python helpers/compliance_validate.py slice.json` (or thin `compliance_checklist.py`); hand back findings with problem + proposed alternative — never silent-apply.

### Step 6 — Hand-back

Return the CREATE_PATH payload: status, views touched, elements/relationships created or reused, compliance notes, open questions, confirmation assumption.

## Output template

```markdown
## Specialist Result: archi-business

**Status:** completed | blocked | needs-user
**Confirmation:** approved (assumed from hand-off)

### Views touched
- …

### Elements and relationships
| Action | Name | Type/kind | ID (if known) |
|--------|------|-----------|---------------|
| reused/created | … | … | … |

### Compliance notes
- none | …

### Open questions
- …

### Candidate disposition
| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| … | captured \| folded \| needs-user \| out-of-scope | element @ view, or parent | one line |

### Next specialist hint
- …
```

## Return to orchestrator

1. Specialist Result markdown
2. IDs needed by downstream specialists (traceability, layout, documentation)
3. Explicit statement that work stayed inside confirmed scope
4. Candidate disposition table (every hand-off candidate; validate with `python helpers/disposition.py` when a file artifact exists)
