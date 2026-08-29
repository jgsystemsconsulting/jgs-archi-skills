<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Live Archi smoke evidence

Recorded 2026-08-28 against a live Archi 5.x instance running the JGS Archi
Bridge plugin (`net.vheerden.archi.mcp` 1.8.0, dropins install) at
`http://127.0.0.1:18090/mcp`.

## What ran

`python tests/live_mcp_smoke.py` drives the full orchestrator-style flow
against a dedicated scratch model (`JGS-Skills-Live-Smoke.archimate`, included
here). It exercises: MCP initialize, tools/list, get-model-info guard,
resources/list + resources/read (`archimate://reference/archimate-layers`),
search-elements, get-or-create-element (twice, proving live reuse:
`found_existing` with the same id), update-element documentation, three
create-relationship calls (Assignment, Serving, Realization), create-view,
four add-to-view calls with positions and autoConnect, assess-layout,
auto-layout-and-route, get-view-contents (4 objects, 3 connections asserted),
export-view PNG, then offline helpers `compliance_validate` and
`rationale_schema` over the captured slice.

## Verdict

PASS. Live `tools/list` matched the offline inventory exactly (69 tools, 14
resources, zero diff in either direction). All mutations applied to the
scratch model only; the model guard in the script refuses to run when the
active model is anything else. Final state: 4 elements, 3 relationships,
4 views, approval mode restored to ON after the run.

## Findings surfaced by going live

1. The server binds to the model that fired `MODEL_OPENED` last (or
   `models.get(0)` at start). A model created in-session via Ctrl+N never
   fires that event, so the server kept targeting a different open model
   until the scratch model was saved, closed, and reopened. Skills must not
   assume "new model in this session is the model the server sees"; the
   get-model-info guard in the smoke script encodes this.
2. Relationship `type` values use full names (`AssignmentRelationship`), not
   bare names (`Assignment`); bare names fail with
   `INVALID_RELATIONSHIP_TYPE`.
3. The offline compliance fixture lacked the `BusinessActor -Assignment->
   BusinessProcess` pattern. The live MCP reference
   (`archimate://reference/archimate-relationships`) permits it ("active
   structure elements to behaviour elements") and live create-relationship
   accepted it, so the fixture was a false positive; it was widened with
   that pattern and a note citing this evidence.

## Files

- `JGS-Skills-Live-Smoke.archimate` - the scratch model after the run
- `id-baa8acc69f2c440694c26b786edc8ff0_*.png` - exported view image
- `live-slice.json`, `inventory.json` - captured model slices for offline helpers
- `rationale.md` - structured rationale validated by `helpers/rationale_schema.py`
- `transcript.json` - step-by-step run transcript

## Reproducing

Start Archi, open a scratch model, start the MCP server (MCP Server > Start
MCP Server), make sure that model is the bound one (get-model-info), then:

```bash
python tests/live_mcp_smoke.py
```

Approval Mode can stay ON; mutations will queue in the Pending Approvals
dock and the script fails on the model-name guard rather than writing to a
foreign model. This run disabled Approval Mode temporarily for the scratch
test and restored it afterwards.
