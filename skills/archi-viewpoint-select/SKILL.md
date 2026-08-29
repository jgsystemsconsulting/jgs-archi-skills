---
name: archi-viewpoint-select
description: "Ground ArchiMate viewpoint choices to stakeholder, concern, purpose, and abstraction level. Orchestrator-dispatched."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# archi-viewpoint-select

## When to use

Orchestrator-dispatched. Use after a draft View Plan exists and each viewpoint must be traced to stakeholder, concern, purpose, and abstraction. Never user-invoked.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Given intent plus draft viewpoints (from the orchestrator), produce a **Viewpoint Trace Table** proving each choice maps to stakeholder, concern, purpose, and abstraction level (VSEL-04 / VIEW-01). When no standard viewpoint fits, propose an organisation-specific viewpoint with justification that stays ArchiMate-compliant (VSEL-06 / VIEW-02). List rejected alternatives so the user can see the choice space (VSEL-07 / NG-3).

## Hard rules

1. **No MCP mutations.** Do not call `create-element`, `create-relationship`, `create-view`, `clone-view`, `bulk-mutate`, `update-element`, `update-relationship`, `delete-element`, or other mutating tools. Read-only resources only (VSEL-10).
2. **Do not copy ArchiMate metamodel tables** into the trace or chat. Prefer MCP resources for definitions (NG-4). Offline, use plain-language names and the local matrix helper keys.
3. **Dispatch only via orchestrator** (SPEC-02).
4. **User governs** organisation-specific proposals and final viewpoint set (NG-3).

## Inputs

From the orchestrator hand-off:

| Field | Source |
|-------|--------|
| Intent axes | Problem, stakeholders, concerns, scope, purpose (design/decide/inform), abstraction (overview/detail/mixed) |
| Draft viewpoints | Optional bullets from a preliminary View Plan |
| Model context | Optional existing view names (inspect-only; no creates) |

## MCP resources (read-only)

When Bridge is connected, read as needed:

- `archimate://recipes/index`
- `archimate://reference/archimate-view-patterns`
- `archimate://reference/archimate-layers`

Do not invent other resource URIs. Offline: state what you would read and continue with matrix keys + plain language.

## Procedure

### Step 1 — Normalize intent axes

Build a structured intent object:

```json
{
  "stakeholders": ["role-or-name", "..."],
  "concerns": ["concern-tag", "..."],
  "purpose": "design|decide|inform",
  "abstraction": "overview|detail|mixed"
}
```

Map free-text purpose/abstraction into those enums when clear; otherwise keep tokens for concern/stakeholder matching.

### Step 2 — Rank standard candidates (offline helper)

Run the suite matrix helper (keys/axes only; definitions remain on MCP):

```bash
python helpers/viewpoint_selection_matrix.py path/to/intent.json --top 8
```

Interpret:

- `ranked[]` — candidate `key` / `label` / `score` / `matched`
- `standard_fit` — true when top score ≥ threshold (default 3)
- Prefer labels that also appear in MCP recipes/view-patterns when online

### Step 3 — Build the Trace Table

Select enough viewpoints to cover the stakeholder×concern set (typically 2–6). For each selected viewpoint fill:

| Column | Meaning |
|--------|---------|
| Viewpoint | Standard name (or org-specific name) |
| Stakeholder | Who this view serves |
| Concern | What worry/success criterion it addresses |
| Purpose | design / decide / inform (plain words OK) |
| Abstraction | overview / detail / mixed |
| Standard? | `yes` if standard ArchiMate/recipe viewpoint; `no` if org-specific |
| Justification | One or two sentences tying axes → choice; cite matrix matches or MCP recipe when used |

### Step 4 — Organisation-specific path (when needed)

If `standard_fit` is false **or** a stakeholder×concern pair is uncovered by standard candidates:

1. Propose under **Organisation-Specific Proposals** with: name, stakeholders, concerns, purpose, abstraction, **compliance constraints** (allowed layers only; no illegal element mixes; still ArchiMate-native concepts).
2. Set `Standard?` = `no` and justify why standards were insufficient.
3. Never invent new metamodel element types or relationship kinds.

### Step 5 — Rejected alternatives

List notable non-selected candidates (from matrix or drafts) with a one-line rejection reason (e.g. "no facilities concern", "too detailed for executive audience").

### Step 6 — Schema check

Write the artifact (chat or file) with exactly these H2 headings and a header row containing all required columns, then:

```bash
python helpers/viewpoint_trace_schema.py path/to/trace.md
```

Fix until exit 0.

## Output template

```markdown
## Viewpoint Trace Table
| Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Standard? | Justification |
|-----------|-------------|---------|---------|-------------|-----------|---------------|
| … | … | … | … | … | yes/no | … |

## Organisation-Specific Proposals

None this pass.
# or:
### <Name>
- Stakeholders / concerns / purpose / abstraction
- Why standards insufficient
- Compliance constraints (layers, no illegal mixes)

## Rejected Alternatives

| Viewpoint | Why rejected |
|-----------|--------------|
| … | … |
```

## Return to orchestrator

Hand back:

1. Schema-valid Trace Table markdown
2. List of viewpoint names + abstraction levels for View Plan **Proposed Viewpoints**
3. Flag if any org-specific proposal needs user confirmation before modelling
