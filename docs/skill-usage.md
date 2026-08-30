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

## Invoke / first run

The only user-facing skill is the orchestrator:

```text
/archi-orchestrator
/archi-orchestrator invoice-to-cash capability map for finance and ops
```

It elicits intent, drafts a schema-checked View Plan, grounds viewpoints, and
stops at a confirmation gate. Specialists run only after you approve the plan.
Do not invoke specialists yourself.

Companion docs:

- Shared modelling contract: [CREATE_PATH.md](CREATE_PATH.md)
- Skill index: [SKILLS.md](../SKILLS.md)
- MCP consume-only contract: [MCP.md](MCP.md)

## What it does, in order

1. Elicit and normalize intent (`archi-elicit`).
2. Draft the View Plan; ground viewpoints (`archi-viewpoint-select`).
3. Wait for your approve / revise / abort.
4. Dispatch layer specialists (motivation, capability/strategy, business,
   application, technology/physical, implementation/migration) as the plan
   requires.
5. Trace, QA, layout, and documentation specialists close the run.

Helpers under `helpers/` are stdlib checkers the skills call. They never talk
to the MCP. Live MCP checks are opt-in via `python tests/live_mcp_smoke.py`.
