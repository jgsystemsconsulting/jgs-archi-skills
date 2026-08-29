<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Using the pack with other agents

Skills follow the open [Agent Skills](https://agentskills.io) `SKILL.md`
format. Some agents read that format natively (the skill folder is copied
unchanged). Others need a format transform.

`install.py` handles both. Default agent is **zcode** (flat
`~/.zcode/skills/<skill>/`). That default is the binding delivery form for
this pack (workspace AGENTS.md). The namespaced Claude Code target
(`$CLAUDE_CONFIG_DIR/skills/jgs/<skill>/`) ships as a first-class `--agent
claude` path. This is a documented letter deviation from RR-S-03, not a
silent one.

```bash
python install.py --list-agents
python install.py --agent claude --dry-run
python install.py --agent all
python install.py --agent cursor
```

## Per-agent targets

| Agent | `--agent` | Format | Default target |
|-------|-----------|--------|----------------|
| ZCode | `zcode` (default) | native (folder) | `~/.zcode/skills/<skill>/` |
| Claude Code | `claude` | native (folder) | `~/.claude/skills/jgs/<skill>/` (honours `$CLAUDE_CONFIG_DIR`) |
| OpenClaw | `openclaw` | native (folder) | `~/.openclaw/skills/jgs/<skill>/` |
| GitHub Copilot CLI | `copilot` | native (folder) | `~/.copilot/skills/jgs/<skill>/` |
| OpenAI Codex CLI | `codex` | native (folder) | `~/.agents/skills/jgs/<skill>/` |
| Gemini CLI | `gemini` | extension | `~/.gemini/extensions/jgs-<skill>/` |
| Cursor | `cursor` | transform (project rule) | `./.cursor/rules/<skill>.mdc` (project-local) |

`--agent all` covers the user-global agents (zcode, claude, openclaw, copilot,
codex, gemini). Cursor is project-local: run `--agent cursor` in the repo you
want rules in.

## Native vs transform

Native agents get the whole skill folder (`SKILL.md` plus any supporting
files). Transform agents (Cursor) get `SKILL.md` inlined into one `.mdc`
rule. Gemini gets a small extension directory with `GEMINI.md` plus
`gemini-extension.json`.

Existing `--dest` and `--link` flags still work. `--dest` overrides the dest
root for the chosen agent. For `zcode`, `--dest DIR` writes `DIR/<skill>/`,
which is what CI packaging smoke uses.
