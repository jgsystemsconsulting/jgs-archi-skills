# jgs-archi-skills

Agent-guided ArchiMate viewpoint creation in Archi: a ZCode skill suite that
drives the existing JGS Archi Bridge MCP (consume-only). One orchestrator
skill plus twelve specialists; Archi is the only canvas, and the MCP
resources are the sole ArchiMate reference.

## Prerequisites

- Archi with the JGS Archi Bridge plugin
- MCP endpoint (default): see [docs/MCP.md](docs/MCP.md)
  (`http://127.0.0.1:18090/mcp`, 69 tools, 14 resources)
- Python 3.10+ (standard library only; no pip packages required)

## Install skills

```bash
python install.py
```

Installs each `skills/<name>/` package that contains `SKILL.md` into
`~/.zcode/skills/<name>/`.

Optional: `python install.py --link` (symlink when the OS allows; otherwise
copy).

## Usage

Invoke the orchestrator from your ZCode skill runner:

```
/archi-orchestrator <plain-language intent>
```

The orchestrator elicits intent, drafts a schema-checked view plan, grounds
viewpoints via archi-viewpoint-select, and (after your approval) dispatches
layer specialists, traceability, QA, layout, and documentation in order.
Specialists are orchestrator-dispatched, not user-invoked.

## Tests

```bash
python -m unittest discover -s tests -q
```

76 tests cover the helpers, specialist contracts, and the offline fixtures.
Tests never call the MCP; live checks are opt-in via
`python tests/live_mcp_smoke.py` (requires Archi + Bridge running and the
scratch model bound; see `docs/evidence/live-archi-smoke/README.md`).

## Structural validation

```bash
python helpers/validate_skill_mcp_refs.py
```

Fails if any skill cites an MCP tool or `archimate://` resource not listed
in `docs/mcp/archi-bridge-inventory.json`.

## Eval loop and gates

`docs/eval/reference-scenario.md` is the frozen evaluation scenario.
`GATES.md` holds the release gate ledger: metamodel, naming, rationale,
documentation coverage, and layout checks over an unattended model build,
plus a fresh-model confirmation run. All 10 gates are met with recorded
evidence under `docs/evidence/eval-loop/`. Iteration history and scores:
`ITERATION-0.md` and `ITERATION-1.md` in the same directory. The harness
that runs the loop lives in `docs/eval/`.

## Layout

| Path | Role |
|------|------|
| `skills/` | ZCode skill packages (`SKILL.md` each) |
| `helpers/` | Stdlib validators, checkers, and matrices |
| `docs/eval/` | Eval-loop harness (MCP session, builder, exporter, gate checks) |
| `docs/evidence/` | Offline fixtures, live scenario captures, eval-loop runs |
| `docs/MCP.md` | Endpoint + consume-only contract |
| `docs/mcp/archi-bridge-inventory.json` | Offline 69-tool / 14-resource allowlist |
| `docs/CREATE_PATH.md` | Shared specialist modelling contract |
| `VISION.md` | Product objectives and non-goals |
| `GATES.md` | Release gate ledger with evidence |
| `CHANGELOG.md` | Milestone history (v1.0 through v1.6) |
| `.planning/` | GSD roadmap and phase state |

## Status

Milestone **v1.6**: eval loop complete. Unattended builds from the frozen
scenario pass metamodel, naming, rationale, documentation-coverage, and
layout checks with zero findings; a fresh-model confirmation run reproduces
green. History: v1.0 foundations and orchestrator; v1.1 viewpoint select;
v1.2 full specialist set; v1.3 coherence and reuse; v1.4 compliance
validation; v1.5 rationale depth; v1.6 eval loop and live evidence. See
[CHANGELOG.md](CHANGELOG.md).
