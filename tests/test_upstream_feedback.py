#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Structural checks for the upstream feedback loop. No live GitHub."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "jgs-upstream-feedback" / "SKILL.md"
ORCH = ROOT / "skills" / "archi-orchestrator" / "SKILL.md"
FORM = ROOT / ".github" / "ISSUE_TEMPLATE" / "skill_improvement.yml"
CONFIG = ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml"
VALIDATOR = ROOT / "helpers" / "validate_skill_mcp_refs.py"
INVENTORY = ROOT / "docs" / "mcp" / "archi-bridge-inventory.json"


class UpstreamFeedbackTests(unittest.TestCase):
    def test_skill_exists_with_frontmatter(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"), "missing YAML frontmatter")
        self.assertIn("name: jgs-upstream-feedback", text)
        self.assertIn("argument-hint:", text)

    def test_skill_has_one_yes_loop(self) -> None:
        text = SKILL.read_text(encoding="utf-8").casefold()
        for needle in (
            "gh auth status",
            "gh issue create",
            "issues/new",
            "yes / no / edit",
        ):
            self.assertIn(needle, text, msg=needle)

    def test_skill_fail_closed_and_gates(self) -> None:
        text = SKILL.read_text(encoding="utf-8").casefold()
        for needle in (
            "any user would hit this",
            "no bot token",
            "never",
            "pull request against the mcp",
            "allow_pr",
            "skill-meta",
            "already_approved",
        ):
            self.assertIn(needle, text, msg=needle)

    def test_skill_has_no_archimate_uris(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertNotIn("archimate://", text)

    def test_validator_ok_on_feedback_skill_alone(self) -> None:
        self.assertTrue(SKILL.is_file(), "utility skill missing")
        proc = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--inventory",
                str(INVENTORY),
                "--skills-root",
                str(SKILL.parent.parent),
            ],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        isolated = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--inventory",
                str(INVENTORY),
                "--skills-root",
                str(SKILL.parent),
            ],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(isolated.returncode, 0, isolated.stdout + isolated.stderr)

    def test_orchestrator_dispatches_filer(self) -> None:
        text = ORCH.read_text(encoding="utf-8")
        self.assertIn("jgs-upstream-feedback", text)
        folded = text.casefold()
        self.assertIn("any user would hit this", folded)
        self.assertIn("raise this against", folded)

    def test_skill_improvement_form(self) -> None:
        text = FORM.read_text(encoding="utf-8")
        self.assertIn("name: Skill improvement", text)
        for field_id in ("skill", "outcome_blocked", "proposed_change", "version"):
            self.assertIn(f"id: {field_id}", text)
        self.assertIn("no model content", text.casefold())

    def test_config_points_at_mcp_tracker(self) -> None:
        text = CONFIG.read_text(encoding="utf-8")
        self.assertIn("jgsystemsconsulting/jgs-archi-mcp", text)
        self.assertIn("blank_issues_enabled: false", text)


if __name__ == "__main__":
    unittest.main()
