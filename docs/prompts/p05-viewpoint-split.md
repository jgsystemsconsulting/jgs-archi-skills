<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P05 Stakeholder viewpoint split

## Priority
P1

## Invoke
/archi-orchestrator same freight visibility problem, but I need three views: COO overview, customer-service detail, IT application usage

## Problem
Shipment visibility is poor. The COO wants one overview. Customer service wants the inquiry handling path in detail. IT wants which applications are used in that path. Same model, three audiences.

## Stakeholders
- Chief Operating Officer
- Head of Customer Service
- IT Manager
- Customer service representative

## Concerns
- Overview versus detail
- One shared set of concepts
- No extra layers beyond business and application
- Each view answers that stakeholder's question

## Scope
In: business and application content for freight visibility, three justified viewpoints.
Out: technology, physical, migration, and a fourth audience.

## Current state
Representatives call carriers. Status sits in a TMS and a CRM. No shared picture.

## Target state
Three views on one model. Viewpoint choices traced to stakeholder, concern, purpose, and abstraction.

## Expected views
- COO Overview
- Customer Service Detail
- IT Application Usage

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-business
- archi-application
- archi-layout
- archi-documentation

## Pass checks
- Three views named exactly as listed
- Viewpoint trace exists (stakeholder, concern, purpose, abstraction)
- Same real-world concepts keep the same names across views
- Confirmation gate shown before any MCP mutate
