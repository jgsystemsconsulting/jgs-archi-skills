<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# The bottleneck was never ArchiMate

An adoption brief for SOAM, Skill-Orchestrated ArchiMate Modelling, in Archi. What it is, what changed to make it possible, what it brings over manual modelling, and what it does not claim.

> If you are an enterprise architect, read sections 3 to 5. If you are an engineering manager, read 4 and 6. If you are an open-source or tooling person, read 2 and 7.

## The problem you already have {#problem}

Delivery ships weekly. Architecture views lag by sprints. That lag is not a shortage of the ArchiMate language, and it is not a shortage of Archi. The method lives in the architect's head. The tool is a canvas.

The loop is familiar on most programmes. Stakeholder workshop. Tacit viewpoint choice. Days of placing boxes. A review that finds the wrong cut. A slide deck that holds the rationale the model never did. Cross-layer traces (capability through process to application to node to work package) are the first labour dropped under deadline. Juniors invent illegal relations; seniors lint after the fact. The next programme opens the slides, not the model.

ArchiMate already names stakeholders, viewpoints, and layers. Archi already holds a real model. The dominant practice does not instrument the method inside that model, so architecture work cannot keep cadence with engineering. Throughput is why an engineering organisation should care. Throughput here is a reason, not a measured result.

## What changed {#changed}

Language-model tools have been tried on modelling for years. The dominant failure mode is stable and documented. The model stays unchanged. The metamodel is copied or approximated in a prompt. The agent emits a picture beside the system of record: PlantUML, JSON, a screenshot, a Draw.io file. The architect is asked to bless a drawing after the fact. Cámara et al. (2023) reported mixed reliability on UML tasks outside a controlled prompt. Fill, Fettke, and Köpke (2023) reported conceptual-modelling experiments in which models emit plausible diagrams that are not the organisation's model. That line of work generates a parallel artefact.

Two surfaces undercut that failure mode. Model Context Protocol (MCP) made a live tool surface agent-operable. Agentic coding hosts (ZCode, Claude Code, Cursor, and peers) can call tools in a session rather than only emit text. An agent can now write into the system of record instead of pasting a picture next to it.

What matters is governance, not generation. An agent that can mutate Archi without a gate is more dangerous than one that draws PlantUML. Skill-Orchestrated ArchiMate Modelling (SOAM) is the method on that surface: plain-language intent in, a view plan the architect signs, specialists dispatched only for named layers, writes only through the JGS Archi Bridge MCP into Archi. The language stays in MCP resources. Skills orchestrate; they do not carry a stale copy of ArchiMate tables.

## One run, end to end {#run}

Take a mid-size manufacturer. Quotes go out by email. Orders land in the ERP. Collections are chased from a spreadsheet. Finance cannot see cash in flight. Operations cannot see which capabilities actually run quote, order, invoice, and collect. Stakeholders on the brief: CFO, head of operations, IT manager, credit controller. In scope: capabilities, order-to-cash processes, supporting applications. Out of scope: shop floor, physical distribution, payroll, ERP replacement. Target: one capability map finance and operations agree on, with as-is processes and the applications that realize them.

You type a plain-language job into the host that has the skill pack installed:

```text
/archi-orchestrator invoice-to-cash capability map for finance and ops
```

The orchestrator runs elicitation and viewpoint selection. It drafts a view plan. The plan names views, stakeholders, concerns, and which layer specialists will run. On this brief the views are Capability Map, Order-to-Cash Operations, and Application Support. Specialists named on the plan: elicit, viewpoint-select, capability-strategy, business, application, then traceability, model-qa, layout, and documentation. Technology and physical are not on the plan. The method must not invent a mill.

Stop here. Read the plan the way you would read a statement of work. If you would not sign it, reject it. Nothing has been written. Rejection returns to intent with no half-written model. A rejection is a successful first run: the gate worked, the canvas is clean, and you still own the cut.

If you approve, only the named specialists run. They write elements, relations, views, and documentation fields through the bridge into Archi. Traceability must leave at least one path from a capability through a process to an application. Documentation fields carry an evidence line (stated, inferred, or existing), not a restatement of the element name. The first generation ends at a draft checkpoint. Completing a specialist does not mean the architecture is finished. The ERP is already there; the run maps what it covers versus spreadsheet work. It does not propose a replacement programme.

Invoice-to-cash is install first-contact only: stop at the gate. The IEEE paper walks are two author-run models in the we-repo (Hatherley Plate mill CRM that must not swallow the MES, and Moorfield Range where RangePlan must not swallow GroundOS or AirStack). A TMS landing-zone refuse remains an unexecuted starter prompt. Same gate on every brief. A refused layer is method behaviour.

## What it brings over manual modelling {#manual}

Manual Archi practice loses cycle time in recurring ways. Table 1 names each waste, what it costs, and the SOAM stage built to hit it. The rows are unchanged from the IEEE Software practice write-up.

| Waste | What it costs | SOAM stage |
|---|---|---|
| Viewpoint chosen from habit | Wrong audience, kitchen-sink diagrams, rework | Viewpoint select and view-plan approval |
| Elicitation decoupled from modelling | Notes go stale; review finds the wrong scope | Elicit, then plan; no mutate yet |
| Drawing as the main effort | Allowed relations live in the modeller's head | Layer specialists via MCP |
| Cross-layer traces optional | Motivation to mill equipment breaks first | Traceability |
| Docs as a second artefact | Rationale in slides; model becomes pictures | Documentation fields in the model |
| Language not executable | Juniors invent illegal relations; seniors lint | MCP resources and model QA |

Waste classes are only half the comparison. Entry cost, reversibility, and exit cost decide whether a shop will try the method at all.

| Criterion | Manual practice | SOAM run |
|---|---|---|
| Cost of entry | New licence, new tool adoption cycle, training | Archi already installed, paste-install prompt, MIT, Python 3.10+ standard library only |
| Reversibility | Rework discovered at review, after days of boxes | Nothing mutates before the view plan is approved; first generation ends at a draft checkpoint |
| Exit cost | Model tied to the suite that drew it | Delete the skills folder; the model stays a valid, open ArchiMate model in Archi |

These tables are qualitative. There is no stopwatch on this page. SOAM compresses elicit, plan, model, QA, and document into one governed run; that claim is reasoned from the waste table, not timed against a bake-off. Per the honesty bar in the method papers, treat design-for-adoption as a design choice, not as evidence of uptake.

## What is new versus the AI tools you have seen {#new}

Four claims separate SOAM from "describe your enterprise and let AI draw it." Each claim names where you verify it.

1. Writes into the real model through the bridge MCP, with no parallel artefact. Verify in section 2 above and in the bridge repository `jgs-archi-mcp`.
2. The ArchiMate language is never copied into prompts. MCP resources are the sole source of truth, and a structural validator reports fourteen skill files with zero unknown tool references on v1.0.0. Verify in the repository README section "Structural validation"; command `python helpers/validate_skill_mcp_refs.py`.
3. Governance is the method. Specialists are dispatched, not user-invoked, and a refused layer is success. Verify in the repository README usage section and in `SKILLS.md`.
4. Traceability, model QA, layout, and documentation run as pipeline stages: the labour that dies first under deadline. Verify in `docs/CREATE_PATH.md`, the shared specialist contract.

A prompt that says "draw ArchiMate" has none of these rules. MCP is the tool protocol those agents can speak. It is not a modelling method by itself. SOAM is the method on that protocol.

## Status {#status}

| Works now | Evidence pending | Community dependent |
|---|---|---|
| v1.0.0 pack, 14 skills, offline test suite, structural validation of MCP references, seven install targets, opt-in live MCP smoke. Evidence: two public author-run frozen-brief models with replayable pastes in [jgs-archi-skills-we](https://github.com/jgsystemsconsulting/jgs-archi-skills-we) | Timing study against hand modelling on the same brief; second-architect repeat runs for stable element names; one anonymised client run; QA defect-class comparison against a senior architect | Issue flow on the pack, community worked-run reports on Discussions, recipe and convention contributions |

Unknown stays unknown. The walks so far are frozen briefs by the method authors, not client engagements. They show method coverage. They do not show organisational uptake. Language-model output is non-deterministic; the same intent can yield different element names. Governance (approval gate, QA, no-invention rule) is the control, not model temperature. The implementation is one bridge, one skill suite, Archi only. The argument does not generalise to Sparx or LeanIX. Throughput is unmeasured. Those future measurements match the list in the IEEE practice write-up. They are not results on this page.

## Why open source makes it safer, not just cheaper {#opensource}

The pack is MIT. You can fork it, pin it, or vendor the skills folder. Bug-report and skill-improvement issue forms sit on the tracker so defects arrive structured. In-session upstream feedback drafting (`/jgs-upstream-feedback`) turns a pack defect found mid-run into a draft the maintainer can act on; local model issues stay local. GitHub Discussions hold worked runs and questions that are not bugs. `CITATION.cff` gives academic credit a stable target.

Skills are reviewable markdown. Many-eyes applies to method text, not only to code. A house that needs different naming, folder layout, or evidence rules can fork and encode those rules in `docs/MODELLING_CONVENTIONS.md` without waiting on a vendor roadmap. The loop is simple: one user's run surfaces a defect, the fix lands in the next release, every user's next run gets it.

Open source is a safety property for a method that mutates the system of record. You can read the gate, the specialist contract, and the MCP allow-list before you approve a plan. You can delete the skills and keep the model.

## Try it in one afternoon {#try}

Prerequisites:

- Archi 5.7 or later
- JGS Archi Bridge plugin, MCP at `http://127.0.0.1:18090/mcp` by default
- Python 3.10 or later, standard library only (no extra modelling engine)

Point your agent host at the paste-install prompt in the repository README: [https://github.com/jgsystemsconsulting/jgs-archi-skills](https://github.com/jgsystemsconsulting/jgs-archi-skills). The prompt installs the bridge and the skill pack; read each README and follow it. Do not invent steps.

First contact after install:

```text
/archi-orchestrator invoice-to-cash capability map for finance and ops
```

Stop at the view plan. If you would not sign it, reject it. Nothing was written. That is the whole first afternoon: wire the bridge, install the skills, reach the gate, exercise a rejection. Generation after approval is a second session, on a brief you own.

## What we do not claim {#claims}

No speedup percentage. No replacement for the enterprise architect. No industry-adoption claim. ArchiMate is not incomplete, and architects are not slow. Given ArchiMate and Archi, the dominant practice does not instrument the method. Cadence of architecture work is the reason an engineering organisation should care; measure it later.

The method write-up that backs these boundaries is the IEEE Software practice cut [`ieee/soam-ieee-software.pdf`](ieee/soam-ieee-software.pdf) (markdown working copy [`soam-ieee-software.md`](soam-ieee-software.md)). The longer preprint is [`ieee/soam-ieee-long.pdf`](ieee/soam-ieee-long.pdf). Both name the same refusals this brief inherits: parallel-artefact generation is not the method, MCP is not a modelling method by itself, the IEEE walks are two author-run frozen briefs (mill and range), throughput is unmeasured, and design-for-adoption is not evidence of uptake. Invoice-to-cash on this page is first-contact install practice, not an IEEE walk.

Canonical web page for this brief: [https://jgsystemsconsulting.github.io/jgs-archi-skills/why-soam.html](https://jgsystemsconsulting.github.io/jgs-archi-skills/why-soam.html).

Sign the view plan. Archi stays the system of record.
