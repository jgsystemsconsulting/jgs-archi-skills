# jgs-archi-skills

Agent-guided ArchiMate viewpoint creation in Archi: a ZCode skill suite that drives the existing [JGS Archi Bridge MCP](https://github.com/) (consume-only).

## Prerequisites

- Archi with the JGS Archi Bridge plugin
- MCP endpoint (default): see [docs/MCP.md](docs/MCP.md) (`http://127.0.0.1:18090/mcp`)
- Python 3.10+ (standard library only; no pip packages required)

## Install skills

```bash
python install.py
```

Installs each `skills/<name>/` package that contains `SKILL.md` into `~/.zcode/skills/<name>/`.

Optional: `python install.py --link` (symlink when the OS allows; otherwise copy).

## Validate MCP references

```bash
python helpers/validate_skill_mcp_refs.py
```

Fails if any skill cites an MCP tool or `archimate://` resource not listed in `docs/mcp/archi-bridge-inventory.json`.

```bash
python -m unittest tests.test_validate_skill_mcp_refs -v
```

## Layout

| Path | Role |
|------|------|
| `skills/` | ZCode skill packages (`SKILL.md` each) |
| `helpers/` | Stdlib validators and matrices |
| `docs/MCP.md` | Endpoint + consume-only contract |
| `docs/mcp/archi-bridge-inventory.json` | Offline 69-tool / 14-resource allowlist |
| `docs/evidence/` | Live scenario captures (later phases) |
| `VISION.md` | Product objectives and non-goals |
| `.planning/` | GSD roadmap and phase state |

## Status

Phase 1 foundations: inventory, structural validator, install path, docs. Orchestrator skill (OBJ-1) is Phase 2.
