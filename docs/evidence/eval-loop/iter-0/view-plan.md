<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# View Plan: Meridian Freight customer-service uplift

## Intent Summary

Meridian Freight, a regional freight brokerage, wants a model of its current
customer-service and shipment operations to ground an uplift programme:
faster quotes, integrated carrier data, and self-service tracking. The run
models motivation (why change), strategy (which capabilities), business
(how work runs), application (what supports it), and technology (what hosts
it), plus one end-to-end traceability view. Input and standing approval:
docs/eval/reference-scenario.md (FROZEN v1.0).

## Stakeholders and Concerns

- Chief Operating Officer: margin pressure, cost per shipment, operational visibility
- Head of Customer Service: slow quotes, manual re-keying, service consistency
- Chief Financial Officer: cost per shipment, measurable outcomes
- IT Manager: integration debt, hosting platform, data growth
- Customer: shipment status transparency, self-service tracking

## Proposed Viewpoints

- Motivation (overview): why the change is needed; serves all stakeholders; overview
- Capability Map (overview): capabilities to strengthen and supporting resources; serves COO, IT Manager; overview
- Business Process (detail): customer service processes and services; serves Head of Customer Service, Customer; detail
- Application Cooperation (detail): applications supporting the process; serves IT Manager; detail
- Technology (detail): platform hosting and integrating the applications; serves IT Manager; detail
- Layered (mixed): end-to-end traceability from goals to technology; serves COO, CFO; mixed

Names and abstraction levels match docs/evidence/eval-loop/iter-0/viewpoint-trace.md.

## Layers Involved

- Motivation: drivers, assessments, goals, outcomes, requirements, stakeholders
- Strategy: capabilities and resources
- Business: actors, processes, services, business objects
- Application: components, services, functions, data objects
- Technology: nodes, system software, artifacts, technology service

## Modelling Sequence

1. Motivation specialist creates stakeholders, drivers, assessments, goals, outcomes, requirements and their influence/association/realization links.
2. Capability-strategy specialist creates capabilities and resources, links resources to capabilities and capabilities to requirements.
3. Business specialist creates actors, processes, services, business objects; assignment, triggering, access, and realization links.
4. Application specialist creates components, services, functions, data objects; realization, access, and serving links into the business layer.
5. Technology-physical specialist creates nodes, system software, artifacts, technology service; assignment, realization, and serving links into the application layer.
6. Traceability specialist builds the End-to-End Traceability view from existing elements across layers.
7. Model QA runs compliance and reuse checks over the whole model.
8. Layout specialist places and routes all six views.
9. Documentation specialist finalizes rationale and completion summary.

## Dependencies

- Viewpoint trace completed before element creation (done, see Appendix).
- Layer specialists run in order; traceability needs their element IDs.
- All names follow the frozen scenario lists and title-collapse-v1 naming policy.

## Validation Points

- compliance_validate reports no violations on the final slice
- naming conflicts check reports zero conflicts
- rationale schema validates the per-view rationale bundle
- documentation coverage: every element and relationship documented
- layout check: no overlaps, consistent direction, layer grouping

## Open Questions for User

None for this run: the frozen scenario pre-answers scope, naming, and views.
Any structural ambiguity (relationship typing) is resolved against MCP
reference resources, never invented.

## Confirmation Gate

The frozen scenario doubles as standing approval: running the eval loop
against it authorises model creation in the dedicated eval model
(JGS Eval Loop) only. No other model may be touched.

## Appendix: Viewpoint Trace

See viewpoint-trace.md in this directory (schema-validated).
