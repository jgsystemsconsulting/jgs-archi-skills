# View Rationale: End-to-End Traceability

## Purpose
Let a reader follow one uninterrupted chain from a motivation element to the technology that supports it, specifically for the single-source-of-truth carrier data goal.

## Stakeholders and Concerns
COO and CFO need to see that money spent on the integration gateway traces to a goal; IT Manager needs the deployment chain visible.

## Viewpoint
Layered viewpoint (standard, mixed abstraction): motivation column, strategy column, business column, application column, technology column, left to right.

## Questions Answered
Which technology element realizes the carrier-data goal, through which capability, process, and service?

## Assumptions
A single representative chain suffices; the full model contains parallel chains for the other goals.

## Decisions
Chain: driver influences goal, requirement realizes goal, capability realizes requirement, business process realizes capability, application service serves the process, hub component realizes the service, artifact realizes the component, node assigned to the artifact.

## Exclusions
Alternative chains (quoting, tracking) stay in their layer views; this view carries only the carrier-data chain.

## Open Questions
None; chain verified complete (9 elements, 8 connections).
