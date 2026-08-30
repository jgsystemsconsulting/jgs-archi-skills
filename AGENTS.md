<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# jgs-archi-skills

Agent-guided ArchiMate viewpoint creation in Archi: an orchestrator plus specialist ZCode skills driving the JGS Archi Bridge MCP.

<!-- ralph-setup:implementation begin -->
## Implementation direction (binding)

- Delivery form: suite of ZCode skills (one SKILL.md per skill) developed in this repo and installed to `~/.zcode/skills/` via an install script. One orchestrator skill (user-invoked) plus the full specialist set (elicitation, viewpoint selection, motivation, capability/strategy, business, application, technology/physical, implementation/migration, cross-layer traceability, model QA, layout/presentation, documentation/rationale); specialists are orchestrator-dispatched, not user-invoked.
- Runtime and dependency policy: Python 3.10+ helper scripts, standard library only (viewpoint selection matrix, compliance checklist asserts, structural validation of the suite). No other dependencies.
- Interface contract: skills call the existing JGS Archi Bridge MCP (default `http://127.0.0.1:18090/mcp`; 69 tools, 14 resources). MCP resources are the ArchiMate reference source of truth; skills orchestrate them, never copy them. Skill naming: open, planner decides.
- Data and persistence stance: no database; skills are stateless. Model content and rationale live inside the Archi model via MCP documentation fields. The repo holds skills, helpers, and tests.
- Quality bar: each objective is verified by structural checks (skills reference only real MCP tools) plus one documented live end-to-end scenario per specialist against a real Archi model via the MCP.

Constraints inherited from VISION.md: never modify jgs-archi-mcp, never duplicate ArchiMate reference material into skills, Archi is the only canvas, the user governs scope and architectural decisions, no EA tools other than Archi.
<!-- ralph-setup:implementation end -->
