# Create path (coherence + compliance)

Binding for specialists that mutate the Archi model via MCP.

## Inspect before create (SPEC-03, SPEC-04)

1. Call `search-elements` / `get-or-create-element` before `create-element`
2. Reuse existing concept IDs across views
3. Keep naming consistent for the same real-world concept

## Compliance (COMP-01, COMP-02)

1. Confirm types against MCP resources (`archimate://reference/archimate-layers`, `archimate://reference/archimate-relationships`)
2. On violation: explain and propose a compliant alternative; never silent-apply illegal edges
3. Optional offline gate: `python helpers/compliance_checklist.py report.json`

## Common tools

`search-elements`, `get-or-create-element`, `create-element`, `create-relationship`, `add-to-view`, `get-view-contents`
