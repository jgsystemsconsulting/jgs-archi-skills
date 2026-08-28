# Tool sequence: compliance validation

## Live (Bridge up)

1. Specialist/model-qa gathers elements via `search-elements` / `get-view-contents` / `get-relationships`
2. Read MCP `archimate://reference/archimate-layers` and `archimate://reference/archimate-relationships`
3. On suspected issue: draft model-slice JSON from gathered IDs
4. Optional offline: `python helpers/compliance_validate.py slice.json --json`
5. Report findings (problem + proposed_alternative); never silent-apply
6. If user authorizes a listed fix set: minimal MCP updates only

## Offline evidence (this pack)

1. Load `pass-slice.json` / `fail-slice.json`
2. `python helpers/compliance_validate.py … --json`
3. Thin gate remains: `python helpers/compliance_checklist.py report.json` when a boolean map exists
4. Coherence helpers still available for duplicates/naming (`reuse_inspect`, `naming_convention`)
