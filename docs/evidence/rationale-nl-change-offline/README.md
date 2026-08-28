# Evidence: rationale-nl-change-offline

Offline pack for OBJ-6 / SEED-006 (v1.5). No live Archi MCP required.

## Contents

| Path | Purpose |
|------|---------|
| `valid/*.md` | Multi-view rationale pack (all required sections, non-empty) |
| `invalid/missing-sections.md` | Fails missing_section |
| `invalid/empty-decisions.md` | Fails empty_section |
| `inventory.json` + `change-note.txt` | NL-change inputs |
| `nl-change-impact.json` | Impact plan preserving shared `el-customer` |
| `completion-summary-valid.md` / `invalid` | RATE-03 pass/fail |
| `*-result.txt` | Captured helper CLI output |

## Commands

```bash
python helpers/rationale_schema.py --bundle docs/evidence/rationale-nl-change-offline/valid
python helpers/rationale_schema.py --bundle docs/evidence/rationale-nl-change-offline/invalid
python helpers/nl_change_impact.py docs/evidence/rationale-nl-change-offline/change-note.txt docs/evidence/rationale-nl-change-offline/inventory.json
python helpers/completion_summary_schema.py docs/evidence/rationale-nl-change-offline/completion-summary-valid.md
python -m unittest discover -s tests -q
python helpers/validate_skill_mcp_refs.py
```

## Regression freeze

- `archi-viewpoint-select` SHA256 remains v1.1 freeze `01ad2cc359bb1a4e42a26d8eda383b394fc73a6409373736eba1c5bd6caf94ea`
- Thin v1.0 rationale heading API (`missing_headings`) still usable
- No rework of v1.0–v1.4 cores beyond rationale/documentation hooks (NG-1..5)
