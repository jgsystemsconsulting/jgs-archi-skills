<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P14 One-day conference operations

## Priority
P2

## Invoke
/archi-orchestrator one-day conference: registration, badge printing, wifi, and the volunteer process

## Problem
A one-day conference runs registration on a laptop, prints badges at a side table, and gives volunteers a paper list. Wifi is a venue service. The organiser wants a small as-is picture, not an enterprise rebuild.

## Stakeholders
- Event organiser
- Volunteer lead
- Venue IT
- Attendee

## Concerns
- Queue at registration
- Badge errors
- Wifi as a venue service, not a company data centre

## Scope
In: volunteer process, registration and badge applications or devices, venue wifi as technology.
Out: multi-year event strategy, CRM for attendees, and a cloud migration.

## Current state
Spreadsheet of attendees. Badge printer on a volunteer laptop. Venue wifi with a shared code.

## Target state
Small operations view plus the technology that hosts registration and wifi.

## Expected views
- Volunteer Operations
- Technology Platform

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-business
- archi-technology-physical
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Wifi is modelled as venue technology, not an in-house data centre
- Volunteer process is present
- Confirmation gate shown before any MCP mutate
