<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# View Rationale: Customer Service Operations

## Purpose
Show how customer service work actually flows: who performs which process, how processes trigger each other, which services the business provides, and which business data is touched.

## Stakeholders and Concerns
Head of Customer Service needs the process chain to standardize; Customers experience the quoting and tracking services.

## Viewpoint
Business Process Co-operation viewpoint (standard): actors, processes, services, business objects.

## Questions Answered
Who does the work, in what order, producing which services, and reading or writing which records?

## Assumptions
Quote acceptance always leads to shipment planning; tracking starts after planning books the shipment.

## Decisions
Access relations carry accessType (write for quote creating the order, readwrite for planning and onboarding) to make data ownership explicit; processes realize capabilities so the business layer closes the strategy loop.

## Exclusions
Business roles, events, and functions are not in the frozen scenario element lists.

## Open Questions
Whether Quote Shipment should be a BusinessEvent-driven subprocess is out of scope for this pass.
