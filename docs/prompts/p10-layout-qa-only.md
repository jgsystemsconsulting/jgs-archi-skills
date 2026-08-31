<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P10 Layout and QA only

## Priority
P1

## Invoke
/archi-orchestrator the Application Support view is unreadable. Relayout it and report compliance issues. Do not add elements.

## Problem
Application Support already exists in the open model and is unreadable: overlaps, no grouping, connections crossing. The user wants layout and a compliance report. They do not want new concepts.

## Stakeholders
- Model owner
- IT Manager

## Concerns
- Readability
- Illegal relationships already on the view
- Scope creep (new systems appearing)

## Scope
In: layout of the existing Application Support view; QA findings with proposed fixes.
Out: creating elements, other views, and applying QA fixes unless the user later approves them.

## Current state
One messy Application Support view. Content is otherwise in scope as-is.

## Target state
Same elements, readable layout, a QA report. Zero new concepts.

## Expected views
- Application Support

## Specialists expected
- archi-elicit
- archi-viewpoint-select
- archi-layout
- archi-model-qa
- archi-documentation

## Pass checks
- No new elements created
- Layout assessed on Application Support
- QA findings explained with a compliant alternative, not silently applied
- Confirmation gate shown before any MCP mutate
