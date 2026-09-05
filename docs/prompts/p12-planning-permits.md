<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P12 City planning permits

## Priority
P2

## Invoke
/archi-orchestrator city planning permits: citizen portal, back-office case system, GIS, statutory timescales

## Problem
A city planning team misses statutory timescales. Citizens submit on a portal. Casework sits in a back-office system. GIS is a separate stack. Nobody has one picture of the permit journey.

## Stakeholders
- Head of Planning
- Case officer
- GIS lead
- Citizen (applicant)
- Legal/statutory officer

## Concerns
- Statutory clock
- Portal versus case system versus GIS
- What the citizen can see

## Scope
In: permit process, the three applications, traces to the timescale goal.
Out: building-control inspections as a full physical model, and a vendor replacement programme.

## Current state
Portal takes PDF uploads. Case system is 12 years old. GIS is desktop for specialists. Timescales are tracked in a spreadsheet.

## Target state
As-is operations and application support with the statutory timescale as a goal. Three systems stay three systems.

## Expected views
- Motivation Overview
- Permit Operations
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
- Statutory timescale appears as a goal or requirement
- Portal, case system, and GIS remain distinct
- Confirmation gate shown before any MCP mutate
