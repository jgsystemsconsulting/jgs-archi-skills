#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Offline checks for the self-model catalog. Stdlib only."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "helpers"))
from compliance_validate import validate_slice  # noqa: E402

CATALOG = ROOT / "tests" / "fixtures" / "self_model_catalog.json"
INVENTORY = ROOT / "docs" / "mcp" / "archi-bridge-inventory.json"

VIEWS = {
    "Self-Model Motivation",
    "Self-Model Application Cooperation",
    "Self-Model Business Process",
}


class T(unittest.TestCase):
    def setUp(self):
        self.cat = json.loads(CATALOG.read_text(encoding="utf-8"))
        self.inv = json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_three_views(self):
        names = {v["name"] for v in self.cat["views"]}
        self.assertEqual(names, VIEWS)

    def test_slice_validates(self):
        findings = validate_slice(
            {
                "elements": self.cat["elements"],
                "relationships": self.cat["relationships"],
                "view_usages": self.cat["view_usages"],
            }
        )
        self.assertEqual(findings, [], findings)

    def test_no_mcp_tool_element_names(self):
        tools = set(self.inv["tools"])
        names = {e["name"] for e in self.cat["elements"]}
        self.assertEqual(names & tools, set())

    def test_mcp_is_one_component(self):
        mcp = [
            e
            for e in self.cat["elements"]
            if e["name"] == "JGS Archi Bridge MCP"
        ]
        self.assertEqual(len(mcp), 1)
        self.assertEqual(mcp[0]["type"], "ApplicationComponent")

    def test_orchestrator_present(self):
        names = {e["name"] for e in self.cat["elements"]}
        self.assertIn("Archi Orchestrator", names)
        self.assertIn("View Plan Confirmation", names)

    def test_view_usages_cover_views(self):
        by_id = {e["id"]: e["name"] for e in self.cat["elements"]}
        expected = {
            (v["id"], eid, by_id[eid])
            for v in self.cat["views"]
            for eid in v["element_ids"]
        }
        got = {
            (u["view_id"], u["element_id"], u["name"])
            for u in self.cat["view_usages"]
        }
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
