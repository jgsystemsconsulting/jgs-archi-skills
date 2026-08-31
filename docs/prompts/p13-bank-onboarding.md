<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P13 Retail current-account onboarding

## Priority
P2

## Invoke
/archi-orchestrator retail bank: current-account onboarding only. Capabilities, processes, and the apps that realize them. No full industry landscape.

## Problem
A retail bank wants current-account onboarding modelled end to end. Other products are out. The risk is drawing a giant industry map instead of this one journey.

## Stakeholders
- Head of Retail Onboarding
- Branch operations
- Digital channel owner
- Compliance (KYC)
- IT Manager

## Concerns
- KYC handoff
- Branch versus digital path
- Scope exploding into every banking product

## Scope
In: onboarding capabilities, the current-account process, applications that realize that process.
Out: payments, lending, cards, and any full industry-reference landscape.

## Current state
Branch uses a teller desktop. Digital uses a web form that drops into the same core. KYC is a separate case tool.

## Target state
Capability map and operations for this product only, with the apps that realize it.

## Expected views
- Capability Map
- Current-Account Onboarding
- Application Support

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-capability-strategy
- archi-business
- archi-application
- archi-traceability
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- No elements named for other products (loans, cards, payments) unless the user later expands scope
- KYC tool remains distinct from the core
- Confirmation gate shown before any MCP mutate
