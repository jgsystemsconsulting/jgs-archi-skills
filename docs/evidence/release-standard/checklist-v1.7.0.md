<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# §5 checklist: jgs-archi-skills v1.7.0

Release Repo Standard v1.9, profile Base + RR-S, standalone, proprietary EULA.
Date: 2026-08-29.

| # | Item | Result | Evidence / reason |
|---|------|--------|-------------------|
| 1 | Release gate exits 0 | PASS | `python scripts/check_release.py` prints `release gate: PASS`. CI: `.github/workflows/validate.yml` inlines the same checks and does not execute repo code. |
| 2 | All applicable RR-B MUSTs | PASS | Closed in this release. See audit-v1.6.md for the v1.6 gap list. |
| 3 | All RR-S MUSTs (08..15 treated as MUST) | PASS | Installer, SKILLS.md, skill-usage, badges, SECURITY.md, validate.yml, When-to-use + Prerequisites on all 13 skills, four host manifests, other-agents.md. |
| 4 | Leak checks | PASS | Required files present; no forbidden paths; no leak sentinels; python headers present. |
| 5 | Version agreement 1.7.0 | PASS | CHANGELOG top `[1.7.0]`, RELEASE-INFO, CITATION.cff, both plugin.json, gemini-extension.json, README badge, landing REV + JSON-LD softwareVersion. |
| 6 | Agent-install prompt | PASS | README labelled block embeds repo URL, v1.7.0, and `python install.py`. |
| 7 | Tagged release | PASS (this ship) | Intended tag `v1.7.0` in RELEASE-INFO. Historical tags v1.0..v1.6 left immutable. |
| 8 | Catalogue RR-B-19 | N/A | Maintainer: JGSC does not maintain a public product catalogue. No pricing in the repo. |
| 9 | Multi-agent install RR-S-15 | PASS | `install.py --list-agents` / `--agent` / `--dry-run`. Default zcode flat. README + docs/other-agents.md. |
| 10 | Landing page RR-B-20 | PASS (files); Pages N/A until public | `docs/index.html` + `docs/.nojekyll` shipped. Self-contained, self-hosted fonts, title/description/canonical/OG, what-it-is, skill chain, agents, install, first-run. GitHub Pages create returned HTTP 422: "Your current plan does not support GitHub Pages for this repository" while the repo is private on the free plan. Homepage is set to the intended Pages URL. Enable Pages from `master:/docs` when the repo is public or on Pro. |
| 11 | About metadata RR-B-21 | PASS (script) | `scripts/configure_repo.sh` sets description, homepage, 7 topics. |
| 12a | Marketplace manifests RR-B-29a | PASS | `.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/marketplace.json`, `gemini-extension.json`. `claude plugin validate` passed. |
| 12b | Directory submissions RR-B-29b | N/A | Proprietary EULA. OSS-only directories ineligible. Human-only; not claimed done. |
| 12a MCP | RR-M-07 | N/A | Not an MCP-bridge product. |
| 13 | GitHub Release RR-B-22 | PASS (this ship) | Notes from CHANGELOG 1.7.0. |
| 14 | Branch protection RR-B-23 | N/A | HTTP 403 on private free plan. SHOULD for a solo-maintained repo. Re-apply when public or Pro. |
| 15 | Landing brand RR-B-24 | PASS | Design-system tokens, `:focus-visible`, `prefers-reduced-motion`, no emoji icons, grids collapse at 860px. Playwright screenshots: `.playwright-mcp/landing-desktop-1280.png`, `.playwright-mcp/landing-mobile-390.png` (untracked). Title 50 chars, description 149. Zero em dashes in `docs/index.html`. |
| 16 | Link integrity RR-B-25 | PASS | `audit.py --links` on the tree. Re-check after publish. |
| 17 | Docs presentation RR-B-26 | PASS | README mermaid for the skill chain. No ASCII diagrams. Tables and headings. |
| 18 | De-slop RR-B-28 | PASS | Technical Writer on README, skill-usage, other-agents, landing copy, CHANGELOG 1.7.0. Em-dash sweep: `grep -rl` over README/docs/CHANGELOG empty. `prose_check.py` remaining hits are HTML-comment `-->` false positives and installer flag `--dry-run`. |
| 19 | Commit identity RR-B-27 | PASS | `git log --all --format='%ae %ce'` only jgsystemsconsulting noreply. |
| 19a | Multi-page RR-B-30 | PASS | Assessment: 13 skills, MCP.md, CREATE_PATH, CHANGELOG, EULA, eval evidence. Maintainer default (recommended): one landing page. Extra HTML pages not justified. Deep content stays Markdown. |
| 20 | Signpost RR-S-16 | N/A | No signpost pack. |
| 21 | RR-R | N/A | Not a research instrument. |
| 22 | README spot-check | PASS | Customer tone, install/usage, no internal URLs. |
| 23 | CITATION.cff RR-B-31 | PASS | CFF 1.2.0, org author, version 1.7.0. |
| 24 | Bug-report RR-B-32 | PASS | bug_report.yml + config.yml; blank issues off; advisory link; hygiene required. |
| 25 | BOM RR-B-33 | PASS | audit.py BOM scan clean. |
| 26 | RR-M-08 | N/A | Not an MCP-bridge product. |

RR-S-03 letter deviation: default install target is flat `~/.zcode/skills` because workspace AGENTS.md binds that delivery form. Namespaced Claude `jgs/` ships as `--agent claude`.

RR-S-07: `docs/TOOL-REFERENCE.md` deliberately absent; companion contract is `docs/MCP.md`.
