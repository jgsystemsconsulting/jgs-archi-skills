<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

<!-- GSD:project-start source:PROJECT.md -->

## Project

**jgs-archi-skills**

A suite of ZCode skills that turn the existing JGS Archi Bridge MCP into a governed, agent-guided architecture-development capability inside Archi. One user-invoked orchestrator elicits architectural intent and produces a plain-language view plan; orchestrator-dispatched specialists create ArchiMate elements, relationships, and views through the MCP without requiring ArchiMate expertise from the user.

**Core Value:** A non-expert can state architectural intent and receive a coherent, ArchiMate-compliant multi-view model plan and construction path that stays governed by the user.

### Constraints

- **Tech stack**: ZCode skills + Python 3.10+ standard library only — no third-party Python deps
- **Interface**: Call existing Archi Bridge MCP only; never copy ArchiMate reference content into skills
- **Canvas**: Archi only; no alternate renderers or EA tools
- **Governance**: User remains in the loop for scope and architectural decisions
- **Persistence**: No database; model documentation fields via MCP hold rationale and content
- **Repo role**: Skills, helpers, tests, and `docs/evidence/` only

<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->

## Technology Stack

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| ZCode skills (`SKILL.md`) | host current | User/orchestrator-invoked skill packages | Delivery form fixed by VISION; install to `~/.zcode/skills/` |
| JGS Archi Bridge MCP | existing plugin | 69 tools + 14 ArchiMate resources | Sole runtime interface to Archi; SoT for language reference |
| Archi | existing install | Modelling canvas and model store | NG-2/NG-5: only canvas and EA tool |
| Python | 3.10+ | Helper scripts (matrix, compliance, suite validation) | Stdlib-only policy; deterministic checks outside the agent loop |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Python standard library only | 3.10+ | argparse, pathlib, json, unittest/assert | All helpers and structural tests |
| *(none else)* | — | — | Third-party deps forbidden by VISION |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| MCP client (host) | Call Archi Bridge at `http://127.0.0.1:18090/mcp` | Skills orchestrate; do not embed HTTP clients if host MCP is available |
| `docs/evidence/` | Capture live scenario transcripts | One E2E scenario per specialist |
| Install script | Copy/link skills into `~/.zcode/skills/` | Repo is source of truth |

## What NOT to Use

| Avoid | Why |
|-------|-----|
| New diagramming/rendering engines | NG-2 |
| Bundled ArchiMate metamodel copies inside skills | NG-4; MCP resources are SoT |
| Databases / skill-side persistence | Stateless skills; model holds content |
| Non-Python helpers or PyPI deps | Policy: Python 3.10+ stdlib only |
| Modifications to jgs-archi-mcp | NG-1 |

## Installation

- Develop skills in-repo under a skills tree (exact layout planner-owned).
- Install script publishes to `~/.zcode/skills/`.
- Require Archi + JGS Archi Bridge MCP running for live evidence; structural checks run offline against MCP tool/resource manifests captured or queried.

## Confidence Notes

- HIGH: delivery form, MCP contract, stdlib policy, non-goals.
- MEDIUM: exact skill file naming and package layout (VISION leaves open to planner).
- LOW: none material for stack choice.

<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
