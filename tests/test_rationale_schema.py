#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Unit tests for helpers/rationale_schema.py. Stdlib only."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "rationale_schema.py"
sys.path.insert(0, str(ROOT / "helpers"))
from rationale_schema import (  # noqa: E402
    REQUIRED,
    missing_headings,
    validate_bundle,
    validate_rationale,
)

HEADS = list(REQUIRED)
VALID = "\n".join(["## %s\nx" % h for h in HEADS])


class T(unittest.TestCase):
    def _run(self, body, extra=None):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(body)
            path = fh.name
        try:
            cmd = [sys.executable, str(H), path]
            if extra:
                cmd.extend(extra)
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_ok_cli(self):
        self.assertEqual(self._run(VALID).returncode, 0)

    def test_missing_cli(self):
        self.assertEqual(self._run("## Purpose\nx").returncode, 1)

    def test_empty_section(self):
        body = "\n".join(
            ["## %s\n%s" % (h, "" if h == "Decisions" else "x") for h in HEADS]
        )
        findings = validate_rationale(body)
        self.assertTrue(any(f["check_id"] == "empty_section" for f in findings))
        r = self._run(body)
        self.assertEqual(r.returncode, 1)

    def test_missing_headings_api(self):
        self.assertIn("Decisions", missing_headings("## Purpose\nx"))

    def test_bundle_json(self):
        good = {"id": "v1", "text": VALID}
        bad = {"id": "v2", "text": "## Purpose\nx"}
        findings = validate_bundle({"views": [good, bad]})
        self.assertTrue(any(f.get("view_id") == "v2" for f in findings))
        self.assertFalse(
            any(
                f.get("view_id") == "v1" and f.get("severity", "error") != "warn"
                for f in findings
            )
        )

    def test_bundle_dir_cli(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "view-a.md").write_text(VALID, encoding="utf-8")
            (d / "view-b.md").write_text("## Purpose\nx\n", encoding="utf-8")
            r = subprocess.run(
                [sys.executable, str(H), "--bundle", str(d)],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            self.assertEqual(r.returncode, 1)

    def test_json_flag(self):
        r = self._run("## Purpose\nx", extra=["--json"])
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        self.assertIn("findings", data)


if __name__ == "__main__":
    unittest.main()
