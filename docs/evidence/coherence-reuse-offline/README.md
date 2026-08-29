<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Coherence reuse offline evidence (v1.3 / OBJ-4)

Offline pack proving multi-view reuse of one element ID, duplicate minimisation,
and naming consistency without live Archi MCP.

## Scenario

Intent: model Customer Portal once; show it on Application Structure and Application Usage views.

## Artifacts

- `inventory.json`: model element snapshot
- `reuse-decisions.json`: reuse_inspect outputs for candidates
- `usages.json`: per-view element name usages
- `naming-conflicts.json`: naming_convention conflicts report (expect clean after unify)
- `multi-view-reuse.md`: narrative of shared ID across views
- `tool-sequence.md`: expected MCP + helper sequence
