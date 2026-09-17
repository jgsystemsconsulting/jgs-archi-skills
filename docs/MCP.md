<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# MCP contract (JGS Archi Bridge)

## Endpoint

Default MCP HTTP endpoint:

```text
http://127.0.0.1:18090/mcp
```

Skills and agents talk to the running JGS Archi Bridge inside Archi. Do not hard-code alternate hosts in skill logic without documenting the override.

## Attach from ZCode

ZCode reads MCP servers from `~/.zcode/cli/config.json` (user scope) or
`<repo>/.zcode/config.json` (workspace scope; a same-named user entry
overrides the workspace entry). Add the bridge under `mcp.servers`:

```json
{
  "mcp": {
    "servers": {
      "archi": {
        "type": "http",
        "url": "http://127.0.0.1:18090/mcp"
      }
    }
  }
}
```

Merge into an existing `mcp.servers` object if one is present; do not
replace unrelated servers. Restart the ZCode session after editing, then
check Settings, MCP: `archi` should show connected. A failed status almost
always means the bridge is not running; start the MCP server in Archi first,
then reconnect.

Two host caveats: the config schema is strict, so an unknown key silently
drops the server, and config files do not expand `${...}` variables, which
does not matter for this fixed localhost URL.

Claude Code equivalent:

```bash
claude mcp add --transport http archi http://127.0.0.1:18090/mcp
```

Other hosts (Claude Desktop, Cline, Cursor): see the jgs-archi-mcp README.

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
