<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P07 Shadow quoting tools

## Priority
P1

## Invoke
/archi-orchestrator we have four overlapping quoting tools. Map the as-is application landscape and which business services they serve.

## Problem
Four quoting tools grew up in different branches. Nobody can say which business service each one serves. Consolidation talk keeps stalling because the as-is map does not exist.

## Stakeholders
- IT Manager
- Branch managers (four)
- Head of Sales
- Integration lead

## Concerns
- Overlap versus genuine difference
- Which business services break if a tool is retired
- Naming: four tools, not one blob

## Scope
In: as-is applications and the business services they serve.
Out: target-state design, vendor scorecards, and technology hosting.

## Current state
Tools: QuoteFast (north), RateSheet (south, spreadsheet plus macros), CarrierDesk quoting module, and a broker portal used by one team. All produce a priced quote.

## Target state
Application landscape that still shows four systems and the services they serve. No silent merge.

## Expected views
- Application Landscape
- Business Services Served

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-business
- archi-application
- archi-traceability
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Four quoting applications remain distinct
- Each is tied to at least one business service
- Confirmation gate shown before any MCP mutate
