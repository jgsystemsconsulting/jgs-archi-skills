<!--
Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
SPDX-License-Identifier: MIT
-->

# Distribution ledger · jgs-archi-skills

One row per place this product is, or could be, distributed and discovered
(`RR-B-36`, release-repo-standard). Statuses: `submitted` (URL + date, filed
by the maintainer), `in progress`, `deferred`, `deliberate N/A`, `planned`.
A non-submitted row MUST carry the decision and its date so the question
stays closed until its premises change. Revisit at every release: move
statuses, re-date reasons whose premises changed, never drop a row silently.
An agent never marks a row `submitted`; filing is the maintainer's action
and this ledger records it.

Last reviewed: 1.0.1 / 2026-09-24

## In-host marketplaces (manifests shipped, RR-B-29a / RR-S-08)

| Channel | Manifest | Status | Decision / reason | Date |
|---|---|---|---|---|
| Claude Code: `/plugin marketplace add jgsystemsconsulting/jgs-archi-skills` | `.claude-plugin/` | works at repo level | Manifest shipped; installable from the repo today. | 2026-09-24 |
| Claude Code: anthropics/claude-plugins-official directory | `.claude-plugin/` | planned | Curated directory, human web form. Submit after maintainer review of the listing copy. | 2026-09-24 |
| Cursor: cursor.com/marketplace/publish | `.cursor-plugin/` | planned | MIT licence qualifies. Manually reviewed form; maintainer action. | 2026-09-24 |
| OpenAI Codex CLI: Plugin Directory | `.agents/plugins/` | planned | Maintainer action. | 2026-09-24 |
| Gemini CLI: geminicli.com/extensions gallery | `gemini-extension.json` | planned | Auto-indexed crawler needs the `gemini-cli-extension` topic, the root manifest, and a tag. Manifest and tags are present; the topic set currently carries `gemini-cli` but not `gemini-cli-extension`. Add the topic to trigger the daily crawl. | 2026-09-24 |

## Web directories & catalogues

| Channel | Artifact | Status | Decision / reason | Date |
|---|---|---|---|---|
| GitHub About + topics + Release | `scripts/configure_repo.sh` | in progress | Applied at publish (RR-B-21): description, homepage, 13 topics including one per host. Topic set re-checked while writing this ledger. | 2026-09-24 |
| Org catalogue (labs.jgsystemsconsulting.com) | site entry | planned | RR-B-19 product entry; links install + licensing. Maintainer adds at next site update. | 2026-09-24 |
| Community lists: awesome-archimate, awesome-claude-skills, awesome-claude-code | PR entry | deferred | MIT qualifies, but all three lists are discretionary and manually reviewed. Revisit after first external usage signal rather than at first release. | 2026-09-24 |

## Feedback-loop notes

- MCP aggregator directories (RR-M-07b) are deliberate N/A for this pack:
  the skills drive the JGS Archi Bridge MCP but are not themselves an MCP
  server. Directory submissions belong to the `jgs-archi-mcp` bridge repo
  and its own ledger. 2026-09-24.
- `RR-S-17` (in-pack feedback utility skill) is not shipped here. Feedback
  flows through the RR-B-32 issue forms (bug + improvement) named in the
  README. Revisit if external adoption grows. 2026-09-24.
