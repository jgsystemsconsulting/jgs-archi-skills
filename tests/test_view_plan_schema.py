#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Tests for helpers.view_plan_schema."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helpers" / "view_plan_schema.py"

HEADINGS = """# Sample

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
"""

TAIL = """
## Open Questions for User
x

## Confirmation Gate
x
"""

DONE_NAMED = """
## Done When
Stop rule: named-deliverable
Pass checks:
- Capability Map view exists
- MUST NOT holds
MUST NOT:
- Do not add mill equipment
- Do not invent a motivation layer
"""

DONE_OUTCOME = """
## Done When
Stop rule: outcome-until
Pass checks:
- Quote-to-cash trace is visible on the named views
- CRM and MES remain separate applications
MUST NOT:
- Do not merge CRM into MES
- Do not redesign the mill
"""

NINE = HEADINGS + TAIL
VALID_NAMED = HEADINGS + DONE_NAMED + TAIL
VALID_OUTCOME = HEADINGS + DONE_OUTCOME + TAIL


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

    def test_nine_heading_plan_fails(self) -> None:
        proc = self._run(NINE)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("Done When", proc.stdout)

    def test_named_deliverable_passes(self) -> None:
        proc = self._run(VALID_NAMED)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_outcome_until_passes(self) -> None:
        proc = self._run(VALID_OUTCOME)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_missing_confirmation_fails(self) -> None:
        body = VALID_NAMED.replace("## Confirmation Gate\nx\n", "")
        proc = self._run(body)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("Confirmation Gate", proc.stdout)

    def test_bad_stop_rule_goal_fails(self) -> None:
        body = VALID_NAMED.replace(
            "Stop rule: named-deliverable", "Stop rule: goal"
        )
        proc = self._run(body)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("stop rule", proc.stdout.lower())

    def test_bad_stop_rule_spaced_token_fails(self) -> None:
        body = VALID_NAMED.replace(
            "Stop rule: named-deliverable", "Stop rule: named deliverable"
        )
        proc = self._run(body)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("stop rule", proc.stdout.lower())

    def test_empty_must_not_fails(self) -> None:
        body = VALID_NAMED.replace(
            "MUST NOT:\n- Do not add mill equipment\n- Do not invent a motivation layer\n",
            "MUST NOT:\n",
        )
        proc = self._run(body)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("MUST NOT", proc.stdout)


if __name__ == "__main__":
    unittest.main()
