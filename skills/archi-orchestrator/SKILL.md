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

## Completion summary (when stopping)

Always end with:

1. Path or paste of the View Plan
2. Confirmation status (pending / approved / aborted)
3. Next recommended action (revise plan, approve, or hand off to specialists when available)
