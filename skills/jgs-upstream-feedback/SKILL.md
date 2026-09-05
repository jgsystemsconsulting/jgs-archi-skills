---
name: jgs-upstream-feedback
description: "File an agnostic pack or MCP-contract issue on GitHub after one user yes. Trigger: /jgs-upstream-feedback"
argument-hint: "[optional gap note]"
---
<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# jgs-upstream-feedback

## When to use

User-invoked, or dispatched by a pack orchestrator, when a shipped skill or MCP contract blocked an outcome that any user of the pack would hit. Not a modelling specialist. Does not talk to Archi.

## Prerequisites

GitHub CLI (`gh`) is optional. Logged-in `gh` files the issue; otherwise this skill prints a pre-filled GitHub new-issue URL. Python is not required.

## Hard rules

1. File nothing until the user says yes to the exact draft, unless already_approved is true and the body is unchanged.
2. Skill-meta only. No element names, model paths, viewpoint content, tokens, or credentials.
3. Origin only if any user would hit this. Local model, org, install, or governance pain stays local.
4. No bot token. File as the logged-in user.
5. Never open a pull request against the MCP plugin. Never patch plugin source.
6. allow_pr stays false unless the user asked for a patch and the current workspace is a clone of the skill pack origin.
7. Do not phone home. Do not write a lessons file. Do not stall a modelling session on login.

## Caller payload

Orchestrator or this skill (direct invoke) must have:

- kind: skill-gap or mcp-gap or bug
- issues_repo: owner/name
- title: short, no model nouns
- body: the markdown template below, already filled
- labels: list, or empty
- allow_pr: false unless the PR gate below is fully met
- already_approved: true only when the caller already showed this exact draft and the user said yes

Direct invoke with no payload: ask what to report, apply origin-vs-local, classify, then fill the payload. Default issues_repo is jgsystemsconsulting/jgs-archi-skills. If kind is mcp-gap, issues_repo is jgsystemsconsulting/jgs-archi-mcp. already_approved stays false.

## Body template (skill-meta)

Use this exact markdown as the gh issue body and as the URL body query. Do not add extra sections.

Skill: <skill or unknown>
Step: <orchestrator step or specialist name>
Outcome blocked: <one sentence>
Proposed change: <one sentence>
Pack version: <from RELEASE-INFO.txt or unknown>
Agent host: <zcode or claude or other or unknown>
MCP tool or resource: <name only, or none>

This report contains no model content, tokens, or credentials.

## Origin vs local

Keep only if the proposed change belongs in shipped skill text, a helper, or the MCP contract, and every other user of the pack would hit the same hole.

Stay silent on GitHub (or stop, on direct invoke) when the pain is their model, org names, MCP URL, OS path, a local skill edit, a governance no, or ops (bridge not running, wrong model open).

If you cannot state the gap without their nouns, or cannot say "any user would hit this," do not file. On direct invoke, ask that sentence once. No means stop.

After redact, strip leftover proper nouns. If proposed_change is "add an element for their capability," abort.

Hygiene line in every body: This report contains no model content, tokens, or credentials.

## Draft the user must see

If already_approved is true and the body matches what they approved, skip this ask and go to File on yes.

Otherwise show title, issues_repo, and body. Then ask:

Raise this against <issues_repo>?

Yes / no / edit first

No: stop. Do not ask again this session for that gap.
Edit: revise, show again, file only on a later yes.

## File on yes

1. Run gh auth status.
2. If authenticated, run gh issue create with repo, title, body, and optional label flags, as this user. Print the issue URL. Stop.
3. If not authenticated, or gh errors (network, 403, 422), do not retry-spam. Open or print:

https://github.com/<owner>/<name>/issues/new?title=<urlencoded>&body=<urlencoded>&labels=<urlencoded>

Omit the template query parameter. If the URL would be too long, truncate body to the skill-meta fields plus the hygiene line and say the rest is in chat.

Never invent labels on the MCP tracker. If unsure, omit labels.

## PR gate

Default allow_pr is false. Do not offer a PR on the suggestion prompt.

All of these must be true before a PR: user asked for a patch; current workspace is a git clone of the skill pack origin (not an install.py copy); gap passed origin-vs-local; change is a tight skill or helper edit.

Then show the exact diff, wait for yes, branch, commit, gh pr create as them. One concern. Consume-only. No language tables copied into SKILL.md.

Refuse PR when there is no clone, the tree is dirty with unrelated work, the target is the MCP plugin, or the files live under the installed skills directory. Tell them to clone the pack repo and ask again. Do not git init that folder.

## Done

Print the issue URL (or the pre-filled URL). Stop. No extra "anything else?"
