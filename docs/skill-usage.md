<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Using jgs-archi-skills

## Prerequisites

- Archi with the JGS Archi Bridge plugin running.
- MCP endpoint (default `http://127.0.0.1:18090/mcp`). See [MCP.md](MCP.md).
- Python 3.10+ on PATH (standard library only; no pip packages).
- A host that can load Agent Skills (`SKILL.md`). ZCode is the default install
  target. Claude Code, Copilot CLI, OpenClaw, and Codex read the folder
  natively; Gemini and Cursor use the installer transform. See
  [other-agents.md](other-agents.md).

## Install

```bash
python install.py                 # ZCode, flat ~/.zcode/skills/<skill>/
python install.py --dry-run       # preview, write nothing
python install.py --agent claude  # namespaced ~/.claude/skills/jgs/<skill>/
python install.py --agent all     # every user-global agent
python install.py --list-agents
```

Restart the agent session so it discovers the skills.

To install both the Bridge plugin and this pack in one shot, paste the
"Install with your AI agent" prompt from [README.md](../README.md) into
your coding agent.

## Invoke / first run

User-facing skills are `/archi-orchestrator` (modelling) and
`/jgs-upstream-feedback` (pack defects). Example modelling invoke:
`/archi-orchestrator invoice-to-cash capability map for finance and ops`.

It elicits intent, drafts a schema-checked View Plan, grounds viewpoints, and
stops at a confirmation gate. Specialists run only after you approve the plan.
Do not invoke layer specialists yourself.

If a run hits a pack or MCP-contract hole that any user would hit, the
orchestrator may offer to raise a GitHub issue. You can also invoke
`/jgs-upstream-feedback` later.

Companion docs:

- Shared modelling contract: [CREATE_PATH.md](CREATE_PATH.md)
- House style: [MODELLING_CONVENTIONS.md](MODELLING_CONVENTIONS.md)
- Skill index: [SKILLS.md](../SKILLS.md)
- MCP consume-only contract: [MCP.md](MCP.md)
- Diagrams: [cooperation](diagrams/cooperation.html) and [modelling run](diagrams/modelling-run.html)

## Starter prompts

Copy a one-liner from [docs/prompts/README.md](prompts/README.md). Each card
also has the elicit fields, expected views, specialists, and pass checks.

P0 examples:

```text
/archi-orchestrator invoice-to-cash capability map for finance and ops
/archi-orchestrator Northridge and Vale insurance merger: current vs target customer onboarding, with a migration roadmap
/archi-orchestrator manufacturing plant: as-is shop floor and the CRM programme that is supposed to fix order visibility
/archi-orchestrator on the current model, add a second CRM for the European branch and show impact; do not duplicate shared customer data
```

Do not invoke specialists yourself. Do not paste element-create commands.

## What it does, in order

1. Elicit and normalize intent (`archi-elicit`).
2. Draft the View Plan; ground viewpoints (`archi-viewpoint-select`).
3. Wait for your approve / revise / abort.
4. Dispatch layer specialists (motivation, capability/strategy, business,
   application, technology/physical, implementation/migration) as the plan
   requires.
5. Trace, QA, layout, and documentation specialists close the run.

Interactive modelling run: [diagrams/modelling-run.html](diagrams/modelling-run.html).

Helpers under `helpers/` are stdlib checkers the skills call. They never talk
to the MCP. Live MCP checks are opt-in via `python tests/live_mcp_smoke.py`.
