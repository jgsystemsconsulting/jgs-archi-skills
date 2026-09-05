<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# P01 Invoice to cash

## Priority
P0

## Invoke
/archi-orchestrator invoice-to-cash capability map for finance and ops

## Problem
A mid-size manufacturer quotes by email, books orders in the ERP, and chases collections from a spreadsheet. Finance cannot see cash in flight. Operations cannot see which capabilities actually run quote, order, invoice, and collect.

## Stakeholders
- Chief Financial Officer
- Head of Operations
- IT Manager
- Credit controller

## Concerns
- Time from quote to cash
- Duplicate customer and order data
- Which capabilities the ERP already covers versus spreadsheet work

## Scope
In: capabilities, the order-to-cash processes, and the applications that support them.
Out: shop-floor control, physical distribution, payroll, and a future-state ERP replacement.

## Current state
ERP holds orders and invoices. Quotes live in email. Collections live in a spreadsheet. Customer records exist in both ERP and a small CRM.

## Target state
One capability map that finance and ops agree on, with the as-is processes and the applications that realize them. No redesign of the ERP.

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
- Views named exactly as listed
- Same capability names on every view that shows them
- At least one path from a capability through a process to an application
- Documentation fields are not a restatement of the name
- Confirmation gate shown before any MCP mutate
