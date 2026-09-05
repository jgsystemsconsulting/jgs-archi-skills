<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P08 Legacy TMS to cloud landing zone

## Priority
P1

## Invoke
/archi-orchestrator move the legacy TMS to a cloud landing zone; plateaus and work packages only. Do not redesign the business.

## Problem
CarrierDesk TMS runs on an on-prem application server. Infrastructure wants it in a cloud landing zone. The operating model stays as it is. The ask is plateaus, gaps, and work packages.

## Stakeholders
- IT Manager
- Infrastructure lead
- TMS application owner
- Security lead
- Operations (informed only)

## Concerns
- Dual-run window
- What happens to the on-prem server
- Business layer must not be rewritten
- Cutover is a work package, not a slogan

## Scope
In: technology as-is and target, implementation and migration (plateaus, gaps, work packages).
Out: new business processes, new capabilities, and a CRM programme.

## Current state
Brokerage Application Server hosts CarrierDesk TMS. Users are internal planners.

## Target state
TMS runs in the landing zone. On-prem server is a plateau then a decommission work package. Business elements unchanged if they already exist; this run does not invent a new operating model.

## Expected views
- Technology Current
- Technology Target
- Migration Roadmap

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-technology-physical
- archi-implementation-migration
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Plateaus or work packages exist
- No new business process invented to justify the move
- Confirmation gate shown before any MCP mutate
