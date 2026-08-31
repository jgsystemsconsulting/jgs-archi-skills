<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P11 Regional clinic intake to discharge

## Priority
P2

## Invoke
/archi-orchestrator regional clinic: patient intake to discharge, EHR vs billing, 48-hour referral target

## Problem
A regional clinic loses referrals in paper handoffs between intake, the EHR, and billing. The clinical director wants a 48-hour referral target made visible, with as-is systems left distinct.

## Stakeholders
- Clinical director
- Practice manager
- Billing lead
- IT lead
- Referring GP (external)

## Concerns
- Referral turnaround
- EHR versus billing overlap
- Patient identity across the journey

## Scope
In: motivation for the 48-hour target, intake-to-discharge process, EHR and billing applications.
Out: medical-device modelling, national spine integration, and a greenfield EHR.

## Current state
Intake is a paper form. EHR holds clinical notes. Billing is a separate package. Referrals sit in a shared inbox.

## Target state
As-is picture plus the 48-hour goal. EHR and billing stay two applications.

## Expected views
- Motivation Overview
- Patient Journey
- Application Support

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-motivation
- archi-business
- archi-application
- archi-traceability
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- 48-hour referral goal is in the model
- EHR and billing remain distinct
- Confirmation gate shown before any MCP mutate
