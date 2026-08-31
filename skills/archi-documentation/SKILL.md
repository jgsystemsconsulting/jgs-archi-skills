---
name: archi-documentation
description: "Documentation/rationale specialist; orchestrator-dispatched. Writes structured rationale and completion summary via MCP."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# archi-documentation

## When to use

Orchestrator-dispatched after View Plan confirmation when rationale and a completion summary must be written into the model.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Record structured rationale for significant views into model documentation fields via MCP, support natural-language change notes without destroying shared elements, and produce a completion summary for the modelling run (SPEC-D-11 / RATE-01..03 / OBJ-6).

## Hard rules

1. **Mutations only after View Plan confirmation** (SPEC-D-15) when writing into the model.
2. **Orchestrator-dispatched only** (SPEC-02).
3. **Follow `docs/CREATE_PATH.md`** including the OBJ-6 rationale / NL-change / completion-summary section.
4. Validate rationale markdown with `python helpers/rationale_schema.py` before write when a file artifact exists (non-empty required sections).
5. NL regeneration must run an impact plan first and reuse element IDs; never recreate shared concepts as duplicates (RATE-02).
6. Validate completion summary with `python helpers/completion_summary_schema.py` before hand-back when a file artifact exists.

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Confirmation status | yes | |
| Views to document | yes | |
| View Plan + Trace Table | recommended | Purpose, stakeholders, concerns |
| Modelling decisions | optional | From prior specialists |
| NL change request | optional | For regenerate path |
| View/element inventory | optional | For NL impact helper |

## MCP resources

- `archimate://recipes/index`
- `archimate://reference/archimate-view-patterns`

## MCP tools

Read: `get-view-contents`, `get-element`, `get-views`  
Write docs: `update-element`, `update-view`, `update-model` as appropriate for documentation fields  
Never delete shared structure to refresh text

## Offline helpers (OBJ-6)

```bash
# Rationale depth (single file or multi-view bundle)
python helpers/rationale_schema.py path/to/rationale.md
python helpers/rationale_schema.py --bundle path/to/dir-or-bundle.json [--json]

# NL-change impact (deterministic; never mutates)
python helpers/nl_change_impact.py note.txt inventory.json

# Completion summary structure
python helpers/completion_summary_schema.py path/to/summary.md
```

Required rationale sections (helper-enforced): Purpose, Stakeholders and Concerns, Viewpoint, Questions Answered, Assumptions, Decisions, Exclusions, Open Questions. Bodies must be non-empty.

Required completion-summary blocks: Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run, Deliberately Deferred, Improve Next. First generation is a draft (CP-G7). A legitimate empty deferred/next block is the word `none`.

## Procedure

OBJ-4 coherence: before each create, search existing elements; run `helpers/reuse_inspect.py` on the snapshot when useful; apply `helpers/naming_convention.py` normalize; update run-scoped `reuse_registry`; never auto-merge `ambiguous`. Hand-back must list **reused** vs **created** IDs.

OBJ-5 compliance: optional `helpers/compliance_validate.py` on a captured slice; explain-and-propose only.

### Step 0 — Gate
Stop if writing to model without approval.

### Step 1 — Draft rationale
Per significant view, draft rationale markdown covering schema sections from View Plan + specialist results. Prefer non-empty concrete sentences, not placeholders.

### Step 2 — Validate rationale
Run `rationale_schema` helper (file or `--bundle`); fix until exit 0. Record schema validation status for hand-back.

### Step 3 — Record in model
Write validated text into the view/element documentation fields via MCP update tools. Do not delete shared structure.

### Step 4 — NL changes (RATE-02)
If user requested changes:

1. Capture or assemble inventory JSON (`views`, `elements` with `shared` / `view_ids`).
2. Run `helpers/nl_change_impact.py` on the change note + inventory.
3. Present impact plan (affected views, must-reuse IDs, exclusions) to user/orchestrator; wait for confirmation (NG-3).
4. Regenerate visuals via layout/layer specialists **only** for `regenerate_scope`; reuse every `must_reuse_element_ids` entry; never recreate shared concepts.
5. Update rationale deltas for affected views; re-run rationale validation.

### Step 5 — Completion summary (RATE-03)
Emit run summary covering required blocks. Validate with `completion_summary_schema` when a file artifact exists.
Do not present the model as finished. Deferred and Next are required blocks; use `none` when there is nothing to list.

### Step 6 — Hand-back
Return Specialist Result including schema validation status, impact plan path/fields when NL path ran, and completion summary.

## Output template

```markdown
## Specialist Result: archi-documentation

**Status:** completed | blocked | needs-user

### Rationale written
| View | Schema valid | Model field updated |
|------|--------------|---------------------|
| … | yes | yes/no |

### NL-change impact (if any)
- Affected views: …
- Must-reuse element IDs: …
- User confirmation: pending | approved | aborted

### Completion summary
- Views Touched: …
- Decisions: …
- Open Questions: …
- Confirmation Status: …
- Specialists Run: …
- Deliberately Deferred: …
- Improve Next: …

### Schema validation
- rationale_schema: pass | fail
- completion_summary_schema: pass | fail

### Open questions
- …
```

## Return to orchestrator

1. Specialist Result including completion summary and validation status
2. Paths to rationale / impact / summary artifacts when the run asks for a file capture
