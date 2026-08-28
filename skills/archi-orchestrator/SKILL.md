---
name: archi-orchestrator
description: "Elicit architectural intent and produce a plain-language ArchiMate view plan via JGS Archi Bridge MCP (user-governed). Trigger: /archi-orchestrator"
argument-hint: "[optional free-text intent]"
---

# archi-orchestrator

User-invoked entrypoint for agent-guided architecture work in Archi. You elicit intent, optionally ground on MCP **resources** (read-only), and produce a **plain-language View Plan**. You do **not** create model elements in this skill's happy path.

## Hard rules

1. **User governs scope** (VISION NG-3). Never silently lock architectural decisions.
2. **No MCP mutations** in this skill until the user explicitly confirms the View Plan. Do not call `create-element`, `create-relationship`, `create-view`, `clone-view`, `bulk-mutate`, `update-element`, `update-relationship`, `delete-element`, or other mutating tools here. Specialists (later) perform creates after confirmation.
3. **Do not copy ArchiMate metamodel tables** into chat or into the plan body. If you need reference material, **read** MCP resources (see below). Offline, say what you would read and continue with plain language.
4. **Consume-only** toward jgs-archi-mcp. Default endpoint: `http://127.0.0.1:18090/mcp` (see `docs/MCP.md`).

## Optional MCP resource reads (inventory-approved)

When the Archi Bridge MCP is connected, you may read:

- `archimate://recipes/index`
- `archimate://reference/archimate-view-patterns`
- `archimate://reference/archimate-layers`

Do not invent other resource URIs.

## Step 1 — Elicit intent (ORCH-01)

Collect plain-language answers for every field below. If the user already supplied some in the invocation args, do not re-ask those; fill gaps only.

| Field | Prompt cue |
|-------|------------|
| Problem | What problem or opportunity are we addressing? |
| Stakeholders | Who cares about the outcome? |
| Concerns | What worries or success criteria do they have? |
| Scope | What is in / out for this modelling pass? |
| Current state | What exists today (systems, processes, constraints)? |
| Target state | What should be true afterward? |
| Expected outcome | What deliverable does the user want from this run (views, decisions, migration path, …)? |

## Step 2 — Draft the View Plan (ORCH-02, ORCH-03)

Write a markdown View Plan with **exactly** these H2 headings (schema-checked):

```markdown
## Intent Summary
## Stakeholders and Concerns
## Proposed Viewpoints
## Layers Involved
## Modelling Sequence
## Dependencies
## Validation Points
## Open Questions for User
## Confirmation Gate
```

### Section guidance

- **Intent Summary** — 3–6 sentences restating problem, scope, outcome in the user's words.
- **Stakeholders and Concerns** — bullets pairing people/roles with concerns.
- **Proposed Viewpoints** — each bullet: viewpoint name; purpose in plain language; stakeholders served; abstraction level as overview / detail / mixed. Prefer standard ArchiMate viewpoint names when they fit; if inventing an organisation-specific viewpoint, say so and keep it compliant (no illegal element mixes). Trace each choice to stakeholder + concern + purpose.
- **Layers Involved** — plain language first (e.g. "business processes and the applications that support them"); optional ArchiMate layer name in parentheses.
- **Modelling Sequence** — numbered steps a modeller would follow; name future specialist responsibilities in plain words (motivation, business, application, …) without requiring the user to invoke them.
- **Dependencies** — what must be true before later steps (data, decisions, existing model content).
- **Validation Points** — how we will know the model is good enough (questions answered, checks to run).
- **Open Questions for User** — unresolved decisions; never hide them.
- **Confirmation Gate** — explicit text that **no model creates/updates run until the user approves** this plan (approve / revise / abort).

Keep the main plan free of element-type catalogs. If technical type hints help a later agent, put them only under optional:

```markdown
## Appendix: Technical Hints
```

## Step 2b — Ground viewpoints (VSEL-08..10 / OBJ-2)

After drafting **Proposed Viewpoints**, dispatch the orchestrator-only specialist **archi-viewpoint-select** (do not ask the user to invoke it):

1. Pass normalized intent axes (stakeholders, concerns, purpose, abstraction) and the draft viewpoint bullets.
2. Specialist returns a schema-valid **Viewpoint Trace Table** (plus org-specific proposals and rejected alternatives). No MCP mutations on this path.
3. Reconcile **Proposed Viewpoints** so names and abstraction levels **match the Trace Table** (VSEL-09). Prefer Trace Table order when conflicts arise.
4. Optionally attach the Trace Table under:

```markdown
## Appendix: Viewpoint Trace
```

5. If the specialist proposed organisation-specific viewpoints, surface them under **Open Questions for User** until the user accepts or revises them (NG-3).
6. Offline helper the specialist may run: `python helpers/viewpoint_selection_matrix.py`; validate traces with `python helpers/viewpoint_trace_schema.py`.

Then continue to schema check of the View Plan itself.

## Step 3 — Schema check

If the plan is written to a file, run:

```bash
python helpers/view_plan_schema.py path/to/view-plan.md
```

Fix missing headings until exit 0. For chat-only drafts, self-check the nine required H2 titles.

## Step 4 — Confirmation (ORCH-04)

Present the View Plan and stop. Ask the user to **approve**, **revise** (with notes), or **abort**.

- On **revise**: update the plan and re-check schema; do not mutate the Archi model.
- On **abort**: stop cleanly; summarize what was learned; no MCP mutations.
- On **approve**: state that modelling may proceed via specialist skills in a later step/phase; still do not mutate inside this skill unless a future version of this skill explicitly adds a post-confirm specialist dispatch section approved by the roadmap.



## Step 5 — Post-confirm specialist dispatch (SPEC-D-16, SPEC-D-17)

After the user **approves** the View Plan (Step 4), modelling may proceed via orchestrator-dispatched specialists. The orchestrator still does not need to mutate inside this skill; it **hands off** with a standard payload and a default order.

### Hand-off payload (required fields)

| Field | Content |
|-------|---------|
| confirmation_status | `approved` |
| intent_summary | From View Plan Intent Summary + elicit output |
| stakeholders_concerns | From View Plan |
| viewpoints | Names + abstraction levels (must match Trace Table) |
| layers_in_scope | From View Plan Layers Involved |
| modelling_sequence | Numbered steps from View Plan |
| reuse_constraints | Prefer existing IDs; naming notes |
| reuse_registry | Run-scoped map concept_key → element_id (OBJ-4); seed empty or from prior specialists |
| naming_policy | Policy id (default title-collapse-v1) + optional overrides |
| open_questions | Still unresolved items (user-visible) |
| target_views | Optional known view names |

### Default specialist order (decision rules)

Skip specialists whose layer/concern is out of confirmed scope.

1. archi-elicit — only if intent fields still incomplete
2. archi-viewpoint-select — already done in Step 2b; re-run only if viewpoints change after approval notes
3. archi-motivation — if motivation/strategy drivers in scope
4. archi-capability-strategy — if capability/strategy in scope
5. archi-business — if business layer in scope
6. archi-application — if application layer in scope
7. archi-technology-physical — if technology/physical in scope
8. archi-implementation-migration — if roadmap/migration in scope
9. archi-traceability — after at least two layer specialists (or when cross-layer traces requested)
10. archi-model-qa — after structural creates; before final layout freeze preferred
11. archi-layout — after content stable on target views
12. archi-documentation — last: rationale + completion summary

Parallelism: independent layer specialists may run in parallel when the modelling sequence has no dependency; traceability waits on their IDs.

### Shared contract

Every mutating specialist must follow `docs/CREATE_PATH.md` including the OBJ-4 coherence section (reuse registry, naming policy, no silent ambiguous merge). Offline assists: `helpers/reuse_inspect.py`, `helpers/naming_convention.py`. Inventory tools only. No ArchiMate table dumps (NG-4). User remains governor (NG-3).

### Completion

End the run when documentation specialist returns a completion summary, or earlier if the user aborts. Capture offline evidence under `docs/evidence/` when live MCP is unavailable.

## Completion summary (when stopping)

Always end with:

1. Path or paste of the View Plan
2. Confirmation status (pending / approved / aborted)
3. Next recommended action (revise plan, approve, or hand off to specialists when available)
