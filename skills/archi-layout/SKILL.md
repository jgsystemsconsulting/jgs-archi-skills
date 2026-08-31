---
name: archi-layout
description: "Layout/presentation specialist; orchestrator-dispatched. Archi-native layout tools only after confirmation."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# archi-layout

## When to use

Orchestrator-dispatched after View Plan confirmation when target views need Archi-native layout and presentation.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Improve readability of target Archi views using inventory layout and presentation tools only (SPEC-D-10). Archi is the only canvas (NG-2).

## Hard rules

1. **Mutations only after View Plan confirmation** (SPEC-D-15).
2. **Orchestrator-dispatched only** (SPEC-02).
3. **Follow `docs/CREATE_PATH.md`**.
4. **No alternate renderer** (NG-2). No non-Archi export as the primary layout path.
5. Inventory layout tool names only.

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Confirmation status | yes | approved |
| Target view IDs/names | yes | |
| Readability goals | optional | fewer crossings, group by layer, spacing |

## MCP resources

- `archimate://recipes/index`
- `archimate://reference/archimate-view-patterns`
- `archimate://prompts/routing-preconditions-checklist`

## MCP tools

Assess: `assess-layout`, `get-view-contents`, `detect-hub-elements`, `export-view`
Layout: `auto-layout-and-route`, `layout-flat-view`, `layout-within-group`, `arrange-groups`, `optimize-group-order`, `apply-positions`
Spacing: `adjust-view-spacing`, `apply-spacing-recommendations`, `apply-element-spacing-recommendations`, `apply-group-spacing-recommendations`, `resize-elements-to-fit`
Connections: `auto-route-connections`, `auto-connect-view`
Notes/groups: `add-group-to-view`, `add-note-to-view`, `update-view-object` when hand-off allows

## Procedure

OBJ-4 coherence: before each create, search existing elements; run `helpers/reuse_inspect.py` on the snapshot when useful; apply `helpers/naming_convention.py` normalize; update run-scoped `reuse_registry`; never auto-merge `ambiguous`. Hand-back must list **reused** vs **created** IDs.


### Step 0 — Gate
Stop without approval.

### Step 1 — Baseline
`get-view-contents` + `assess-layout` on each target view. Record issues (overlaps, hubs, spacing).

### Step 2 — Choose strategy
- Structure views with more than about 10 elements: grouped or nested (`add-group-to-view` / `parentViewObjectId`). Flat needs a recorded reason in the hand-back.
- Flat structural views (small, or justified): `layout-flat-view` or `auto-layout-and-route`
- Grouped layered views: `arrange-groups` / `layout-within-group`
- Connection spaghetti: `auto-route-connections` after positions stable
- Nested hub (six or more connections): resize the hub, then `auto-route-connections`. Re-route alone is inert.
- Junctions: about 14 by 14. Do not pass a layer-folder `folderId` for a Junction.
- Literal `&` in names and labels, never `&amp;`.

### Step 3 — Apply
Run layout tools; avoid `clear-view` unless hand-off explicitly rebuilds the view.

Route after layout: `auto-layout-and-route` alone often leaves diagonal
terminal segments that hold `assess-layout` at `fair`. Escalate in this
order, re-assessing after each step:

1. `auto-route-connections` with `mode=terminals-only` (rectifies terminals,
   keeps routed bodies).
2. If terminal findings persist, full `auto-route-connections` (may add a
   few edge crossings; compare `assess-layout` ratings, not just counts).
3. If a view is still below `good`, one retry of `auto-layout-and-route`
   (with `targetRating`) followed by a full route.

Target `excellent`; accept `good` only with a recorded residual reason
(e.g. structurally inherent crossings). Record every assessment verdict in
the specialist hand-back.

### Step 4 — Re-assess dimensions
`assess-layout` again. Walk `ratingBreakdown`. Dispose every non-pass dimension (fix or record why accepted). Treat partial and not-checked as unverified, not passed. Do not sign off on overallRating alone.

### Step 5 — Annotate last (CP-G5)
Only after layout and routing are finished, add notes or legends with `add-note-to-view`. Omit `height` so the server auto-fits. Place with `position: below-content`, never above-content. Do not run layout, route, or resize after notes. If geometry must change, re-place the note after it.

### Step 6 — Render close-out (CP-G6)
After any add, move, resize, or style, including notes: `assess-layout` then `export-view`. Inspect the PNG. The render wins if the metric under-counts.

### Step 7 — Hand-back

## Output template

```markdown
## Specialist Result: archi-layout

**Status:** completed | blocked | needs-user

### Views laid out
| View | Tools used | Residual issues |
|------|------------|-----------------|
| … | … | ratingBreakdown leftovers or none |

### Open questions
- …
```

## Return to orchestrator

1. Specialist Result
2. Views ready for documentation/export
