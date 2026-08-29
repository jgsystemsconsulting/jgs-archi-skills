#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Tests for helpers.view_plan_schema."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helpers" / "view_plan_schema.py"

VALID = """# Sample

## Intent Summary
x

## Stakeholders and Concerns
x

## Proposed Viewpoints
x

## Layers Involved
x

## Modelling Sequence
x

## Dependencies
x

## Validation Points
x

## Open Questions for User
x

## Confirmation Gate
x
"""


class ViewPlanSchemaTests(unittest.TestCase):
    def _run(self, body: str) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(body)
            path = fh.name
        try:
            return subprocess.run(
                [sys.executable, str(HELPER), path],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_valid_passes(self) -> None:
        proc = self._run(VALID)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_missing_confirmation_fails(self) -> None:
        body = VALID.replace("## Confirmation Gate\nx\n", "")
        proc = self._run(body)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("Confirmation Gate", proc.stdout)


if __name__ == "__main__":
    unittest.main()
