# Evidence layout

Convention for live specialist scenarios (EVID-02):

```text
docs/evidence/<skill-or-scenario-id>/
  README.md
  transcript.md
  view-plan.md
  rationale.md
  completion-summary.md
```

Offline smoke: `orchestrator-smoke/` (not a live MCP run).

EVID-01 (orchestrator live E2E): add `docs/evidence/orchestrator-live/` when Archi + Bridge are available.

## Fixtures

- `orchestrator-smoke/` — v1.0 offline view-plan smoke
- `viewpoint-selection-offline/` — v1.1 OBJ-2 offline matrix → trace → view-plan fixture
- `specialist-suite-offline/` — v1.2 OBJ-3 specialist dispatch + tool-sequence fixtures
