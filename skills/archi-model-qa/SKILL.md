---
name: archi-model-qa
description: "Model QA specialist; orchestrator-dispatched. Compliance and coherence checks with explain-and-propose fixes."
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# archi-model-qa

## When to use

Orchestrator-dispatched. Use to run compliance and coherence checks with explain-and-propose findings.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Run compliance and coherence checks on the working model/views: element types, relationship legality, abstraction consistency, cross-view naming, and duplicates. Explain violations and propose compliant alternatives; never silent-apply illegal fixes (SPEC-D-09 / COMP-02 / OBJ-5).

## Hard rules

1. Prefer **read + report**. Mutating fixes only when View Plan confirmation is approved and the user/orchestrator explicitly authorizes applying a listed fix set.
2. **Orchestrator-dispatched only** (SPEC-02).
3. **Follow `docs/CREATE_PATH.md`** compliance section (OBJ-5 depth).
4. **No metamodel table dumps** (NG-4).
5. Offline deep assist: `python helpers/compliance_validate.py slice.json [--json]` on a model-slice snapshot (primary OBJ-5 path).
6. Optional thin boolean gate: `python helpers/compliance_checklist.py report.json`.
7. Coherence assists (OBJ-4): `python helpers/reuse_inspect.py …`, `python helpers/naming_convention.py conflicts usages.json`.
8. House style: python helpers/docs_coverage.py slice.json --require-evidence ; python helpers/naming_convention.py aspect-hints usages.json ; python helpers/folder_convention.py slice.json. Explain-and-propose. Never auto-rename or auto-move.

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Confirmation status | yes | For any mutating fix apply |
| Scope | yes | Views, folders, or whole model slice |
| Prior specialist results | optional | Known creates to re-check |

## MCP resources

- `archimate://reference/archimate-layers`
- `archimate://reference/archimate-relationships`
- `archimate://reference/archimate-view-patterns`
- `archimate://recipes/index`

## MCP tools

Read: `get-views`, `get-view-contents`, `get-element`, `get-relationships`, `search-elements`, `find-concept-usage`, `get-model-info`, `get-folders`, `get-folder-tree`  
Optional authorized fix: `update-element`, `update-relationship`, `create-relationship`, `delete-relationship`, `move-to-folder` (only listed, user-approved fixes)

## Procedure

OBJ-4 coherence: before each create, search existing elements; run `helpers/reuse_inspect.py` on the snapshot when useful; apply `helpers/naming_convention.py` normalize; update run-scoped `reuse_registry`; never auto-merge `ambiguous`. Hand-back must list **reused** vs **created** IDs.

OBJ-5 compliance: build a model-slice JSON from scope; run `helpers/compliance_validate.py`; surface every finding with problem + proposed_alternative. Live: also read MCP relationship/layer resources. Never silent-apply.

### Step 1 — Scope gather
Load target views and related elements/relationships into a slice snapshot when offline validation is needed. Call `get-folder-tree`, join ancestor folder names with `/` onto each element's and view's `folder_path`, then run `folder_convention.py`. Missing tree is needs-user / blocked, not a silent skip.

### Step 2 — Check dimensions
1. Element types coherent with layer/viewpoint purpose: MCP layers + `compliance_validate` element_type_known
2. Relationship source/target combinations and permitted types: MCP relationships + validator endpoints/type checks
3. Abstraction-level consistency: validator abstraction_level_consistent
4. Duplicate concepts (same name/type near-matches): search snapshot + `reuse_inspect` / duplicate_label conflicts
5. Cross-view naming consistency: `naming_convention.detect_conflicts` and/or validator cross_view_naming_consistent
6. Orphans not justified by hand-off
7. Unresolved `ambiguous` reuse decisions still open in the registry
8. Undispositioned hand-off candidates (CP-G3). A candidate with no captured / folded / needs-user / out-of-scope row is a finding; explain and propose (ask the user, or fold with a reason). Never silent-drop.
9. Documentation house style (Evidence line on elements, not type restatement): docs_coverage --require-evidence
10. Aspect naming hints: naming_convention aspect-hints (low severity; never auto-rename)
11. Folder placement: folder_convention.py on a slice that includes folder_path (propose move-to-folder)

### Step 3 — Findings file
Write structured findings (markdown + optional slice JSON for `compliance_validate` / thin checklist JSON).

### Step 4 — Propose alternatives
For each violation: problem, why illegal/risky, compliant alternative, optional MCP action if approved. Prefer validator `proposed_alternative` text when offline.

### Step 5 — Apply only if authorized
If fix set approved: apply minimally; re-read to confirm. Else stop at report.

### Step 6 — Hand-back

## Output template

```markdown
## Specialist Result: archi-model-qa

**Status:** completed | needs-user | blocked
**Fixes applied:** none | listed IDs

### Findings
| ID | Severity | Object | Problem | Proposed alternative |
|----|----------|--------|---------|----------------------|
| F1 | high/med/low | … | … | … |

### Compliance
- compliance_validate slice path / finding count
- optional compliance_checklist report.json path

### Open questions
- …
```

## Return to orchestrator

1. Findings table (explain + propose)
2. Whether modelling can proceed or must pause
3. Explicit note: no silent illegal fixes
