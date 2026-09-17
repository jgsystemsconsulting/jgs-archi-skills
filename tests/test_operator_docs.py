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


class TestZCodeWire(unittest.TestCase):
    def test_mcp_doc_has_zcode_attach(self):
        t = text("docs/MCP.md")
        self.assertIn("18090/mcp", t)
        self.assertIn("Attach from ZCode", t)
        self.assertIn("mcp.servers", t)

    def test_readme_links_zcode_attach(self):
        self.assertIn("docs/MCP.md#attach-from-zcode", text("README.md"))


class TestEntryLinks(unittest.TestCase):
    def test_readme_links_runbook(self):
        self.assertIn("docs/live-mcp-smoke.md", text("README.md"))

    def test_contributing_references_runbook(self):
        self.assertIn("docs/live-mcp-smoke.md", text("CONTRIBUTING.md"))


if __name__ == "__main__":
    unittest.main()
