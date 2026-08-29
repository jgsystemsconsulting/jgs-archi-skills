<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Evidence: viewpoint-selection-offline

**Milestone:** v1.1 / SEED-002 / OBJ-2
**Mode:** Offline fixture (no live Archi Bridge required)

## Artifacts

| File | Role |
|------|------|
| intent-axes.json | Structured intent axes |
| matrix-output.json | `viewpoint_selection_matrix.py` ranked output |
| trace-table.md | Schema-valid Viewpoint Trace Table |
| view-plan.md | View Plan with Proposed Viewpoints aligned to trace |

## Reproduce

```bash
python helpers/viewpoint_selection_matrix.py docs/evidence/viewpoint-selection-offline/intent-axes.json --top 6
python helpers/viewpoint_trace_schema.py docs/evidence/viewpoint-selection-offline/trace-table.md
python helpers/view_plan_schema.py docs/evidence/viewpoint-selection-offline/view-plan.md
python -m pytest tests/ -q
```
