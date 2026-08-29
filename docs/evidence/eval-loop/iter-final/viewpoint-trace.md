<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Viewpoint Trace: Meridian Freight eval run (iter-0)

## Viewpoint Trace Table

| Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Standard? | Justification |
|---|---|---|---|---|---|---|
| Motivation (matrix key: motivation) | Chief Operating Officer; Head of Customer Service; CFO; IT Manager; Customer | Why change: visibility, margin, data growth | Design and design rationale: show drivers, assessments, goals, outcomes, requirements in one picture | overview | yes | Motivation elements only; answers "why are we doing this" |
| Capability Map (matrix key: capability-map) | COO; IT Manager | Which abilities need strengthening | Design: capabilities and supporting resources for Meridian's operations | overview | yes | Strategy-layer viewpoint; capability/resource only |
| Business Process (matrix key: business-process) | Head of Customer Service; Customer | Slow quotes, manual re-keying | Design: customer service processes, actors, services, and business data | detail | yes | Business behaviour viewpoint over the frozen process list |
| Application Cooperation (matrix key: application-cooperation) | IT Manager; Head of Customer Service | Integration debt between TMS, CRM, portal | Design: applications, their services, functions, and data, supporting the business process | detail | yes | Ranked 3 by matrix; matches cross-application support concern |
| Technology (matrix key: technology) | IT Manager | Hosting and integration platform risk | Design: nodes, software, artifacts, technology service supporting applications | detail | yes | Technology-layer structure and behaviour for the frozen platform |
| Layered (matrix key: layered) | COO; CFO | Traceability from goals to technology | Design and design rationale: end-to-end motivation-to-technology chains | mixed | yes | Layered viewpoint composes the layers above for traceability |

## Organisation-Specific Proposals

None. All six views map to standard ArchiMate viewpoints; no organisation-specific
viewpoint is proposed in this run.

## Rejected Alternatives

| Alternative | Reason rejected |
|---|---|
| Implementation and Migration (matrix key: implementation-migration) | Scenario scope explicitly excludes migration planning |
| Physical (matrix key: physical) | Scenario scope excludes physical distribution of goods |
| Business Product (matrix key: business-product) | No products are modeled in the frozen scenario |
| Value Stream viewpoint | No value stream in the frozen scenario content |
