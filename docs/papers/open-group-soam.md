<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Skill-Orchestrated ArchiMate Modelling: Keeping the Architect in the Loop

**A practitioner note for ArchiMate and Archi users**

JG Systems Consulting Ltd  
Working draft. Not an Open Group publication. Same method as the IEEE Software practice write-up; this cut is for architecture practitioners, not a research track.

## The job

Architecture views in an engineering organisation are supposed to be the system of record for change. They lag delivery by sprints. The Open Group already defined ArchiMate viewpoints. ISO/IEC/IEEE 42010 already said stakeholders get viewpoints. Archi already holds a real model. The bottleneck is the method: it lives in the modeller's head, and the tool is a canvas.

The loop is familiar. Workshop. Tacit viewpoint. Days of boxes. Review finds the wrong cut. Rationale sits in a slide deck the next programme will not open. Cross-layer traces (capability to process to application to node to work package) are the first labour dropped under deadline.

Language-model tools do not fix this if they emit a picture or a PlantUML file beside Archi. The organisation's model is unchanged. The architect is asked to bless a drawing after the fact.

## The method (SOAM)

Skill-Orchestrated ArchiMate Modelling is a governed pipeline on top of Archi.

1. Plain-language intent in.
2. Orchestrator elicits stakeholders, concerns, scope, and a view plan.
3. The architect approves or rejects. Nothing mutates until yes.
4. Only the named layer specialists run (motivation, capability, business, application, technology/physical, implementation/migration as required).
5. Traceability, model QA, layout, and documentation run as stages, not as leftover work.
6. Writes go through the JGS Archi Bridge (MCP) into the open Archi model. ArchiMate language tables stay in MCP resources. Skills do not copy the metamodel.

The user invokes the orchestrator only. Layer specialists are not a buffet. A capability cut does not silently grow a technology view. A landing-zone move that says "do not redesign the business" does not invent processes to justify the diagram. A refused layer is method behaviour, not a failed generation.

First generation is a draft. Completing a specialist does not mean the architecture is finished.

## Two author-run walks (not client case studies)

These are not timed engagements. They show coverage. Both were executed by the authors in Archi. Working models and paste fences: [jgs-archi-skills-we](https://github.com/jgsystemsconsulting/jgs-archi-skills-we). Author-run frozen firms, not client models. These are the IEEE paper walks.

**Hatherley Plate (mill CRM).** MES and ERP run the mill. Sales track orders in spreadsheets. A CRM programme is funded to fix visibility. Plant engineers fear the drawing will treat the CRM as the MES. Views: Motivation Overview, Capability Map, Production Operations, Application Support, Technology and Physical. Constraint: OrderSight and MillOS stay separate applications; mill equipment assigned to a node; no work-package roadmap. Five views are on the companion mill walk (`hatherley.html`).

**Moorfield Range.** Hawker Range Systems Ltd runs one UK training range. Instructors still track sorties on SortieBoard. RangePlan is funded for sortie visibility. Constraint: RangePlan, GroundOS, and AirStack stay separate; SysML stays off the ArchiMate canvas; the air vehicle is not product structure; no work-package roadmap. Same method cut as the mill: motivation and technology/physical in, implementation and migration out. Model and pastes live in the same we-repo. This is the refuse-scope walk: dispatch does not invent SysML, a plateau, or a merged blob.

Starter prompts for a capability-cut (invoice-to-cash) and a landing-zone refuse exist in the skill pack. They are unexecuted install first-contact briefs, not IEEE evidence.

## What we are not claiming

No speedup percentage. No replacement of the enterprise architect. No "the industry has adopted this." ArchiMate is not incomplete. Architects are not slow. Given ArchiMate and Archi, the dominant practice does not instrument the method.

MIT skills, Archi already in the shop, no second EA suite. That is a design choice so a team can try the method. It is not evidence of uptake.

## Try it

Archi 5.7+, JGS Archi Bridge plugin, skill pack:

- https://github.com/jgsystemsconsulting/jgs-archi-mcp
- https://github.com/jgsystemsconsulting/jgs-archi-skills

```text
/archi-orchestrator invoice-to-cash capability map for finance and ops
```

Stop at the view plan. If you would not sign it, reject it. Nothing has been written yet. That starter is install first-contact, not a paper walk.

## Further reading

Practice write-up (IEEE two-column PDF): `docs/papers/ieee/soam-ieee-software.pdf` in the skills repository.

ISO/IEC/IEEE 42010:2022. ArchiMate 3.2 Specification (The Open Group). Archi (Beauvoir and Sarrodie). Model Context Protocol specification.
