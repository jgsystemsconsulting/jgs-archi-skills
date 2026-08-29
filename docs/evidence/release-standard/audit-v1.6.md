<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Release Repo Standard v1.9 audit: jgs-archi-skills at v1.6

Date: 2026-08-29. Auditor: `python ~/.zcode/skills/release-repo-standard/tools/audit.py --repo . --profile base --gh --links` plus a hand pass of the MANUAL list and every RR-S item the script does not model.

Posture for the v1.7.0 close-out (locked this run):

- Profile: Base + RR-S (skills pack). RR-S-08..15 treated as MUST (existing-pack carve-out waived).
- Build model: standalone.
- Licence: proprietary EULA (maintainer D1). SPDX `LicenseRef-JGSC-Proprietary`. CONTRIBUTING.md and CODE_OF_CONDUCT.md out of scope (RR-B-12).
- Catalogue (RR-B-19): N/A. JGSC does not maintain a public product catalogue. No pricing in the repo.
- Default install: flat `~/.zcode/skills/<skill>/` (workspace AGENTS.md). Namespaced Claude target ships alongside. Documented RR-S-03 letter deviation.

## Machine audit (v1.6 tree)

14 FAIL, 2 WARN, 7 PASS.

| ID | Result | Detail |
|----|--------|--------|
| RR-B-01 | FAIL | LICENSE missing |
| RR-B-02 | FAIL | COPYRIGHT missing; NOTICE missing |
| RR-B-03 | FAIL | 40 .py without header |
| RR-B-04 | FAIL | 40 .py without SPDX |
| RR-B-05 | FAIL | README missing Licence and Support headings |
| RR-B-07 | FAIL | SECURITY.md missing |
| RR-B-09 | FAIL | version mismatch: no RELEASE-INFO / CITATION / plugin.json; CHANGELOG top is `## Unreleased` then `## v1.6`, not `## [x.y.z]` |
| RR-B-10 | FAIL | RELEASE-INFO.txt missing |
| RR-B-15 | FAIL | no `scripts/check_release.py`, no `.github/workflows/validate.yml` |
| RR-B-21 | FAIL | About description empty, 0 topics, homepage unset |
| RR-B-28 | FAIL | em dash in 14 customer-facing docs (evidence READMEs, eval ITERATION notes, superpowers plan) |
| RR-B-31 | FAIL | CITATION.cff missing |
| RR-B-32 | FAIL | no `.github/ISSUE_TEMPLATE/bug_report.yml` or `config.yml` |
| RR-B-11 | PASS | tracked tree clean (local `.bak` is untracked) |
| RR-B-13 | PASS | .gitignore present |
| RR-B-14 | PASS | no leak sentinels |
| RR-B-25 | PASS | links resolve on the current tree |
| RR-B-27 | PASS | all commits use the jgsystemsconsulting noreply |
| RR-B-33 | PASS | no BOM in toml/json/yaml/cff |
| TMPL | PASS | no placeholder residue |
| RR-B-20 | WARN | Pages not enabled (private repo) |
| RR-B-23 | WARN | no branch protection (HTTP 403 on free private plan) |

`ci.yml` exists as the test workflow. It is not the RR-B-15 / RR-S-12 gate.

## Hand verification (MANUAL + RR-S)

| ID | Result | Notes |
|----|--------|-------|
| RR-B-00 | N/A | Standalone repo; no generated output to protect. |
| RR-B-06 | PARTIAL | README Usage is invoke-only. RR-S-05 `docs/skill-usage.md` is absent, so the skills-pack depth bar is unmet. |
| RR-B-08 | PARTIAL | CHANGELOG exists (Keep a Changelog-ish) but top entry is Unreleased / two-component `v1.6`. |
| RR-B-12 | PASS (posture) | No CONTRIBUTING / CoC / PR template. Correct for proprietary. |
| RR-B-16 | FAIL | No agent-install prompt block. |
| RR-B-17 | N/A | AGENTS.md present (workspace). llms.txt not required. |
| RR-B-18 | FAIL for 1.7.0 | Tags `v1.0`..`v1.6` exist (two-component, immutable). No `v1.7.0`. |
| RR-B-19 | N/A | Maintainer: no JGSC product catalogue. Record in release notes. |
| RR-B-20 | FAIL | No `docs/index.html`, no `docs/.nojekyll`. |
| RR-B-22 | FAIL for 1.7.0 | GitHub Release `v1.6` exists. No `v1.7.0`. |
| RR-B-23 | N/A (documented) | Protection API 403 on private free plan. SHOULD for a solo-maintained repo. Re-apply when public or Pro. |
| RR-B-24 | FAIL | No landing page, so no design-system / Playwright / SEO pass. |
| RR-B-26 | PASS | No ASCII diagrams in customer docs. README uses a table. |
| RR-B-28 prose | FAIL | Em dashes as above. No Technical Writer / ai-slop-cleaner record. |
| RR-B-29a | FAIL | No `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/marketplace.json`, or `gemini-extension.json`. |
| RR-B-29b | N/A | Proprietary EULA. Public directories that require OSS are ineligible. Human-only; agent must not claim submitted. |
| RR-B-30 | FAIL (unassessed at v1.6) | No landing page. Assessment for v1.7.0: one `docs/index.html`; extra HTML pages not justified. Deep content stays Markdown. |
| RR-S-01 | PASS | 13 `skills/<name>/SKILL.md` with `name` + `description`. |
| RR-S-02 | FAIL | `install.py` only. No `install.sh` / `install.ps1`. No `--dry-run`. |
| RR-S-03 | DEVIATION | Default dest is flat `~/.zcode/skills` (binding delivery form). Claude namespaced target absent. |
| RR-S-04 | FAIL | No SKILLS.md. |
| RR-S-05 | FAIL | No `docs/skill-usage.md`. |
| RR-S-06 | PASS | All skill dirs share the `archi-` prefix. |
| RR-S-07 | PASS | Deliberate absence of `docs/TOOL-REFERENCE.md`. Companion contract is `docs/MCP.md`. |
| RR-S-08 | FAIL | No marketplace manifests. |
| RR-S-09 | FAIL | No README badge cluster. |
| RR-S-10 | FAIL | No SECURITY.md. |
| RR-S-11 | FAIL | Two-component tags; no three-component 1.7.0 propagation set. |
| RR-S-12 | FAIL | No `validate.yml`. |
| RR-S-13 | FAIL | None of the 13 SKILL.md files contain `## When to use` or a Prerequisites / Requirements / `compatibility:` marker. |
| RR-S-14 | PASS | Frontmatter `name` is kebab-case and matches the directory; description non-empty. |
| RR-S-15 | FAIL | No `--agent` / `--list-agents`. No `docs/other-agents.md`. |
| RR-S-16 | N/A | No `kind: signpost` pack. |
| RR-M-* | N/A | Not an MCP-bridge product. Skills consume jgs-archi-mcp; they do not ship it. |

## v1.6 inventory (binding facts)

- 13 skills under `skills/`.
- 40 tracked first-party `.py` files, 372 tracked `.md` files.
- `install.py` flags: `--skills-root`, `--dest` (default `~/.zcode/skills`), `--link`.
- Tests: `python -m unittest discover -s tests -q` (existing suite; do not change skill semantics).
- `tests/test_specialist_contract.py` freezes SHA-256 of `skills/archi-viewpoint-select/SKILL.md`. Header / When-to-use edits must update that digest.
- Git identity already clean. Do not rewrite tags `v1.0`..`v1.6`.

## Close-out work this release must do

Legal files and SPDX headers; README / SECURITY / SKILLS.md / skill-usage / other-agents / CITATION / RELEASE-INFO / issue forms; `validate.yml` inline gate plus `scripts/check_release.py` (present for RR-B-15; CI must not execute it); installer `--dry-run` / `--agent` / wrappers / four host manifests; one landing page + Pages/About; em-dash sweep; tag and GitHub Release `v1.7.0`.
