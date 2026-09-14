<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Changelog

Single-source history for jgs-archi-skills. Tags are three-component semver
(`vMAJOR.MINOR.PATCH`).

## [Unreleased]

- Papers and adoption pack lands in the tracked tree: `docs/papers/` markdown
  set, `docs/papers/landing.md`, both IEEE PDFs, both TeX sources, `soam.bib`,
  and the two build scripts, so README and companion links resolve on GitHub.
- `docs/papers/ieee/build.sh` and `build-long.sh` now call `pdflatex` and
  `bibtex` from PATH; the machine-local MiKTeX absolute paths are gone.
- TeX debris (`*.aux`, `*.bbl`, `*.blg`, `*.log`, `*.out` under
  `docs/papers/ieee/`), the `_preview/` scratch directory, both dated preview
  PDFs, and `docs/images/drafts/` are gitignored; the `soam-workshop.md`
  leftover and the internal FCL triage log are deleted, and the pack README
  drops the workshop link.
- `docs/papers/why-soam.md` honesty edit is now tracked: invoice-to-cash is
  first-contact only, the IEEE walks are the mill and the range, the TMS
  starter stays unexecuted.

## [1.0.1] - 2026-09-08

The orchestrator now has a goal path. Same `/archi-orchestrator`. Start the
invoke with `goal:` or `until:` to lock outcome-until: keep going until the
signed outcome is visible on the model. Named deliverable stays the default.
Landing How you ask and skill-usage document both stop rules. Prompt card p15
is the copy-paste `until:` job.

- Done When on the View Plan: named-deliverable or outcome-until, signed pass
  checks, and MUST NOT. Approve signs the exit.
- Companion mill walk page (`docs/hatherley.html`) with five Hatherley Plate
  view exports. Author-run frozen brief. Refuse at the View Plan gate is the
  method.
- Companion GitHub Pages hub (altitudes, agents, how you ask, why, eval,
  examples, install) plus a six-layer guide written for a technology architect
- Hub names every install host (ZCode, Claude Code, Cursor, Gemini CLI,
  OpenAI Codex, GitHub Copilot CLI) and points pack feedback plus Discussions
  as the public room
- Companion Engagement page: standup, named viewpoint packages, and
  enablement, with no rate card on the page

## [1.0.0] - 2026-08-31

First public release. Agent-guided ArchiMate viewpoint creation in Archi via
the JGS Archi Bridge MCP.

- Orchestrator plus twelve specialists plus the jgs-upstream-feedback utility
- User-governed View Plan confirmation
- Shared CREATE_PATH contract with run gates CP-G1 through CP-G7, candidate
  disposition ledger, evidence line, layout footguns, draft first generation
- JGS modelling house style (`docs/MODELLING_CONVENTIONS.md`) with optional
  documentation evidence checks, aspect naming hints, and folder-placement
  checks. Language catalogs stay on the Archi Bridge MCP
- Starter prompt pack for `/archi-orchestrator`: 14 frozen use-case cards under
  `docs/prompts/`, schema checker `helpers/prompt_card_schema.py`
- Archify diagrams on Pages: cooperation architecture and modelling-run
  workflow under `docs/diagrams/`
- Offline helpers and unittest suite (stdlib only); live MCP smoke is opt-in
- Release Repo Standard (Base + RR-S): LICENSE, SECURITY.md, installers, host
  manifests, GitHub Pages landing page, CI integrity gate
- Licence-enquiry page linked from the landing page, README, and GitHub
  Release notes
- Paste-ready agent install prompt in the README covering both the Archi
  Bridge MCP and this skill pack. Same text in the Bridge README.
