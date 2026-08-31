<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P04 Natural-language change: second CRM

## Priority
P0

## Invoke
/archi-orchestrator on the current model, add a second CRM for the European branch and show impact; do not duplicate shared customer data

## Problem
The open Archi model already has a CRM. The European branch will run a second CRM. The user wants the change in plain language, with impact visible, and without a second copy of the shared customer record.

## Stakeholders
- European branch manager
- IT Manager
- Data owner for customer records
- Original CRM product owner

## Concerns
- Duplicate customer data
- Which applications the new CRM serves
- Blast radius on existing views
- Reuse of elements already in the model

## Scope
In: delta to the existing application landscape and traces; update Application Support and End-to-End Traceability; document impact.
Out: greenfield rebuild, new motivation stack, technology refresh, and migration plateaus.

## Current state
One CRM, one customer record concept, existing views already in the model. This card assumes that model is the active Archi model.

## Target state
Two CRM applications. One shared customer data concept reused. Impact described in documentation fields. No cloned copies of unchanged elements.

## Expected views
- Application Support
- End-to-End Traceability

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-application
- archi-traceability
- archi-model-qa
- archi-documentation

## Pass checks
- Existing CRM element reused, not recreated under a new name for the same system
- Customer data concept appears once
- No new motivation or technology dump
- Confirmation gate shown before any MCP mutate
