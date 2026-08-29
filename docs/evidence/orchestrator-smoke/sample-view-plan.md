<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Sample View Plan (offline smoke)

Synthetic example for schema + skill dry-run. Not produced against a live Archi model.

## Intent Summary

Finance wants a clear picture of how invoice approval works today and what a future shared service should look like. Scope is business process plus supporting applications for invoice intake through payment release. Outcome: a view plan the team can approve before any model edits.

## Stakeholders and Concerns

- AP Manager: cycle time and exception handling
- CFO office: control and auditability
- IT application owner: integration load on ERP

## Proposed Viewpoints

- Business Process Cooperation: show the invoice flow end to end for AP Manager (overview)
- Application Cooperation: show systems supporting each step for IT (overview)
- Motivation (light): goals and requirements driving the change for CFO (overview)

## Layers Involved

- Business processes and roles (Business)
- Applications and interfaces that support them (Application)
- Light motivation drivers/goals (Motivation)

## Modelling Sequence

1. Confirm stakeholders and scope (this plan)
2. Motivation specialist stubs goals/requirements if approved
3. Business process view of as-is invoice path
4. Application collaboration for systems on that path
5. Validation against open questions

## Dependencies

- Access to current process description (or workshop notes)
- Agreement that payment release is in scope
- Archi model available before any create tools run (post-confirm)

## Validation Points

- Every stakeholder concern maps to at least one viewpoint
- Sequence lists business before deep application detail
- No model mutations claimed before Confirmation Gate approval

## Open Questions for User

- Is external supplier portal in or out of scope?
- Do we model only as-is, or as-is plus target plateau?

## Confirmation Gate

No Archi model creates or updates run until the user explicitly approves this View Plan (approve / revise / abort).
