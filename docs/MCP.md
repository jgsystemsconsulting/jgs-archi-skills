<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# MCP contract (JGS Archi Bridge)

## Endpoint

Default MCP HTTP endpoint:

```text
http://127.0.0.1:18090/mcp
```

Skills and agents talk to the running JGS Archi Bridge inside Archi. Do not hard-code alternate hosts in skill logic without documenting the override.

## Consume-only policy

- Skills **consume** MCP tools and resources only.
- **Never modify** the jgs-archi-mcp plugin, its handlers, or its shipped resources.
- **Never copy** ArchiMate language reference tables into skills. Read `archimate://reference/*` and `archimate://recipes/*` from the MCP.
- Pack defects that look like a missing or wrong bridge tool file as GitHub
  issues on jgs-archi-mcp. Do not open plugin pull requests from these skills.

## Offline inventory

Canonical offline allowlist (69 tools, 14 resources):

```text
docs/mcp/archi-bridge-inventory.json
```

Source: jgs-archi-mcp README "Available Tools" catalog + `ResourceHandler` URI map, captured 2026-08-27.

When Archi is running, live `tools/list` / resource list is preferred for discovery. CI and structural checks use the inventory file so validation works offline.

### Refresh procedure

1. Open sibling checkout of jgs-archi-mcp (do not edit it from this repo).
2. Re-parse README Available Tools bullets and ResourceHandler resource URIs.
3. Replace `docs/mcp/archi-bridge-inventory.json` keeping `policy` flags.
4. Run `python helpers/validate_skill_mcp_refs.py` and fix any skill drift.

## Structural validation

```bash
python helpers/validate_skill_mcp_refs.py
```

Fails (exit 1) if any `skills/**/SKILL.md` cites a tool or `archimate://` resource not in the inventory.

## Install

```bash
python install.py
```

Copies each `skills/<name>/` package that contains `SKILL.md` into `~/.zcode/skills/<name>/`.
