<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P02 Regional insurance merger

## Priority
P0

## Invoke
/archi-orchestrator Northridge and Vale insurance merger: current vs target customer onboarding, with a migration roadmap

## Problem
Two regional insurers are merging. Customers still onboard through two different journeys. Claims and policy admin are duplicated. The board wants one onboarding journey in 18 months without pretending the cores disappear on day one.

## Stakeholders
- Merger programme sponsor
- Head of Customer Operations
- Claims lead (Northridge)
- Policy admin lead (Vale)
- IT Manager
- Regulator liaison

## Concerns
- Dual processes during the plateau
- Customer lettering and identity
- Which work packages retire which systems
- No silent "just replace the core"

## Scope
In: motivation for the merger, as-is and target onboarding, application landscape, plateaus, gaps, and work packages.
Out: product pricing redesign, detailed data modelling, and physical mail-room layout.

## Current state
Northridge uses PolicyBox and a claims desktop. Vale uses ValeCore and a separate portal. Both print welcome packs. Staff re-key at the boundary.

## Target state
One onboarding journey. Two plateaus: dual-run, then ValeCore retired. Work packages named, not a single big-bang cutover.

## Expected views
- Motivation Overview
- Current Customer Onboarding
- Target Customer Onboarding
- Application Landscape
- Migration Roadmap

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-motivation
- archi-capability-strategy
- archi-business
- archi-application
- archi-implementation-migration
- archi-traceability
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Views named exactly as listed
- Plateaus or work packages exist in the model
- Gaps are explicit elements or relationships, not only prose
- Northridge and Vale systems remain distinct on the current view
- Confirmation gate shown before any MCP mutate
