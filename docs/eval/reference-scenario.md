# Reference Scenario: Meridian Freight (FROZEN)

Status: **FROZEN v1.0 (2026-08-28)**. This file is the single fixed input for
every eval-loop iteration. Skills, helpers, and prompts may change between
iterations; this scenario never changes, so scores stay comparable. A new
scenario would be a new file with a new version; it must never edit this one.

Running the eval loop against this scenario counts as the user approving the
produced View Plan: the scenario below plays both roles (elicitation answers
and standing approval). Mutations are permitted only in the dedicated eval
model (`JGS Eval Loop`), never in any other open model.

The scenario deliberately stays in plain language. Element types, legal
relationships, and viewpoint composition are what the skills must get right
from the MCP resources; the scenario does not give those answers away.

## Problem

Meridian Freight is a regional freight brokerage. Customer service
representatives answer shipment-status questions by calling carriers, re-key
order data between a legacy transport management system and a CRM, and
maintain carrier performance scorecards in offline spreadsheets. Quotes take
up to 4 hours. Management has no reliable, current view of carrier
performance or cost per shipment.

## Stakeholders

- Chief Operating Officer
- Head of Customer Service
- Chief Financial Officer
- IT Manager
- Customer (shipper contracting with Meridian)

## Drivers

- Rising customer expectations for shipment visibility
- Margin pressure on brokerage operations
- Growing volume of carrier and shipment data

## Assessments

- Carrier performance is tracked in offline spreadsheets, updated weekly
- Customer service staff re-key order data between systems

## Goals

- Reduce quote turnaround from 4 hours to 30 minutes
- Increase on-time delivery rate to 95 percent
- Provide a single source of truth for carrier data
- Reduce cost per shipment by 12 percent

## Outcomes

- Faster, more consistent customer answers
- Reduced operating cost per shipment

## Requirements

- Provide self-service shipment tracking for customers
- Integrate carrier data feeds into one platform
- Standardize the customer service process across branches

## Capabilities and Resources

Capabilities Meridian believes it must strengthen:

- Shipment Planning
- Carrier Management
- Customer Inquiry Handling
- Order Management
- Performance Analytics

Resources that support those capabilities:

- Carrier Network (contracted carriers)
- Customer Service Team
- Integration Platform

## Business Operation

Actors:

- Customer Service Representative
- Operations Planner

Processes (with plain-language flow and support expectations):

- Handle Customer Inquiry: intake and triage of customer questions; triggers
  Quote Shipment when pricing is needed
- Quote Shipment: produces a priced quote; hands over to Plan Shipment
- Plan Shipment: books a carrier and schedules the shipment
- Track Shipment: monitors in-transit shipments and updates the customer
- Onboard Carrier: vets and contracts new carriers

Services the business provides to customers and carriers:

- Quoting Service
- Tracking Service
- Carrier Onboarding Service

Information the business works with:

- Shipment Order
- Carrier Profile

## Applications (current state, to be modeled as-is)

- CarrierDesk TMS: legacy transport management system; core quoting and
  shipment planning
- SalesCloud CRM: customer records and inquiry history
- TrackIt Customer Portal: self-service shipment tracking for customers
  (pilot)
- FreightHub Integration Hub: new integration layer connecting the above and
  external carrier feeds

Application-level services these must provide:

- Quote Management Service
- Shipment Tracking Service
- Carrier Data Management Service

Application functions:

- Rate Calculation
- Status Aggregation

Data objects:

- Shipment Record
- Carrier Scorecard
- Customer Record

## Technology

- Brokerage Application Server: hosts CarrierDesk TMS and TrackIt Customer
  Portal (artifacts carrierdesk-tms.ear and trackit-portal.war)
- Integration Gateway: hosts FreightHub Integration Hub (artifact
  freighthub-integration.jar), running a Message Broker and an API
  Management Platform
- Secure Message Transport: technology service used for carrier data feeds

## Expected Views

The run should produce these views (names exactly as written):

1. Motivation Overview
2. Capability Map
3. Customer Service Operations
4. Application Support
5. Technology Platform
6. End-to-End Traceability

The End-to-End Traceability view must let a reader follow at least one
complete path from a goal through business and application to the technology
that supports it, and must show the motivation-to-technology chain for the
"single source of truth for carrier data" goal specifically.

## Scope

In: motivation, strategy (capabilities/resources), business, application,
technology, and cross-layer traceability, as listed above.

Out: implementation and migration planning, physical distribution of goods,
product modeling, detailed data modeling, and any future-state redesign
beyond what is listed.

## Quality Expectations (what the eval scores)

1. Metamodel fidelity: correct element types and only legal relationships,
   per the ArchiMate reference exposed by the MCP (sole source of truth).
2. Layout: each view above is readable without manual cleanup: no overlapping
   shapes, consistent flow direction, grouping by layer or role, sensible
   connection routing.
3. Descriptions: every element and relationship carries a meaningful
   documentation field; a documentation field that merely restates the name
   counts as missing.
4. Analysis: motivation-to-technology traceability is complete, no element is
   unreachable from the motivation chain, and cross-layer dependencies are
   explicit in the model (not only in prose).

Naming follows the repo naming policy (title-collapse-v1): identical concepts
keep identical names across all views.
