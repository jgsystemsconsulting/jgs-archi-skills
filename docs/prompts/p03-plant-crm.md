<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P03 Plant operations and CRM programme

## Priority
P0

## Invoke
/archi-orchestrator manufacturing plant: as-is shop floor and the CRM programme that is supposed to fix order visibility

## Problem
A metals plant runs production on a MES and an on-site ERP. Sales still track orders in spreadsheets. A CRM programme is funded to fix order visibility. Plant engineers worry the CRM will be drawn as if it replaces the MES.

## Stakeholders
- Plant manager
- Head of Sales
- MES owner
- CRM programme manager
- Operations planner

## Concerns
- Order visibility from quote to mill schedule
- CRM must not swallow MES
- Equipment and the mill building stay in scope
- What the integration platform actually connects

## Scope
In: motivation for visibility, capabilities, production operations, applications, technology nodes, and physical equipment or facility that hosts them.
Out: implementation roadmap (no work packages), product costing, and a greenfield MES rewrite.

## Current state
MES schedules the mill. ERP holds works orders. Sales spreadsheets hold customer promises. A new CRM is in pilot. An integration gateway sits in the plant comms room.

## Target state
As-is picture that still shows mill equipment and MES, plus the CRM as a sales-facing system served by the gateway. Shared order identity, not a merged blob.

## Expected views
- Motivation Overview
- Capability Map
- Production Operations
- Application Support
- Technology and Physical

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-motivation
- archi-capability-strategy
- archi-business
- archi-application
- archi-technology-physical
- archi-traceability
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Views named exactly as listed
- At least one facility or equipment element assigned to a node
- CRM and MES remain separate applications
- Confirmation gate shown before any MCP mutate
