<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Orchestrator prompt pack

Copy one invoke line into your skill runner after install. Specialists stay
orchestrator-dispatched. The orchestrator still stops at the View Plan
confirmation gate. These cards are job shortcuts, not ArchiMate tutorials.

Do not paste element-type commands (create a named actor, create a named
application). That bypasses elicitation and user governance.

How to invoke: [skill-usage.md](../skill-usage.md).

## P0 (release-shaped)

```text
/archi-orchestrator invoice-to-cash capability map for finance and ops
/archi-orchestrator Northridge and Vale insurance merger: current vs target customer onboarding, with a migration roadmap
/archi-orchestrator manufacturing plant: as-is shop floor and the CRM programme that is supposed to fix order visibility
/archi-orchestrator on the current model, add a second CRM for the European branch and show impact; do not duplicate shared customer data
```

## P1 (one-specialist depth)

```text
/archi-orchestrator same freight visibility problem, but I need three views: COO overview, customer-service detail, IT application usage
/archi-orchestrator board pack: drivers, goals, and outcomes for cutting quote time from 4 hours to 30 minutes. No applications.
/archi-orchestrator we have four overlapping quoting tools. Map the as-is application landscape and which business services they serve.
/archi-orchestrator move the legacy TMS to a cloud landing zone; plateaus and work packages only. Do not redesign the business.
/archi-orchestrator customer portal needs zero-trust access: identity, API gateway, and the rule that customers see only their own shipments
/archi-orchestrator the Application Support view is unreadable. Relayout it and report compliance issues. Do not add elements.
```

## P2 (same skeleton, new domain)

```text
/archi-orchestrator regional clinic: patient intake to discharge, EHR vs billing, 48-hour referral target
/archi-orchestrator city planning permits: citizen portal, back-office case system, GIS, statutory timescales
/archi-orchestrator retail bank: current-account onboarding only. Capabilities, processes, and the apps that realize them. No full industry landscape.
/archi-orchestrator one-day conference: registration, badge printing, wifi, and the volunteer process
```

## Cards

Each file is a frozen brief: elicit fields, expected views, specialists, and
pass checks. Live Archi runs are opt-in. Offline check:

```bash
python helpers/prompt_card_schema.py docs/prompts
```

| Card | File |
|------|------|
| Invoice to cash | [p01-invoice-to-cash.md](p01-invoice-to-cash.md) |
| Insurance merger | [p02-insurance-merger.md](p02-insurance-merger.md) |
| Plant and CRM | [p03-plant-crm.md](p03-plant-crm.md) |
| NL change, second CRM | [p04-nl-change-second-crm.md](p04-nl-change-second-crm.md) |
| Viewpoint split | [p05-viewpoint-split.md](p05-viewpoint-split.md) |
| Motivation only | [p06-motivation-only.md](p06-motivation-only.md) |
| Shadow quoting tools | [p07-shadow-quoting-tools.md](p07-shadow-quoting-tools.md) |
| TMS cloud migration | [p08-tms-cloud-migration.md](p08-tms-cloud-migration.md) |
| Zero-trust portal | [p09-zero-trust-portal.md](p09-zero-trust-portal.md) |
| Layout and QA only | [p10-layout-qa-only.md](p10-layout-qa-only.md) |
| Clinic EHR | [p11-clinic-ehr.md](p11-clinic-ehr.md) |
| Planning permits | [p12-planning-permits.md](p12-planning-permits.md) |
| Bank onboarding | [p13-bank-onboarding.md](p13-bank-onboarding.md) |
| Conference event | [p14-conference-event.md](p14-conference-event.md) |

The maintainer eval-loop frozen scenario (Meridian Freight) stays under
`docs/eval/` and is not this pack. Do not edit it to add prompts.
