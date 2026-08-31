<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Shared specialist modelling contract

Binding contract for orchestrator-dispatched specialists that work the Archi model via the JGS Archi Bridge MCP (OBJ-3 / SPEC-D-12..15). Every specialist skill must follow this document. Do not fork a private create path.

## Scope

| Specialist | Mutations? | Notes |
|------------|------------|-------|
| `archi-elicit` | No | Intent normalization only |
| `archi-viewpoint-select` | No | Trace Table only (v1.1 complete) |
| `archi-motivation` | Yes (post-confirm) | Layer modelling |
| `archi-capability-strategy` | Yes (post-confirm) | Layer modelling |
| `archi-business` | Yes (post-confirm) | Layer modelling |
| `archi-application` | Yes (post-confirm) | Layer modelling |
| `archi-technology-physical` | Yes (post-confirm) | Layer modelling |
| `archi-implementation-migration` | Yes (post-confirm) | Layer modelling |
| `archi-traceability` | Yes (post-confirm) | Cross-layer relationships |
| `archi-model-qa` | Prefer read + report; fixes only when user-approved | Compliance |
| `archi-layout` | Yes (post-confirm) | Layout tools on existing views |
| `archi-documentation` | Yes (post-confirm) | Documentation fields + summary |

## Run gates (hedge-free)

Guidance elsewhere in this file may use "prefer" or "when useful". The table below may not. If a gate is unmet, the draft is not ready unless the specialist names an exception: which gate, which view or element, and why. "Ran long" is not an exception.

| ID | Gate | Pass condition |
|----|------|----------------|
| CP-G1 | Confirm-before-mutate | No mutating MCP call unless View Plan confirmation is `approved`. |
| CP-G2 | Fresh IDs | At the start of every specialist, and after any compaction, re-query IDs with `search-elements` / `get-view-contents`. Identify unnamed notes, images, junctions, and groups by content and geometry, never by batch order. |
| CP-G3 | Disposition complete | Every candidate in the hand-off is `captured`, `folded`, `needs-user`, or `out-of-scope`. Silence is a fail. |
| CP-G4 | No invention | Every created element has `Evidence: stated \| inferred \| existing - <source>` as the first documentation line. No on-canvas element without that citation. |
| CP-G5 | Annotate last | Notes, legends, and images are the last objects placed on a view. Omit `height` on notes. Place notes with `position: below-content`. A later geometry change re-opens CP-G6. |
| CP-G6 | Render close-out | After any add, move, resize, or style on a view, including notes, the last actions are `assess-layout` (dispose every non-pass `ratingBreakdown` dimension; `partial` and `not-checked` are unverified) and an `export-view` PNG that is inspected. |
| CP-G7 | First generation is a draft | The documentation specialist ends the run at a draft checkpoint. Do not present the model as finished. |

Offline assist for CP-G3: `python helpers/disposition.py ledger.md`.

## When mutations are allowed (SPEC-D-15 / NG-3)

1. User has **approved** the orchestrator View Plan confirmation gate.
2. Orchestrator hand-off includes confirmation status `approved` (or equivalent explicit flag).
3. Specialist stays inside the confirmed viewpoints, layers, and scope.
4. No specialist silently expands scope or locks architectural decisions without surfacing them.

If confirmation is missing or aborted: **stop**. Produce a hand-back note; do not call mutating tools.

## Working mode (the model is the checkpoint)

A modelling run can compact or stop mid-way. Conversation memory is not the ledger.

1. Re-query IDs at the start of every specialist (`search-elements`, `get-view-contents`). Do not reuse IDs remembered from an earlier turn.
2. Unnamed view objects (notes, images, junctions, groups) have no name to match. Identify them by content and geometry from a fresh `get-view-contents`. Never assume "note 2 of 3" from an earlier `bulk-mutate` batch.
3. Keep element names stable and domain-derived so `get-or-create-element` / search-before-create stay idempotent.
4. Optional: write a short run marker with `update-model` (confirmation status, viewpoints in scope, last specialist completed) so the next run diffs against the model.

## Orchestrator-dispatched only (SPEC-D-13 / SPEC-02)

- Specialists are not primary user entrypoints.
- User invokes `archi-orchestrator`; orchestrator dispatches specialists.
- Skill frontmatter must keep orchestrator-dispatched framing.

## Inspect before create (SPEC-03, SPEC-04)

1. Call `search-elements` / `get-or-create-element` before `create-element`.
2. Reuse existing concept IDs across views.
3. Keep naming consistent for the same real-world concept.
4. Prefer `find-concept-usage` / `get-view-contents` when attaching to existing structure.

## Provenance on create (CP-G4)

Every created element starts its `documentation` field with:

```
Evidence: stated | inferred | existing - <source>
```

- `stated`: the user or the approved View Plan said it
- `inferred`: the specialist deduced it (keep elicit inferences; do not upgrade them)
- `existing`: already in the model and reused

Never write a bare `Rationale:` line for an inferred why. Omit Rationale, or write `Rationale (inferred):`. Do not add evidence specializations or label glyphs.

Creating specialists (motivation, capability-strategy, business, application, technology-physical, implementation-migration, traceability) include a **Candidate disposition** table in the Specialist Result. Valid dispositions: `captured` (target `element @ view`), `folded` (parent plus reason), `needs-user` (question), `out-of-scope` (why). Validate with `python helpers/disposition.py`.

## House style (modelling conventions)

Binding content-quality rules live in `docs/MODELLING_CONVENTIONS.md`
(naming by aspect, description recipe, default Archi folder tree, view
hygiene). This is JGS house style, not an ArchiMate catalog (NG-4).
Language legality stays on MCP resources and `helpers/compliance_validate.py`.

Offline, on a captured slice, after a modelling batch (model-qa prefers
these on a captured slice; eval G6 omits `--require-evidence`):

```text
python helpers/docs_coverage.py slice.json --require-evidence [--json]
python helpers/naming_convention.py conflicts usages.json
python helpers/naming_convention.py aspect-hints usages.json
python helpers/folder_convention.py slice.json [--json]
```

House-style findings are explain-and-propose only. Never auto-rename or
auto-move.

## Model coherence and reuse (OBJ-4 / COH-*)

Binding for inspect-before-create depth beyond the basic search guidance above.

### Offline helpers (deterministic)

```text
python helpers/reuse_inspect.py "<Name>" --type <Type> --inventory snapshot.json [--json]
python helpers/naming_convention.py normalize "<Name>"
python helpers/naming_convention.py conflicts usages.json
```

- Input: candidate name/type + element inventory snapshot (`[{id,name,type}, ...]`).
- Output decision: `reuse` | `create` | `ambiguous` with match IDs and scores.
- Does **not** call MCP. Use after `search-elements` (or on a captured inventory) to record the decision.
- Normalize labels (title-collapse-v1) and flag cross-view name divergence or duplicate labels.

### Run-scoped reuse registry

Maintain a **run-scoped** map for the modelling session (orchestrator hand-off field `reuse_registry`):

| concept_key | element_id | decision | notes |
|-------------|------------|----------|-------|
| applicationcomponent:customer portal | id-… | reuse | from search |

- `concept_key` = normalized `type:name` (or name-only when type unknown).
- Every specialist **reads** the registry before create and **writes** new reuse/create outcomes.
- Prefer registry hit over a second create for the same concept across views.

### Naming policy

- Default policy id: `title-collapse-v1` (trim, collapse whitespace, title case).
- Orchestrator hand-off field `naming_policy` carries the policy id (and optional overrides).
- Apply `normalize_name` before create; keep the same display name when reusing an ID across views.

### Ambiguous matches (NG-3)

- **Never** auto-merge `ambiguous` decisions.
- Surface candidates to the user/orchestrator; wait for an explicit choice (reuse id X, create new, or rename).
- model-qa reports unresolved ambiguities as findings with explain-and-propose alternatives.

### Live MCP sequence (mutating specialists)

1. `search-elements` (and/or `find-concept-usage`) for the candidate.
2. Optionally run `reuse_inspect` on the search snapshot for a structured decision record.
3. On `reuse`: `add-to-view` / relate existing ID; do not `create-element`.
4. On `create`: `get-or-create-element` or `create-element` with normalized name; register ID.
5. Place new elements with `create-folder` / `move-to-folder` when the target
   layer folder is missing or the element landed in the default bucket. Always
   propose the JGS default tree from `docs/MODELLING_CONVENTIONS.md`.
6. On `ambiguous`: stop mutating that concept; hand back open question.
7. Record reused vs created IDs in the specialist hand-back payload.
8. Relationship documentation: `create-relationship` takes no documentation
   parameter. Set it immediately after create with `update-relationship`
   (id, documentation); a relationship without documentation is a run defect.
9. Before hand-back, verify post-conditions against the model, not memory:
   every planned element and relationship exists (exactly once), and every
   element and relationship carries a documentation field. Re-read via
   `search-elements` / `get-relationships`; never trust in-run bookkeeping
   alone.

## Compliance (COMP-01, COMP-02, OBJ-5 / COMP-03+)

Binding for ArchiMate legality and consistency. Violations are **explained** with a **compliant alternative proposed**. Never silent-apply illegal types, edges, or renames (COMP-02 / NG-3).

### Live path (preferred when Bridge is up)

1. Confirm element types against MCP `archimate://reference/archimate-layers`.
2. Confirm relationship types and source/target legality against MCP `archimate://reference/archimate-relationships`.
3. Read relevant recipes/view-patterns before non-trivial structure (see Recipe section below).
4. On violation: stop the illegal create; report problem + alternative; wait for user/orchestrator choice.

### Offline depth (OBJ-5)

Deep validator:

```text
python helpers/compliance_validate.py slice.json [--allowlist path] [--json]
```

- Input model-slice: `{elements:[{id,name,type,abstraction?}], relationships:[{id,type,source,target}], view_usages?:[…]}`.
- Fixture allowlist: `helpers/fixtures/compliance_allowlist.json` (minimal captured subset; **not** a skill-owned ArchiMate catalog; NG-4). Live MCP remains SoT.
- Checks: element_type_known, relationship_type_permitted, relationship_endpoints_valid, abstraction_level_consistent, cross_view_naming_consistent.
- Output findings: `{check_id, object_refs, problem, proposed_alternative}`; never mutates the model.
- Thin boolean gate (still valid): `python helpers/compliance_checklist.py report.json` for pre-scored check maps.
- Coherence helpers remain available: `reuse_inspect`, `naming_convention` (OBJ-4).

### When to run which

| Situation | Action |
|-----------|--------|
| Live modelling create | MCP reference resources first; optional offline validate on a captured slice after batch |
| CI / offline evidence | `compliance_validate` on fixture slices |
| Quick self-check boolean | `compliance_checklist` if you already have pass/fail map |
| model-qa pass | Prefer `compliance_validate` findings table; coherence helpers for duplicates/naming |

### Findings hand-back

Every compliance note in specialist/orchestrator payloads must carry: check id (when known), object refs, problem explanation, proposed alternative. Do not auto-apply fixes.

## Rationale, NL-change, and completion summary (OBJ-6 / RATE-01..03)

Binding for structured view rationale, safe natural-language change regeneration, and end-of-run completion summary. Rationale and summary text live in the Archi model documentation fields via MCP (stateless skills). Offline helpers are deterministic and never call MCP.

### Draft and validate rationale (RATE-01)

1. Per significant view, draft markdown with required sections: Purpose, Stakeholders and Concerns, Viewpoint, Questions Answered, Assumptions, Decisions, Exclusions, Open Questions.
2. Bodies must be non-empty (whitespace-only fails).
3. Offline validate before write:

```text
python helpers/rationale_schema.py path/to/rationale.md
python helpers/rationale_schema.py --bundle DIR|bundle.json [--json]
```

4. Fix until exit 0 (warn-only order drift may remain).

### Record in model (live, post-confirm)

1. Mutations only after View Plan confirmation (SPEC-D-15 / NG-3).
2. Write validated rationale into view (or element) documentation fields via inventory tools only: `update-view`, `update-element`, `update-model` as appropriate.
3. Never delete shared structure to refresh documentation text.
4. Prefer one rationale blob per significant view; keep section headings stable so re-validation stays possible offline.

### NL-change regeneration (RATE-02)

1. User supplies a natural-language change note; skill may interpret free text into structured keywords, but offline impact planning stays deterministic.
2. Build a view/element inventory snapshot (`views[{id,name,keywords?}]`, `elements[{id,name,shared?,view_ids?}]`).
3. Run impact plan: `python helpers/nl_change_impact.py note.txt inventory.json`
4. Impact plan fields: `affected_views`, `regenerate_scope`, `must_reuse_element_ids`, `exclusions`, `notes`.
5. Before regenerate: require the impact plan; reuse every ID in `must_reuse_element_ids`; never recreate shared concepts as duplicates; never auto-apply without user confirmation (NG-3).
6. Regenerate only listed views (layout/layer specialists as needed); update rationale deltas; re-validate rationale.

### Completion summary (RATE-03)

1. End every modelling run with a completion summary covering at minimum: Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run, Deliberately Deferred, Improve Next. First generation is a draft (CP-G7).
2. Offline validate: `python helpers/completion_summary_schema.py path/to/summary.md`
3. Orchestrator consumes the documentation specialist summary in the run closeout; do not invent new mutating tools.

### When to run which (OBJ-6)

| Situation | Action |
|-----------|--------|
| After significant views exist | Draft + `rationale_schema` validate; write via MCP if confirmed |
| User NL change request | `nl_change_impact` plan → user confirm → regenerate with reuse IDs |
	| End of run | `completion_summary_schema` validate; return summary to orchestrator |

## Recipe and reference reads (NG-4 / SPEC-D-14)

Before non-trivial views, **read** (do not copy tables into the skill or chat dumps):

- `archimate://recipes/index`
- Relevant recipe URIs (e.g. `archimate://recipes/motivation`, `archimate://recipes/behaviour-process-flow`, `archimate://recipes/application-integration`, `archimate://recipes/technology-deployment`, `archimate://recipes/roadmap-migration`)
- `archimate://reference/archimate-view-patterns`
- `archimate://reference/archimate-layers`
- `archimate://reference/archimate-relationships` as needed

Never paste ArchiMate metamodel catalogs into skill markdown. Inventory allowlist: `docs/mcp/archi-bridge-inventory.json`.

## Inventory tools only

Use only tool names listed in the inventory. Common modelling set:

`search-elements`, `get-or-create-element`, `create-element`, `create-relationship`, `create-view`, `add-to-view`, `get-view-contents`, `get-element`, `get-relationships`, `find-concept-usage`, `update-element`, `update-view`, `get-folders`, `get-folder-tree`, `create-folder`, `move-to-folder`

Layout set (layout specialist): `auto-layout-and-route`, `layout-flat-view`, `assess-layout`, `apply-positions`, `export-view`, `update-view-object`, `add-note-to-view`, `get-view-contents`, and related inventory layout tools.

Layout footguns (layout specialist; recipes remain source of truth):

- Grouped or nested default for structure views with more than about 10 elements; flat needs a recorded reason
- Annotate last (CP-G5): omit `height` on `add-note-to-view` and note `update-view-object`; `position: below-content`, never `above-content`
- Junctions about 14 by 14; do not pass a layer-folder `folderId` for a Junction
- Nested hub (six or more connections): resize the hub, then `auto-route-connections`; re-route alone is inert
- Walk `ratingBreakdown`; do not sign off on `overallRating` alone; `partial` and `not-checked` are unverified
- Last action includes `export-view`; the PNG is authoritative where the metric under-counts
- Literal `&` in names and labels, never `&amp;`

Do not invent tool names.

## Return-to-orchestrator payload

Every specialist ends with a structured hand-back:

1. **Status:** completed / blocked / needs-user
2. **Views touched:** names/IDs created or updated
3. **Elements/relationships:** created or reused (IDs when known)
4. **Compliance notes:** violations found and alternatives proposed
5. **Open questions:** decisions still needing the user
6. **Confirmation assumption:** restate that work ran under approved View Plan (or that no mutations ran)
7. **Candidate disposition:** table of every hand-off candidate (creating specialists). `archi-model-qa` treats an undispositioned candidate as a finding; do not silent-fix.

## Hard non-goals

- No modification of jgs-archi-mcp (NG-1)
- No alternate renderer or non-Archi EA tool (NG-2, NG-5)
- No fully autonomous architect (NG-3)
- No ArchiMate table dumps inside skills (NG-4)
