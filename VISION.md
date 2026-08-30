<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# VISION

> Owner-authored from the "Agent-Guided ArchiMate Viewpoint Creation in Archi" vision paper. A coordinated skill suite that turns the JGS Archi Bridge MCP into a governed, agent-guided architecture-development capability.

## Why

The JGS Archi Bridge MCP already exposes 69 tools and ArchiMate reference material inside Archi, but using it well still requires the user to know every layer, viewpoint, element type, and relationship before starting. Users get diagrams; nothing interprets architectural intent, selects viewpoints by purpose, keeps views connected across layers, or validates the result. What is missing is architectural reasoning on top of the tooling.

## Objectives

- OBJ-1: Orchestrator skill elicits architectural intent (problem, stakeholders, concerns, scope, current/target state, expected outcome) and produces a plain-language view plan naming viewpoints, layers, modelling sequence, dependencies, and validation points, without requiring ArchiMate expertise from the user.
- OBJ-2: Viewpoint selection is grounded in the ArchiMate viewpoint framework: traceable to stakeholder, concern, purpose, and abstraction level; where no standard viewpoint fits, a justified organisation-specific viewpoint is proposed that stays ArchiMate-compliant.
- OBJ-3: A full specialist skill set covers the vision-enumerated responsibilities (elicitation, viewpoint selection, motivation, capability/strategy, business, application, technology/physical, implementation/migration, cross-layer traceability, model QA, layout/presentation, documentation/rationale), each creating elements, relationships, and views through the Archi MCP.
- OBJ-4: Model coherence and reuse: before creating an element the agent inspects existing model content; shared concepts are reused as single model elements across multiple views, duplicates minimised, naming consistent.
- OBJ-5: Compliance validation checks element types, relationship source/target combinations, permitted relationship types, abstraction levels, cross-view consistency, and naming; violations are explained with a compliant alternative proposed rather than silently applied.
- OBJ-6: Each significant view carries structured rationale (purpose, stakeholders and concerns, viewpoint, questions answered, assumptions, decisions, exclusions, open questions) recorded in the model via MCP, and users can request natural-language changes that regenerate views without damaging the shared model, ending with a completion summary.

## Non-goals (hard constraints: treat like compiler errors)

- NG-1: No modification of the JGS Archi Bridge plugin itself (jgs-archi-mcp); skills consume its tools and resources only.
- NG-2: No new diagramming or rendering engine; Archi is the only canvas.
- NG-3: No fully autonomous architect: scope, interpretation, and architectural decisions remain visible to and governed by the user.
- NG-4: No duplication of ArchiMate language reference material inside the skills; the MCP's resources are the single source of truth.
- NG-5: No support for EA tools other than Archi.

## Implementation direction

- Delivery form: suite of ZCode skills (one SKILL.md per skill) developed in this repo and installed to `~/.zcode/skills/` via an install script. One orchestrator skill (user-invoked) plus the full specialist set from OBJ-3; specialists are orchestrator-dispatched, not user-invoked.
- Runtime and dependency policy: Python 3.10+ for helper scripts, standard library only. Helpers cover deterministic jobs: viewpoint selection matrix, compliance checklist asserts, structural validation of the skill suite. No other dependencies.
- Interface contract: skills call the existing JGS Archi Bridge MCP (default `http://127.0.0.1:18090/mcp`; 69 tools, 14 resources). MCP resources (archimate-layers, archimate-relationships, archimate-specializations, archimate-view-patterns, viewpoint recipes) are the reference source; skills orchestrate them, never copy them. Exact skill naming: open, planner decides.
- Data and persistence stance: no database; skills are stateless. Model content and rationale live inside the Archi model (documentation fields via MCP). The repo holds skills, helpers, and tests.
- Quality bar: every objective is verified two ways: structural checks (a helper script validates that each skill references only real MCP tools and coherent recipes) and one documented live end-to-end scenario per specialist against a real Archi model via the MCP.

## Alignment

Every seed must cite a live OBJ-n. Seeds that advance an NG-n are rejected.

## Review cadence

When this file stops predicting what gets built, rewrite it.
