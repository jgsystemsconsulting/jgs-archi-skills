<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P06 Motivation-only board pack

## Priority
P1

## Invoke
/archi-orchestrator board pack: drivers, goals, and outcomes for cutting quote time from 4 hours to 30 minutes. No applications.

## Problem
Quotes take up to four hours. The board wants drivers, goals, and outcomes on one page. They explicitly do not want systems on the canvas.

## Stakeholders
- Board sponsor
- Chief Operating Officer
- Head of Sales

## Concerns
- Quote turnaround
- Customer expectation for speed
- Scope creep into applications

## Scope
In: drivers, assessments, goals, outcomes, and requirements that stay in motivation.
Out: applications, technology, physical, processes-as-the-main-view, and migration.

## Current state
Quote time is four hours. Causes are known in prose (re-keying, carrier calls) but not modelled yet.

## Target state
One Motivation Overview. Zero applications on any view this run produces.

## Expected views
- Motivation Overview

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-motivation
- archi-model-qa
- archi-layout
- archi-documentation

## Pass checks
- Only the Motivation Overview view
- No application or technology elements created
- Quote-time goal is explicit
- Confirmation gate shown before any MCP mutate
