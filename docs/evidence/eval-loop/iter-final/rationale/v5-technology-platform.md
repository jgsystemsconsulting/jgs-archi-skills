# View Rationale: Technology Platform

## Purpose
Show where the applications run and which technology carries the carrier data feeds.

## Stakeholders and Concerns
IT Manager is accountable for hosting and secure transport of carrier data.

## Viewpoint
Technology viewpoint (standard): nodes, system software, artifacts, one technology service.

## Questions Answered
Which node hosts which application, and how do carrier feeds reach the hub securely?

## Assumptions
One application server suffices for TMS and portal at current volumes.

## Decisions
Node-assignment carries both artifacts (deployment) and system software (middleware), matching the reference rule that nodes are assigned to artifacts and software; the hub artifact realizes the hub component to close deployment to application.

## Exclusions
Networks, devices, and physical material flows are excluded by scenario scope.

## Open Questions
Disaster-recovery topology is unmodelled; not in scenario.
