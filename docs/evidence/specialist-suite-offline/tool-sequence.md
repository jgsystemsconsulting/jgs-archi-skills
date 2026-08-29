<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Expected tool sequence (offline)

Inventory names only. Not a live transcript.

## Layer specialists (each)
search-elements → get-or-create-element → create-relationship → create-view → add-to-view

## archi-traceability
search-elements → get-relationships → create-relationship → create-view → add-to-view

## archi-model-qa
get-views → get-view-contents → get-relationships → search-elements → (optional authorized update-*)

## archi-layout
get-view-contents → assess-layout → auto-layout-and-route → auto-route-connections → assess-layout

## archi-documentation
get-view-contents → update-view / update-element (documentation fields)
