<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Sign the view plan. Archi stays the system of record.

Delivery ships weekly. Architecture views lag by sprints. The lag is not a shortage of ArchiMate. The method lives in the architect's head and the tool is a canvas.

SOAM (Skill-Orchestrated ArchiMate Modelling) is a governed run inside Archi. You type the job in plain language. The orchestrator drafts a view plan. You approve or reject. Nothing is written until yes. Specialists then fill only the layers you named. Traceability, QA, layout, and documentation sit on the critical path. Language stays in the MCP bridge resources, not in the prompt.

You still own the architecture. The agent does not invoke layer skills. A refused redesign is success, not a failed generation.

## Two author-run walks

Both walks were executed by the authors in Archi. Working models and paste fences: [jgs-archi-skills-we](https://github.com/jgsystemsconsulting/jgs-archi-skills-we). Author-run frozen firms, not client models. These are the IEEE paper walks.

```text
/archi-orchestrator manufacturing plant: as-is shop floor and the CRM programme that is supposed to fix order visibility
```

CRM is funded to fix visibility. Plant engineers fear the drawing will swallow the MES. Constraint: CRM and MES stay separate. Mill equipment stays on a node. Five views: [hatherley.html](../../hatherley.html).

```text
/archi-orchestrator training range: as-is range operations and the planning tool that is supposed to fix sortie visibility
```

RangePlan is funded for sortie visibility. Constraint: RangePlan, GroundOS, and AirStack stay separate. SysML stays off the ArchiMate canvas. The air vehicle is not product structure. Model and pastes live in the same we-repo.

## Starter prompts (not paper walks)

Copy after install. Specialists stay orchestrator-dispatched. These are unexecuted briefs for first contact, not IEEE evidence.

```text
/archi-orchestrator invoice-to-cash capability map for finance and ops
```

Finance and ops cannot see which capabilities run quote, order, invoice, collect. Capability map, operations, application support. No mill. No ERP replacement. Stop at the view plan on first contact.

```text
/archi-orchestrator move the legacy TMS to a cloud landing zone; plateaus and work packages only. Do not redesign the business.
```

Infrastructure wants a landing zone. Operating model stays. Success is plateaus and work packages, not a new business layer. No author-run Archi model yet.

## Install

Needs Archi 5.7+, the [JGS Archi Bridge](https://github.com/jgsystemsconsulting/jgs-archi-mcp) plugin, Python 3.10+ (stdlib only). Paste this into ZCode, Claude Code, or Cursor:

```text
Install and set up JGS Archi Bridge (MCP) and jgs-archi-skills. Read each README and follow it. Do not invent steps.

Repositories:
1. JGS Archi Bridge (Archi MCP plugin): https://github.com/jgsystemsconsulting/jgs-archi-mcp
2. jgs-archi-skills (agent skill pack): https://github.com/jgsystemsconsulting/jgs-archi-skills
```

The full prompt is in the [repository README](https://github.com/jgsystemsconsulting/jgs-archi-skills). MIT. Archi is the only canvas.

## What this is not

Not "describe your enterprise and let AI draw it." Not a second diagram in PlantUML or Draw.io. Not a replacement for the architect.

## Paper that backs the claim

Practice write-up (IEEE Software shape, 4 pages): [ieee/soam-ieee-software.pdf](ieee/soam-ieee-software.pdf)

Longer preprint: [ieee/soam-ieee-long.pdf](ieee/soam-ieee-long.pdf)

Open Group–shaped note: [open-group-soam.md](open-group-soam.md)

No speedup percentage. No "industry has adopted this." The claim is method: gated run, Archi as system of record, language not copied into the agent.
