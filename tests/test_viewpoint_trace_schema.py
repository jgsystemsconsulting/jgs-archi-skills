#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Tests for helpers.viewpoint_trace_schema."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helpers" / "viewpoint_trace_schema.py"

VALID = '# Sample\n\n## Viewpoint Trace Table\n| Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Standard? | Justification |\n|-----------|-------------|---------|---------|-------------|-----------|---------------|\n| Motivation | Sponsor | Goals | Decide | Overview | yes | Maps drivers to outcomes |\n\n## Organisation-Specific Proposals\n\nNone this pass.\n\n## Rejected Alternatives\n\n| Viewpoint | Why rejected |\n|-----------|--------------|\n| Physical | No facilities concern in intent |\n'
MISSING_H2 = '## Viewpoint Trace Table\n| Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Standard? | Justification |\n|-----------|-------------|---------|---------|-------------|-----------|---------------|\n| X | Y | Z | design | overview | yes | because |\n'
MISSING_COL = '## Viewpoint Trace Table\n| Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Justification |\n|-----------|-------------|---------|---------|-------------|---------------|\n| X | Y | Z | design | overview | because |\n\n## Organisation-Specific Proposals\n\n## Rejected Alternatives\n'


class TestTraceSchema(unittest.TestCase):
    def _run(self, text: str) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(text)
            path = f.name
        try:
            return subprocess.run(
                [sys.executable, str(HELPER), path],
                capture_output=True,
                text=True,
                check=False,
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_valid(self) -> None:
        proc = self._run(VALID)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("ok:", proc.stdout)

    def test_missing_h2(self) -> None:
        proc = self._run(MISSING_H2)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing heading", proc.stdout)

    def test_missing_column(self) -> None:
        proc = self._run(MISSING_COL)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Standard?", proc.stdout)

    def test_missing_file(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(HELPER), str(ROOT / "no-trace.md")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
