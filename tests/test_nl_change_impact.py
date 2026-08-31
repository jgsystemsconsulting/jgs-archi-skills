#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Unit tests for helpers/nl_change_impact.py. Stdlib only."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "nl_change_impact.py"
sys.path.insert(0, str(ROOT / "helpers"))
from nl_change_impact import plan_impact  # noqa: E402

INVENTORY = {
    "views": [
        {
            "id": "v-biz",
            "name": "Invoice As-Is Business",
            "keywords": ["invoice", "business", "process"],
        },
        {
            "id": "v-app",
            "name": "Invoice Application Support",
            "keywords": ["invoice", "application", "erp"],
        },
        {
            "id": "v-tech",
            "name": "Hosting Baseline",
            "keywords": ["hosting", "infra"],
        },
    ],
    "elements": [
        {
            "id": "el-customer",
            "name": "Customer",
            "shared": True,
            "view_ids": ["v-biz", "v-app"],
        },
        {
            "id": "el-invoice-proc",
            "name": "Handle Invoice",
            "shared": False,
            "view_ids": ["v-biz"],
        },
        {
            "id": "el-host",
            "name": "App Host",
            "shared": False,
            "view_ids": ["v-tech"],
        },
    ],
}


class T(unittest.TestCase):
    def test_match_invoice_views(self):
        plan = plan_impact(
            "Please regenerate the invoice business view with clearer stalls",
            INVENTORY,
        )
        ids = {v["id"] for v in plan["affected_views"]}
        self.assertIn("v-biz", ids)
        self.assertNotIn("v-tech", ids)
        self.assertIn("el-customer", plan["must_reuse_element_ids"])
        self.assertNotIn("el-host", plan["must_reuse_element_ids"])

    def test_explicit_view_id(self):
        plan = plan_impact("Update only v-app labels", INVENTORY)
        ids = {v["id"] for v in plan["affected_views"]}
        self.assertEqual(ids, {"v-app"})
        self.assertIn("el-customer", plan["must_reuse_element_ids"])

    def test_no_match(self):
        plan = plan_impact("change the color scheme only", INVENTORY)
        self.assertEqual(plan["affected_views"], [])
        self.assertEqual(plan["must_reuse_element_ids"], [])
        self.assertTrue(plan["notes"])

    def test_cli(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            note = d / "note.txt"
            inv = d / "inv.json"
            note.write_text("regenerate Invoice Application Support", encoding="utf-8")
            inv.write_text(json.dumps(INVENTORY), encoding="utf-8")
            r = subprocess.run(
                [sys.executable, str(H), str(note), str(inv)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            self.assertEqual(r.returncode, 0)
            data = json.loads(r.stdout)
            self.assertIn("must_reuse_element_ids", data)
            self.assertIn("el-customer", data["must_reuse_element_ids"])


if __name__ == "__main__":
    unittest.main()
