#!/usr/bin/env bash
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
# Idempotent platform configuration (RR-B-21/23) via the gh CLI.
set -euo pipefail

OWNER="jgsystemsconsulting"
REPO="jgs-archi-skills"
DESCRIPTION="Agent-guided ArchiMate viewpoint creation in Archi via the JGS Archi Bridge MCP."
HOMEPAGE="https://jgsystemsconsulting.github.io/jgs-archi-skills/"
TOPICS=(archimate skills-pack zcode claude-code enterprise-architecture archi mcp)
CI_CHECK="integrity"
BRANCH="$(gh api "repos/$OWNER/$REPO" --jq .default_branch)"

gh repo edit "$OWNER/$REPO" --description "$DESCRIPTION"
[ -n "$HOMEPAGE" ] && gh repo edit "$OWNER/$REPO" --homepage "$HOMEPAGE"
for t in "${TOPICS[@]}"; do gh repo edit "$OWNER/$REPO" --add-topic "$t"; done

# Pages from default branch /docs. Private repos may 404 until public.
gh api -X POST "repos/$OWNER/$REPO/pages" \
  -f "source[branch]=$BRANCH" -f "source[path]=/docs" \
  >/dev/null 2>&1 || gh api -X PUT "repos/$OWNER/$REPO/pages" \
  -f "source[branch]=$BRANCH" -f "source[path]=/docs" \
  >/dev/null 2>&1 || echo "notice: Pages enablement skipped (private/free plan or already on)"

# Branch protection: SHOULD. Private free-plan repos return 403; record and continue.
if ! gh api -X PUT "repos/$OWNER/$REPO/branches/$BRANCH/protection" \
  --input - <<JSON
{
  "required_status_checks": {"strict": true, "contexts": ["$CI_CHECK"]},
  "enforce_admins": false,
  "required_pull_request_reviews": {"required_approving_review_count": 0},
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
then
  echo "notice: branch protection not applied (expected 403 on private free plan; RR-B-23 documented exception)"
fi

echo "verify:"
gh repo view "$OWNER/$REPO" --json description,homepageUrl,repositoryTopics
