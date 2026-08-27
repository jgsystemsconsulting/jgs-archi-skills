# Stack Research

**Domain:** Agent-guided ArchiMate modelling skill suite (ZCode skills + Archi MCP)
**Researched:** 2026-08-27
**Confidence:** HIGH (owner VISION + known MCP contract; library versions N/A)

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
