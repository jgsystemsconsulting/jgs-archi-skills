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

## Compliance (COMP-01, COMP-02)

1. Confirm types against MCP resources (`archimate://reference/archimate-layers`, `archimate://reference/archimate-relationships`).
2. On violation: **explain** and **propose** a compliant alternative; never silent-apply illegal edges or types.
3. Optional offline gate: `python helpers/compliance_checklist.py report.json`.

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
