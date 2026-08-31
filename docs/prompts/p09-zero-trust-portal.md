<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P09 Zero-trust customer portal access

## Priority
P1

## Invoke
/archi-orchestrator customer portal needs zero-trust access: identity, API gateway, and the rule that customers see only their own shipments

## Problem
The TrackIt-style customer portal is opening to more shippers. Security wants identity in front of it, an API gateway, and a clear business rule: a customer sees only their own shipments. This is not a full security-method rollout.

## Stakeholders
- Security lead
- Customer portal owner
- IT Manager
- Customer (shipper)

## Concerns
- Identity before the portal
- Gateway on the API path
- Need-to-know shipment data
- Stay on the ArchiMate language; no invented security metamodel

## Scope
In: the access requirement, the portal and identity/gateway applications, and the technology that hosts them, plus traces.
Out: a full control catalog, physical site security, and migration plateaus.

## Current state
Portal is a pilot. Login is a shared password file. APIs are reached without a gateway.

## Target state
Requirement visible in motivation. Identity and gateway in application. Hosting in technology. Trace from the "own shipments only" rule down to the gateway.

## Expected views
- Motivation Overview
- Application Support
- Technology Platform
- End-to-End Traceability

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-motivation
- archi-application
- archi-technology-physical
- archi-traceability
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Requirement or constraint for own-shipments-only is in the model
- Identity and gateway are distinct from the portal
- Trace from that rule to technology is explicit
- Confirmation gate shown before any MCP mutate
