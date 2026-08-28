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

## When mutations are allowed (SPEC-D-15 / NG-3)

1. User has **approved** the orchestrator View Plan confirmation gate.
2. Orchestrator hand-off includes confirmation status `approved` (or equivalent explicit flag).
3. Specialist stays inside the confirmed viewpoints, layers, and scope.
4. No specialist silently expands scope or locks architectural decisions without surfacing them.

If confirmation is missing or aborted: **stop**. Produce a hand-back note; do not call mutating tools.

## Orchestrator-dispatched only (SPEC-D-13 / SPEC-02)

- Specialists are not primary user entrypoints.
- User invokes `archi-orchestrator`; orchestrator dispatches specialists.
- Skill frontmatter must keep orchestrator-dispatched framing.

## Inspect before create (SPEC-03, SPEC-04)

1. Call `search-elements` / `get-or-create-element` before `create-element`.
2. Reuse existing concept IDs across views.
3. Keep naming consistent for the same real-world concept.
4. Prefer `find-concept-usage` / `get-view-contents` when attaching to existing structure.


## Model coherence and reuse (OBJ-4 / COH-*)

Binding for inspect-before-create depth beyond the basic search guidance above.

### Offline helpers (deterministic)

- `python helpers/reuse_inspect.py "<Name>" --type <Type> --inventory snapshot.json [--json]`
  - Input: candidate name/type + element inventory snapshot (`[{id,name,type}, ...]`).
  - Output decision: `reuse` | `create` | `ambiguous` with match IDs and scores.
  - Does **not** call MCP. Use after `search-elements` (or on a captured inventory) to record the decision.
- `python helpers/naming_convention.py normalize "<Name>"`
- `python helpers/naming_convention.py conflicts usages.json`
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
5. On `ambiguous`: stop mutating that concept; hand back open question.
6. Record reused vs created IDs in the specialist hand-back payload.

## Compliance (COMP-01, COMP-02, OBJ-5 / COMP-03+)

Binding for ArchiMate legality and consistency. Violations are **explained** with a **compliant alternative proposed**. Never silent-apply illegal types, edges, or renames (COMP-02 / NG-3).

### Live path (preferred when Bridge is up)

1. Confirm element types against MCP `archimate://reference/archimate-layers`.
2. Confirm relationship types and source/target legality against MCP `archimate://reference/archimate-relationships`.
3. Read relevant recipes/view-patterns before non-trivial structure (see Recipe section below).
4. On violation: stop the illegal create; report problem + alternative; wait for user/orchestrator choice.

### Offline depth (OBJ-5)

- Deep validator: `python helpers/compliance_validate.py slice.json [--allowlist path] [--json]`
  - Input model-slice: `{elements:[{id,name,type,abstraction?}], relationships:[{id,type,source,target}], view_usages?:[…]}`.
  - Fixture allowlist: `helpers/fixtures/compliance_allowlist.json` (minimal captured subset; **not** a skill-owned ArchiMate catalog — NG-4). Live MCP remains SoT.
  - Checks: element_type_known, relationship_type_permitted, relationship_endpoints_valid, abstraction_level_consistent, cross_view_naming_consistent.
  - Output findings: `{check_id, object_refs, problem, proposed_alternative}` — never mutates the model.
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

`search-elements`, `get-or-create-element`, `create-element`, `create-relationship`, `create-view`, `add-to-view`, `get-view-contents`, `get-element`, `get-relationships`, `find-concept-usage`, `update-element`, `update-view`

Layout set (layout specialist): `auto-layout-and-route`, `layout-flat-view`, `assess-layout`, `apply-positions`, and related inventory layout tools.

Do not invent tool names.

## Return-to-orchestrator payload

Every specialist ends with a structured hand-back:

1. **Status** — completed / blocked / needs-user
2. **Views touched** — names/IDs created or updated
3. **Elements/relationships** — created or reused (IDs when known)
4. **Compliance notes** — violations found and alternatives proposed
5. **Open questions** — decisions still needing the user
6. **Confirmation assumption** — restate that work ran under approved View Plan (or that no mutations ran)

## Hard non-goals

- No modification of jgs-archi-mcp (NG-1)
- No alternate renderer or non-Archi EA tool (NG-2, NG-5)
- No fully autonomous architect (NG-3)
- No ArchiMate table dumps inside skills (NG-4)
