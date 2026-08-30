---
name: archi-elicit
description: "Normalize architectural intent into the orchestrator field set. Orchestrator-dispatched; no model mutations."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# archi-elicit

## When to use

Orchestrator-dispatched. Use when raw intent is incomplete and must be normalized into the orchestrator field set. Never user-invoked.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Turn free-text or partial architectural intent into a complete, plain-language field set the orchestrator can use for View Plan drafting (SPEC-D-01). This skill **never** mutates the Archi model.

## Hard rules

1. **No MCP mutations.** Do not call `create-element`, `create-relationship`, `create-view`, `clone-view`, `bulk-mutate`, `update-element`, `update-relationship`, `delete-element`, or other mutating tools.
2. **Orchestrator-dispatched only** (SPEC-02 / SPEC-D-13).
3. **No ArchiMate metamodel table dumps** (NG-4). Plain language only.
4. **User governs** unresolved scope and decisions (NG-3). Surface unknowns; do not invent answers silently.
5. Shared contract: see `docs/CREATE_PATH.md` (non-mutating row).

## Inputs

From the orchestrator hand-off:

| Field | Source |
|-------|--------|
| Raw intent | Free text, bullets, or prior answers |
| Known fields | Any already-filled orchestrator fields |
| Scope hints | Optional in/out notes from user |

## Field set (must cover)

Match orchestrator Step 1:

| Field | Prompt cue |
|-------|------------|
| Problem | What problem or opportunity are we addressing? |
| Stakeholders | Who cares about the outcome? |
| Concerns | What worries or success criteria do they have? |
| Scope | What is in / out for this modelling pass? |
| Current state | What exists today (systems, processes, constraints)? |
| Target state | What should be true afterward? |
| Expected outcome | What deliverable does the user want from this run? |

## Procedure

### Step 1 — Ingest

Read raw intent and any known fields. Do not re-ask fields that are already clear and complete.

### Step 2 — Gap-fill

For each empty or vague field, either:

- Derive a candidate from context and mark it `inferred`, or
- Record it under **Open Questions** with a concrete ask

Prefer short plain-language bullets over jargon.

### Step 3 — Normalize

Produce a structured intent object (markdown or JSON) with all seven fields populated or explicitly `unknown` plus open questions.

### Step 4 — Sanity pass

- Stakeholders paired with at least one concern when possible
- Scope has both in and out when the user gave boundaries
- Expected outcome is a deliverable (views, decisions, migration path), not a vague hope

## Output template

```markdown
## Normalized Intent

### Problem
…

### Stakeholders
- …

### Concerns
- …

### Scope
- In: …
- Out: …

### Current state
…

### Target state
…

### Expected outcome
…

### Open Questions
- …

### Inferences
| Field | Value | Basis |
|-------|-------|-------|
| … | … | … |
```

Optional JSON twin for machine hand-off:

```json
{
  "problem": "",
  "stakeholders": [],
  "concerns": [],
  "scope": {"in": [], "out": []},
  "current_state": "",
  "target_state": "",
  "expected_outcome": "",
  "open_questions": [],
  "inferences": []
}
```

## Return to orchestrator

Hand back:

1. Normalized Intent markdown (and optional JSON)
2. List of fields still `unknown`
3. Confirmation that **no MCP mutations** were performed
4. Inferred fields stay `inferred`. Downstream specialists must carry them as `Evidence: inferred - elicit` (or a more specific source). Do not upgrade an inference to stated.
