# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Operator docs coverage: live-smoke runbook, ZCode MCP wire, entry links."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(name):
    return (ROOT / name).read_text(encoding="utf-8")


class TestLiveSmokeRunbook(unittest.TestCase):
    def test_runbook_exists_with_operator_facts(self):
        t = text("docs/live-mcp-smoke.md")
        self.assertIn("JGS Skills Live Smoke", t)
        self.assertIn("python tests/live_mcp_smoke.py", t)
        self.assertIn("Approval Mode", t)

    def test_runbook_covers_ctrl_n_footgun(self):
        t = text("docs/live-mcp-smoke.md")
        self.assertIn("MODEL_OPENED", t)


if __name__ == "__main__":
    unittest.main()
