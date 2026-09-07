#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Orchestrator skill names the Done When stop-rule contract. No MCP."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "archi-orchestrator" / "SKILL.md"


class OrchestratorDoneWhenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL.read_text(encoding="utf-8")

    def test_stop_rule_tokens(self) -> None:
        self.assertIn("named-deliverable", self.text)
        self.assertIn("outcome-until", self.text)

    def test_done_when_heading(self) -> None:
        self.assertIn("## Done When", self.text)

    def test_override_tokens(self) -> None:
        self.assertIn("`only:`", self.text)
        self.assertIn("`just:`", self.text)
        self.assertIn("`until:`", self.text)
        self.assertIn("`goal:`", self.text)

    def test_asks_one_question_when_ambiguous(self) -> None:
        lowered = self.text.lower()
        self.assertIn("neither is clear, ask one question", lowered)

    def test_ten_required_headings(self) -> None:
        self.assertIn("ten required", self.text.lower())
        self.assertNotIn("nine required", self.text.lower())

    def test_hand_off_fields(self) -> None:
        self.assertIn("stop_rule", self.text)
        self.assertIn("pass_checks", self.text)
        self.assertIn("must_not", self.text)

    def test_exit_after_one_full_pass(self) -> None:
        self.assertIn("Do not re-dispatch", self.text)


if __name__ == "__main__":
    unittest.main()
