---
name: archi-orchestrator
description: "Elicit architectural intent and produce a plain-language ArchiMate view plan via JGS Archi Bridge MCP (user-governed). Trigger: /archi-orchestrator"
argument-hint: "[optional free-text intent]"
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# archi-orchestrator

## When to use

User-invoked entrypoint for agent-guided ArchiMate work in Archi. Call this when you have architectural intent and need a View Plan before any model mutations.

Starter invoke lines and frozen briefs: `docs/prompts/README.md`.

## Prerequisites

Archi with the JGS Archi Bridge MCP (see docs/MCP.md). Python 3.10+ for helpers. Follow docs/CREATE_PATH.md. Specialists require View Plan confirmation `approved` before mutations.

User-invoked entrypoint for agent-guided architecture work in Archi. You elicit intent, optionally ground on MCP **resources** (read-only), and produce a **plain-language View Plan**. You do **not** create model elements in this skill's happy path.

## Hard rules

1. **User governs scope.** Never silently lock architectural decisions.
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
- **Validation Points** — how we will know the model is good enough (questions answered, checks to run), including house-style checks (names, descriptions, folders) per docs/MODELLING_CONVENTIONS.md.
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

Every mutating specialist must follow `docs/CREATE_PATH.md` including the OBJ-4 coherence section (reuse registry, naming policy, no silent ambiguous merge), the OBJ-5 compliance section (explain-and-propose; never silent-apply), and the OBJ-6 rationale / NL-change / completion-summary section. House style: `docs/MODELLING_CONVENTIONS.md` with offline assists `helpers/docs_coverage.py`, `helpers/naming_convention.py` (including aspect-hints), `helpers/folder_convention.py`. Other offline assists: `helpers/reuse_inspect.py`, `helpers/compliance_validate.py`, `helpers/rationale_schema.py`, `helpers/nl_change_impact.py`, `helpers/completion_summary_schema.py`. Inventory tools only. No ArchiMate table dumps (NG-4). User remains governor (NG-3).

### Compliance findings (OBJ-5)

After the model-qa specialist (or a specialist self-check), consume compliance findings in the run summary:

- Carry forward finding count and any **needs-user** items (illegal types/edges, abstraction or naming conflicts).
- Do not invent mutating tools to auto-fix; surface alternatives and wait for user/orchestrator choice.
- Optional hand-off field: `compliance_findings` (list of `{check_id, object_refs, problem, proposed_alternative}`).

### Documentation and NL-change loop (OBJ-6)

After modelling content is stable (typically after layout), dispatch the documentation specialist (archi-documentation) last:

- Consume its **completion summary** (Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run, Deliberately Deferred, Improve Next) and schema validation status.
- If the user requests natural-language changes: run the documentation NL path (impact plan via `nl_change_impact` → user confirm → regenerate with must-reuse IDs → rationale deltas). Do not invent new mutating tools; reuse layer/layout specialists for regenerate scope only.
- Optional hand-off fields: `completion_summary`, `rationale_validation`, `nl_change_impact`.

### Completion

End the first generation at a **draft checkpoint** (CP-G7). After the documentation specialist returns a valid completion summary, stop and ask the user to confirm, deepen (pick from Improve Next / Deliberately Deferred), or stop. Do not present the model as finished.

Decide-and-log by default. Ask only when the choice is costly to reverse, evidence is missing, and a wrong guess wastes significant work. More than about five open questions means under-deciding; log the reversible ones and continue.

When live MCP is unavailable, say so and continue offline with the View Plan only.

## Completion summary (when stopping)

Always end with:

1. Path or paste of the View Plan
2. Confirmation status (pending / approved / aborted)
3. Compliance/QA outcome (pass, findings pending user, or blocked) when model-qa ran
4. Documentation outcome: completion summary (or path), including Deliberately Deferred and Improve Next, rationale validation status, NL-change impact if any
5. Next recommended action (revise plan, approve, resolve compliance findings, NL-change regenerate, or stop)

## Upstream feedback (pack defects only)

After a blocked step, or after the draft checkpoint, consider a pack or MCP-contract hole. Clean runs stay quiet. Specialists may flag a skill-gap or mcp-gap up to you. They never file.

### Origin vs local

Offer GitHub only if any user would hit this, and the fix belongs in shipped skill text, a helper, or the MCP contract. Say nothing about GitHub for their model, org, install, governance no, or ops (bridge down, wrong model). If you cannot state the gap without their nouns, stay silent.

### Classify

- skill-gap or bug: issues_repo jgsystemsconsulting/jgs-archi-skills
- mcp-gap: issues_repo jgsystemsconsulting/jgs-archi-mcp
- Ambiguous: skills repo, label needs-triage, one sentence on why it might be the bridge

Cap: one suggestion per distinct agnostic gap. Max two per session unless they invoked jgs-upstream-feedback. After no, do not ask again for that gap.

### Suggest then dispatch

One or two lines: what failed, that this is about the pack not the model. Show the redacted title and body (skill-meta only). Ask:

Raise this against <issues_repo>?

On yes, dispatch jgs-upstream-feedback with kind, issues_repo, title, body (the skill-meta template, filled), labels (skill-improvement for skill-gap, bug for bug, omit or needs-triage when ambiguous), allow_pr false, already_approved true. Do not offer a PR here. The filer must not ask again.

On edit: revise the draft, show it again, dispatch only on a later yes (already_approved true only after that yes).

On no, continue or stop.

Late door: user may invoke jgs-upstream-feedback themselves.
