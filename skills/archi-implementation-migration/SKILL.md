---
name: archi-implementation-migration
description: "Implementation and migration specialist; orchestrator-dispatched modelling via Archi MCP after View Plan confirmation."
---

# archi-implementation-migration

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Model the **implementation** concern set: Work packages, deliverables, plateaus, gaps, and migration roadmaps from baseline to target.

Create or reuse elements, relationships, and views through the JGS Archi Bridge MCP after the user approves the View Plan (SPEC-D layer body / OBJ-3).

## Hard rules

1. **Mutations only after View Plan confirmation** (SPEC-D-15 / NG-3). If confirmation is missing, stop with hand-back; no mutating tools.
2. **Orchestrator-dispatched only** (SPEC-02 / SPEC-D-13).
3. **Follow `docs/CREATE_PATH.md`** end to end (inspect-before-create, compliance explain-and-propose, inventory tools only).
4. **No ArchiMate metamodel table dumps** (NG-4 / SPEC-D-14). Read MCP resources; do not paste catalogs into the skill or chat.
5. **Consume-only** toward jgs-archi-mcp (NG-1). Default endpoint: see `docs/MCP.md`.

## Inputs

From the orchestrator hand-off:

| Field | Required | Notes |
|-------|----------|-------|
| Confirmation status | yes | Must be `approved` |
| Intent summary | yes | Problem, stakeholders, concerns, scope |
| Target viewpoints | yes | Names + abstraction from Trace Table / View Plan |
| Layer scope | yes | This specialist owns **implementation** (and explicit adjacencies only when hand-off says so) |
| Existing model hints | optional | Known element names/IDs to reuse |
| Constraints | optional | Naming, folders, exclusions |

## MCP resources (read before non-trivial views)

When Bridge is connected, read as needed:

- `archimate://recipes/index`
- `archimate://recipes/roadmap-migration`
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

1. Restate layer scope and target viewpoints (Implementation and migration / roadmap views).
2. Read recipe/index resources for patterns (no table dumps).
3. Search existing model for concepts named in the intent and hand-off.

### Step 2 — Element set

For each concept in scope:

1. `search-elements` (and `get-or-create-element` when appropriate).
2. Reuse IDs when the same real-world concept already exists.
3. Create only when missing; keep names consistent across views.
4. Prefer types appropriate to the **implementation** layer per MCP reference resources.

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
3. Optional: draft a compliance checklist JSON for `python helpers/compliance_checklist.py` when findings exist.

### Step 6 — Hand-back

Return the CREATE_PATH payload: status, views touched, elements/relationships created or reused, compliance notes, open questions, confirmation assumption.

## Output template

```markdown
## Specialist Result: archi-implementation-migration

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

### Next specialist hint
- …
```

## Return to orchestrator

1. Specialist Result markdown
2. IDs needed by downstream specialists (traceability, layout, documentation)
3. Explicit statement that work stayed inside confirmed scope
