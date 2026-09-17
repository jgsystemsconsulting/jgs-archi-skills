<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Live MCP smoke runbook

## What this is

A live end-to-end smoke of the skill-suite contract against a running JGS
Archi Bridge. It mirrors the orchestrator flow: inspect model, reuse gate,
create, relate, view, rationale, layout, validate, export. The smoke is
opt-in and manual; `python -m unittest discover` never runs it. Exit 0 means
every step passed. This runbook is the only public artifact of a run.

## Prerequisites

- Archi 5.7+ with the JGS Archi Bridge plugin installed.
- MCP server started inside Archi: MCP Server > Start MCP Server, endpoint
  `http://127.0.0.1:18090/mcp`.
- Python 3.10+ (standard library only).

## Scratch model

Create a model named exactly `JGS Skills Live Smoke` and save it to disk.
The script guards on this name (`EXPECTED_MODEL`) and refuses to run against
any other active model, so a wrong name or the wrong active window fails fast
instead of writing into a foreign model.

## The Ctrl+N footgun (MODEL_OPENED)

The bridge binds to the model that fired `MODEL_OPENED` last, or to the first
open model at server start. A model created in-session with Ctrl+N never
fires that event. Symptom: the smoke exits non-zero on the model-name guard
even though the scratch model looks active, because the bridge is still
targeting a different open model.

Fix: save the scratch model, close it, and reopen it so `MODEL_OPENED`
fires. Then confirm the binding before running.

## Approval Mode

Two supported paths:

1. Leave Approval Mode on and grant each mutation from the Pending Approvals
   dock as the run proceeds.
2. Turn Approval Mode off for the scratch run, then turn it back on
   afterwards.

Either way, finish the run with Approval Mode restored.

## Run

```bash
python tests/live_mcp_smoke.py
```

Optional: `--evidence-dir DIR` overrides the default evidence directory
`live-smoke-out/`. Outputs are `transcript.json` and a view PNG in the
evidence directory. The default directory is gitignored.

## If it fails

| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection refused | MCP server not started | In Archi: MCP Server > Start MCP Server, then run again |
| Non-zero exit on the model-name guard | Wrong active model, or an unbound Ctrl+N model | Reopen the saved scratch model (see the footgun above); the guard message names the model it found |
| Steps stall or fail on timeout | Mutation approvals never granted | Grant from the Pending Approvals dock, or toggle Approval Mode off for the run |

The model-name guard is the intended fast failure. When in doubt, read its
message first.

## Evidence policy

Recorded runs and captured slices stay local. The default paths
(`live-smoke-out/`, `docs/evidence/`) are gitignored and must stay that way.
A custom `--evidence-dir` is not covered by .gitignore; do not commit it.
This runbook is the only public artifact of a smoke run.
