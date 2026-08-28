# Regression lock (v1.4 phase 18)

## Suite

```text
python -m unittest discover -s tests -q
# expect: OK (46+ tests)
python helpers/validate_skill_mcp_refs.py
# expect: ok: N skill file(s), 0 unknown refs
```

## Viewpoint-select freeze (v1.1 digest)

```text
sha256sum skills/archi-viewpoint-select/SKILL.md
# expect: 01ad2cc359bb1a4e42a26d8eda383b394fc73a6409373736eba1c5bd6caf94ea
```

## Thin checklist retained

`helpers/compliance_checklist.py` still accepts boolean report maps; deep path is `compliance_validate.py`.

## NG check

- NG-1..5 respected (no plugin edits, no new canvas, user-governed fixes, no metamodel dump, Archi-only)
- No rework of v1.0–v1.3 cores beyond compliance hooks
