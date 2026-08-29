---
status: passed
milestone: v1.5
seed: SEED-006
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Milestone Audit — v1.5 Structured rationale depth

**Date:** 2026-08-28
**Seed:** SEED-006 / OBJ-6
**Verdict:** passed

## Intent

OBJ-6: Each significant view carries structured rationale (purpose, stakeholders and concerns, viewpoint, questions answered, assumptions, decisions, exclusions, open questions) recorded in the model via MCP, and users can request natural-language changes that regenerate views without damaging the shared model, ending with a completion summary.

## Phases

| Phase | Goal | Verification |
|-------|------|--------------|
| 19 | rationale_schema depth + completion_summary_schema + nl_change_impact + tests | passed |
| 20 | CREATE_PATH OBJ-6 + documentation/orchestrator binding | passed |
| 21 | Offline rationale/NL-change evidence + regression lock | passed |

## Requirements coverage (RAT-01..10)

All 10 v1.5 requirements mapped and complete:

- RAT-01..04 helpers + multi-view + NL impact + completion summary + tests
- RAT-05..07 contract and skill binding
- RAT-08..10 evidence + freeze + no core rework

## Cross-phase integration

- `helpers/rationale_schema.py` deepens empty-section + bundle validation; thin `missing_headings` retained
- `helpers/completion_summary_schema.py` enforces RATE-03 required blocks
- `helpers/nl_change_impact.py` returns affected views + must_reuse_element_ids (deterministic)
- CREATE_PATH documents draft/validate, MCP documentation-field write, NL impact gate, completion summary
- archi-documentation binds helpers; Step 4 requires impact plan before regenerate
- archi-orchestrator consumes completion summary and optional NL-change loop
- Evidence pack: `docs/evidence/rationale-nl-change-offline/`
- viewpoint-select SHA256 remains v1.1 freeze `01ad2cc359bb1a4e42a26d8eda383b394fc73a6409373736eba1c5bd6caf94ea`
- MCP-ref validator clean; 59 unit tests green

## Gaps / deferred

- Live Archi MCP E2E still deferred (EVID-LIVE-*)
- Nested Agent unavailable this host; gates ran inline (degraded tier)
- LLM-based semantic NL parsing inside helpers remains out of scope (deterministic tokens only)
- Live MCP write of rationale into documentation fields with transcript remains EVID-LIVE-03

## Security

No blocking findings. Stdlib-only helpers; no secrets; offline markdown/JSON only; skills remain non-mutating until View Plan approval; NL changes never auto-applied (NG-3).

## Golden-path probe (adversarial)

- Empty-section rationale → exit 1 (`empty_section`)
- Missing-section rationale → exit 1
- Valid multi-view bundle → exit 0
- Incomplete completion summary → exit 1
- NL note matching invoice views → must_reuse includes shared `el-customer`; hosting-only element excluded
- Backtick skill name false-positive avoided in orchestrator prose

## Audit decision

**passed** — milestone intent met offline; ready for complete-milestone checkpoint.
