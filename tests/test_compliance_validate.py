#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Unit tests for helpers/compliance_validate.py. Stdlib only."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "compliance_validate.py"
sys.path.insert(0, str(ROOT / "helpers"))
from compliance_validate import load_allowlist, validate_slice  # noqa: E402


def _pass_slice() -> dict:
    return {
        "elements": [
            {"id": "a1", "name": "Claims Clerk", "type": "BusinessRole", "abstraction": "business"},
            {
                "id": "p1",
                "name": "Handle Claim",
                "type": "BusinessProcess",
                "abstraction": "business",
            },
            {
                "id": "s1",
                "name": "Claim Intake",
                "type": "ApplicationService",
                "abstraction": "application",
            },
            {
                "id": "c1",
                "name": "Claims App",
                "type": "ApplicationComponent",
                "abstraction": "application",
            },
        ],
        "relationships": [
            {"id": "r1", "type": "Assignment", "source": "a1", "target": "p1"},
            {"id": "r2", "type": "Realization", "source": "c1", "target": "s1"},
            {"id": "r3", "type": "Serving", "source": "s1", "target": "p1"},
        ],
        "view_usages": [
            {"view_id": "v-biz", "element_id": "p1", "name": "Handle Claim"},
            {"view_id": "v-app", "element_id": "p1", "name": "Handle Claim"},
        ],
    }


class T(unittest.TestCase):
    def test_allowlist_loads(self):
        al = load_allowlist()
        self.assertIn("element_types", al)
        self.assertIn("permitted_patterns", al)

    def test_pass_slice(self):
        findings = validate_slice(_pass_slice())
        self.assertEqual(findings, [])

    def test_unknown_element_type(self):
        s = _pass_slice()
        s["elements"].append({"id": "x1", "name": "Weird", "type": "MagicBox"})
        findings = validate_slice(s)
        self.assertTrue(any(f["check_id"] == "element_type_known" for f in findings))
        f = next(f for f in findings if f["check_id"] == "element_type_known")
        self.assertIn("problem", f)
        self.assertIn("proposed_alternative", f)
        self.assertTrue(f["proposed_alternative"])

    def test_illegal_relationship_type(self):
        s = _pass_slice()
        s["relationships"].append(
            {"id": "bad", "type": "Teleportation", "source": "a1", "target": "p1"}
        )
        findings = validate_slice(s)
        self.assertTrue(
            any(f["check_id"] == "relationship_type_permitted" for f in findings)
        )
        f = next(f for f in findings if f["check_id"] == "relationship_type_permitted")
        self.assertIn("Teleportation", f["problem"])
        self.assertIn("proposed_alternative", f)

    def test_illegal_endpoints(self):
        s = _pass_slice()
        # Device Assignment BusinessProcess is not in fixture patterns
        s["elements"].append(
            {"id": "d1", "name": "Server", "type": "Device", "abstraction": "technology"}
        )
        s["relationships"].append(
            {"id": "bad2", "type": "Assignment", "source": "d1", "target": "p1"}
        )
        findings = validate_slice(s)
        self.assertTrue(
            any(f["check_id"] == "relationship_endpoints_valid" for f in findings)
        )
        f = next(f for f in findings if f["check_id"] == "relationship_endpoints_valid")
        self.assertTrue(f["proposed_alternative"])

    def test_abstraction_mismatch(self):
        s = _pass_slice()
        s["elements"][0]["abstraction"] = "technology"
        findings = validate_slice(s)
        self.assertTrue(
            any(f["check_id"] == "abstraction_level_consistent" for f in findings)
        )
        f = next(f for f in findings if f["check_id"] == "abstraction_level_consistent")
        self.assertIn("business", f["proposed_alternative"])

    def test_naming_conflict(self):
        s = _pass_slice()
        s["view_usages"] = [
            {"view_id": "v1", "element_id": "p1", "name": "Handle Claim"},
            {"view_id": "v2", "element_id": "p1", "name": "Claim Handling"},
        ]
        findings = validate_slice(s)
        self.assertTrue(
            any(f["check_id"] == "cross_view_naming_consistent" for f in findings)
        )
        f = next(f for f in findings if f["check_id"] == "cross_view_naming_consistent")
        self.assertTrue(f["problem"])
        self.assertTrue(f["proposed_alternative"])

    def test_cli_pass_fail(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            good = td_path / "good.json"
            bad = td_path / "bad.json"
            good.write_text(json.dumps(_pass_slice()), encoding="utf-8")
            b = _pass_slice()
            b["elements"].append({"id": "z", "name": "Z", "type": "NotAType"})
            bad.write_text(json.dumps(b), encoding="utf-8")
            g = subprocess.run(
                [sys.executable, str(H), str(good)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            self.assertEqual(g.returncode, 0, g.stdout + g.stderr)
            f = subprocess.run(
                [sys.executable, str(H), str(bad)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            self.assertEqual(f.returncode, 1)
            self.assertIn("proposed:", f.stdout)


if __name__ == "__main__":
    unittest.main()
