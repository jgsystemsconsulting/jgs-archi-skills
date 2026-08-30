#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Unit tests for helpers/completion_summary_schema.py. Stdlib only."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "completion_summary_schema.py"
sys.path.insert(0, str(ROOT / "helpers"))
from completion_summary_schema import validate_completion_summary  # noqa: E402

VALID = """# Completion Summary

## Views Touched
- Business Process Cooperation

## Decisions
- Model as-is only

## Open Questions
- Include payment release?

## Confirmation Status
confirmed

## Specialists Run
documentation, layout

## Deliberately Deferred
- Payment release (out of confirmed scope)

## Improve Next
- Add application cooperation view if payments land
"""

LABEL_VALID = """# Summary
- Views Touched: v1, v2
- Decisions: keep shared Customer
- Open Questions: none
- Confirmation Status: confirmed
- Specialists Run: documentation
- Deliberately Deferred: none
- Improve Next: none
"""

OLD_FIVE = """# Completion Summary

## Views Touched
- Business Process Cooperation

## Decisions
- Model as-is only

## Open Questions
- Include payment release?

## Confirmation Status
confirmed

## Specialists Run
documentation, layout
"""


class T(unittest.TestCase):
    def _run(self, body):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(body)
            path = fh.name
        try:
            return subprocess.run(
                [sys.executable, str(H), path],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_ok_h2(self):
        self.assertEqual(validate_completion_summary(VALID), [])
        self.assertEqual(self._run(VALID).returncode, 0)

    def test_ok_labels(self):
        self.assertEqual(validate_completion_summary(LABEL_VALID), [])

    def test_old_five_block_summary_fails(self):
        findings = validate_completion_summary(OLD_FIVE)
        missing = {f["block"] for f in findings if f["check_id"] == "missing_block"}
        self.assertIn("Deliberately Deferred", missing)
        self.assertIn("Improve Next", missing)
        self.assertEqual(self._run(OLD_FIVE).returncode, 1)

    def test_missing(self):
        findings = validate_completion_summary("## Views Touched\nv1\n")
        self.assertTrue(any(f["check_id"] == "missing_block" for f in findings))
        self.assertEqual(self._run("nope").returncode, 1)

    def test_empty_block(self):
        body = """## Views Touched
x
## Decisions
x
## Open Questions
x
## Confirmation Status
confirmed
## Specialists Run
x
## Deliberately Deferred

## Improve Next
x
"""
        findings = validate_completion_summary(body)
        self.assertTrue(any(f["check_id"] == "empty_block" for f in findings))


if __name__ == "__main__":
    unittest.main()
