<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# View Rationale: Application Support

## Purpose
Show which applications support the business processes, which services and functions realize that support, and which data objects the functions use.

## Stakeholders and Concerns
IT Manager owns integration debt: the hub co-realizing tracking and owning carrier data is the answer to spreadsheet divergence.

## Viewpoint
Application Co-operation viewpoint (standard): components, services, functions, data objects, with serving into the business layer.

## Questions Answered
Which application supports which process, and where does the single carrier dataset live?

## Assumptions
CarrierDesk TMS stays the quoting engine; FreightHub Integration Hub becomes the carrier data owner.

## Decisions
Access relations only from behaviour elements (functions), never from components, per the reference rule; Status Aggregation realizes Performance Analytics so analytics has an application home.

## Exclusions
UI composition and detailed data modeling are excluded by scenario scope.

## Open Questions
Whether SalesCloud CRM should expose a service to Handle Customer Inquiry directly (currently the component serves the process) awaits the user.
