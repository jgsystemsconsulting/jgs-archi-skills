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

## In-session issues

The orchestrator may offer to file an agnostic pack defect. Yes runs
`/jgs-upstream-feedback` as you (gh if logged in, else a pre-filled GitHub URL).
Local model pain is not an upstream issue.

MCP-contract holes file on jgsystemsconsulting/jgs-archi-mcp as issues.
Do not send plugin pull requests from this pack.

Skill pull requests still need a clone of this repo and one concern per PR.

## Pull requests

- One concern per PR.
- Keep skills consume-only toward jgs-archi-mcp. Do not copy ArchiMate
  metamodel tables into `SKILL.md`.
- Content-quality rules live in `docs/MODELLING_CONVENTIONS.md`. Do not fork a
  second naming chapter inside a specialist SKILL.md.
- User still governs architectural decisions.
- Match existing helper style: stdlib only.
- `skills/archi-viewpoint-select/SKILL.md` is digest-frozen; if you must
  change it, update `FROZEN` in `tests/test_specialist_contract.py`.
- New orchestrator shortcuts go in `docs/prompts/` as `pNN-slug.md` with the
  headings `helpers/prompt_card_schema.py` requires. Run
  `python helpers/prompt_card_schema.py docs/prompts` and
  `python -m unittest tests.test_prompt_catalog -q`.

## Licence on contributions

By opening a pull request you license your contribution under the MIT
License in LICENSE, and you confirm you have the right to do so.
