#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Tests for helpers.viewpoint_selection_matrix."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helpers" / "viewpoint_selection_matrix.py"
sys.path.insert(0, str(ROOT / "helpers"))

import viewpoint_selection_matrix as vsm  # noqa: E402


class TestMatrix(unittest.TestCase):
    def test_list_keys(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(HELPER), "--list"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        keys = {c["key"] for c in data["candidates"]}
        self.assertIn("motivation", keys)
        self.assertIn("application-structure", keys)
        self.assertGreaterEqual(len(keys), 8)

    def test_rank_multi_stakeholder(self) -> None:
        intent = {
            "stakeholders": ["executive", "enterprise-architect"],
            "concerns": ["capabilities", "investment", "alignment"],
            "purpose": "decide",
            "abstraction": "overview",
        }
        result = vsm.rank(intent)
        self.assertTrue(result["standard_fit"])
        top_keys = [r["key"] for r in result["ranked"][:3]]
        self.assertTrue(
            "capability-map" in top_keys or "layered" in top_keys,
            top_keys,
        )
        scores = [r["score"] for r in result["ranked"]]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_malformed_exits_nonzero(self) -> None:
        bad = json.dumps({"stakeholders": []})
        proc = subprocess.run(
            [sys.executable, str(HELPER)],
            input=bad,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing required fields", proc.stderr)

    def test_missing_file_exit_2(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(HELPER), str(ROOT / "no-such-intent.json")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)

    def test_cli_sample_file(self) -> None:
        intent = {
            "stakeholders": ["application-architect", "developer"],
            "concerns": ["applications", "components", "interfaces"],
            "purpose": "design",
            "abstraction": "detail",
        }
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(intent, f)
            path = f.name
        try:
            proc = subprocess.run(
                [sys.executable, str(HELPER), path, "--top", "5"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            self.assertEqual(data["ranked"][0]["key"], "application-structure")
        finally:
            Path(path).unlink(missing_ok=True)

    def test_no_metamodel_catalog_words(self) -> None:
        src = HELPER.read_text(encoding="utf-8")
        forbidden = [
            "Assignment relationship",
            "Serving relationship",
            "element-type catalog",
            "BusinessActor",
            "ApplicationComponent",
        ]
        for word in forbidden:
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()
