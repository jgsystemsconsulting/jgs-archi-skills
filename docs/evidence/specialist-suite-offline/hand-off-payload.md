<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Hand-off payload (approved)

- confirmation_status: approved
- intent_summary: Move from nightly batch invoicing to near-real-time billing events for B2B customers
- stakeholders_concerns: CFO (cash timing); Ops (failure handling); IT (integration load)
- viewpoints: Motivation; Business Process; Application Cooperation; Technology; Implementation and Migration
- layers_in_scope: motivation, business, application, technology, implementation
- modelling_sequence: motivation goals → billing capability → invoice process → billing apps → runtime nodes → migration plateaus
- reuse_constraints: reuse existing Customer and Invoice concepts if present
- open_questions: event bus product choice deferred
- target_views: (none pre-existing in offline fixture)
