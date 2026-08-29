<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Changelog

Milestone history for jgs-archi-skills. From v1.7.0 tags are three-component
semver (`vMAJOR.MINOR.PATCH`). Tags v1.0 through v1.6 remain as history.

## [1.7.0] - 2026-08-29

Release Repo Standard v1.9 (Base + RR-S). Proprietary EULA.

- LICENSE, COPYRIGHT, NOTICE, per-file SPDX headers
- SECURITY.md (private GitHub advisory; no email)
- README badge cluster, Install / Usage / Licence / Support, agent-install prompt
- SKILLS.md, docs/skill-usage.md, docs/other-agents.md, CITATION.cff, RELEASE-INFO.txt
- Bug-report issue form; blank issues off
- install.py `--dry-run`, `--agent`, `--list-agents`; install.sh / install.ps1
- Host manifests: `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/marketplace.json`, `gemini-extension.json`
- Default install stays flat `~/.zcode/skills` (documented RR-S-03 exception); Claude namespaced `jgs/` is first-class
- `.github/workflows/validate.yml` inline gate (does not execute repo code)
- docs/index.html landing page + GitHub Pages from master `/docs`
- Playwright screenshots at 1280px and 390px (untracked `.playwright-mcp/`)
- RR-B-19 catalogue N/A; RR-B-23 branch protection blocked on private free plan; RR-B-29b directory submissions N/A (proprietary); RR-B-30 one landing page
- Specialist run OS from the unreleased bucket: CREATE_PATH CP-G1..G7, disposition ledger, draft-first generation, layout footguns

## v1.6 (2026-08-28)

Eval loop to a senior quality bar, plus the first live end-to-end MCP
evidence.

- Frozen evaluation scenario (docs/eval/reference-scenario.md) and a
  GATES.md gate ledger; all 10 gates met with recorded exit codes and
  output fingerprints
- New stdlib checkers with unit tests: helpers/docs_coverage.py
  (meaningful documentation on every element and relationship) and
  helpers/layout_check.py (overlaps, containment, backward flow, layer
  grouping, bridge assessor hard counts)
- Compliance allowlist widened with live-verified element types and
  relationship patterns; the live bridge remains the legality oracle
- archi-layout skill now encodes the assess, layout, and route escalation
  that takes views to good or excellent ratings deterministically
- CREATE_PATH mandates relationship documentation (update-relationship)
  and pre-hand-back verification against the model
- Eval harness under docs/eval/: guarded MCP session wrapper, plan-driven
  builder with post-build verification, slice exporter, gate checks,
  verified-empty model reset
- Baseline scored 40 metamodel findings (offline allowlist gap) and one
  illegal edge the bridge rejected; iteration 1 and the fresh-model
  confirmation run are green on all instruments
- Evidence under docs/evidence/eval-loop/ (exports, findings, transcripts,
  rationale bundles, PNGs); live smoke evidence in live-archi-smoke

## v1.5 (2026-08-28)

Structured rationale depth (OBJ-6): rationale_schema bundle and section
checks, completion_summary_schema, deterministic nl_change_impact with
must-reuse IDs; CREATE_PATH plus documentation and orchestrator wiring;
offline evidence pack. 59 tests green. Known gap carried: live MCP E2E
(closed in v1.6).

## v1.4 (2026-08-28)

Compliance validation (OBJ-5): compliance_validate over model-slice
snapshots with explain-and-propose findings; offline allowlist fixture with
the MCP resources as live source of truth; CREATE_PATH plus model-qa and
specialist binding; pass and fail evidence slices. 46 tests green.

## v1.3 (2026-08-28)

Model coherence and reuse (OBJ-4): reuse registry, title-collapse-v1 naming
policy, naming_convention and reuse_inspect helpers, multi-view reuse
evidence, coherence wiring across specialists and CREATE_PATH.

## v1.2 (2026-08-28)

Full specialist skill set (OBJ-3): motivation, capability-strategy, business,
application, technology-physical, traceability, model-qa, layout,
documentation bodies plus orchestrator post-confirm dispatch; offline
specialist-suite evidence.

## v1.1 (2026-08-28)

Viewpoint selection (OBJ-2): intent axes matrix, viewpoint trace schema,
trace-table evidence.

## v1.0 (2026-08-28)

Foundations: orchestrator skill with elicitation and schema-checked view
plans, MCP consume-only contract, validate_skill_mcp_refs with the offline
inventory, install script, orchestrator smoke evidence.
