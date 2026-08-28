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
- `coherence-reuse-offline/` — v1.3 OBJ-4 multi-view reuse + naming fixtures
- `compliance-validation-offline/` — v1.4 OBJ-5 compliance_validate pass/fail slices + freeze
- `rationale-nl-change-offline/` — v1.5 OBJ-6 rationale depth + NL-change impact + completion-summary fixtures
