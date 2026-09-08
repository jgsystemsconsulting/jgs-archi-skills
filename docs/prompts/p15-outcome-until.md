<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P15 Quote to cash until traceable

## Priority
P1

## Invoke
/archi-orchestrator until: finance and ops can trace quote to cash on the model from a capability through a process to an application

## Problem
A mid-size manufacturer quotes by email, books orders in the ERP, and chases collections from a spreadsheet. Finance and ops do not need another named map. They need to follow quote, order, invoice, and collect on the model.

## Stakeholders
- Chief Financial Officer
- Head of Operations
- IT Manager
- Credit controller

## Concerns
- Time from quote to cash
- Duplicate customer and order data
- Whether the ERP already covers a capability or a spreadsheet still does

## Scope
In: whatever layers make the quote-to-cash path visible.
Out: shop-floor control, physical distribution, payroll, and a future-state ERP replacement.

## Current state
ERP holds orders and invoices. Quotes live in email. Collections live in a spreadsheet. Customer records exist in both ERP and a small CRM.

## Target state
Finance and ops can trace quote to cash from a capability through a process to an application. No mill. No future ERP.

## Expected views
- Capability Map
- Order-to-Cash Operations
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
- A path from a capability through a process to an application is visible on the model
- Quote, order, invoice, and collect are followable on those views
- Shop floor, physical distribution, payroll, and a future ERP are absent
- Confirmation gate shown before any MCP mutate
