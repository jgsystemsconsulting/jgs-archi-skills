<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Contributing

This pack is MIT-licensed. Fork it, change skills for your own viewpoints,
and send a pull request if the change belongs upstream.

## Local setup

Python 3.10+, no extra packages.

```bash
python -m unittest discover -s tests -q
python helpers/validate_skill_mcp_refs.py
python scripts/check_release.py
```

Live MCP checks need Archi plus the JGS Archi Bridge. They are opt-in:
`python tests/live_mcp_smoke.py`.

## Pull requests

- One concern per PR.
- Keep skills consume-only toward jgs-archi-mcp. Do not copy ArchiMate
  metamodel tables into `SKILL.md`.
- User still governs architectural decisions (VISION NG-3).
- Match existing helper style: stdlib only.
- `skills/archi-viewpoint-select/SKILL.md` is digest-frozen; if you must
  change it, update `FROZEN` in `tests/test_specialist_contract.py`.

## Licence on contributions

By opening a pull request you license your contribution under the MIT
License in LICENSE, and you confirm you have the right to do so.
