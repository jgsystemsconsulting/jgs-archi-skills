---
name: archi-documentation
description: "Documentation/rationale specialist; orchestrator-dispatched."
---

# archi-documentation

Contract stub for suite completeness (SPEC-01). Full modelling depth may expand later.


## Rules
- Orchestrator-dispatched only (SPEC-02).
- Inventory MCP tools only; read archimate://recipes/index before non-trivial views.
- Inspect before create: search-elements / get-or-create-element (SPEC-03).
- On compliance failure explain + propose alternative (COMP-02). See docs/CREATE_PATH.md.
- No plugin modification; no ArchiMate table dumps.


## Rationale (RATE-01)
Validate with: python helpers/rationale_schema.py path/to/rationale.md
Record into model docs fields post-confirm via MCP.

## NL changes (RATE-02)
Regenerate views without destroying shared elements; reuse IDs.

## Completion summary (RATE-03)
End with views touched, decisions, open questions, confirmation status.
