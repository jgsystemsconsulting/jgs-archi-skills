#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Unit tests for helpers/disposition.py. Stdlib only."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "disposition.py"
sys.path.insert(0, str(ROOT / "helpers"))
from disposition import parse_markdown_table, validate_ledger  # noqa: E402

TABLE = """# Ledger

| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| CRM | captured | CRM System @ Application Structure | |
| DTO pack | folded | CRM System | 12 request DTOs |
| Payments | needs-user | | one service or two? |
| Batch jobs | out-of-scope | | confirmed out of this pass |
"""

JSON_ROWS = [
    {
        "candidate": "CRM",
        "disposition": "captured",
        "target": "CRM System @ Application Structure",
        "reason": "",
    }
]


class T(unittest.TestCase):
    def _run(self, body: str, extra=()):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(body)
            path = fh.name
        try:
            return subprocess.run(
                [sys.executable, str(H), path, *extra],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_ok_markdown(self):
        rows = parse_markdown_table(TABLE)
        self.assertEqual(len(rows), 4)
        self.assertEqual(validate_ledger(rows), [])
        self.assertEqual(self._run(TABLE).returncode, 0)

    def test_ok_json(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as fh:
            json.dump(JSON_ROWS, fh)
            path = fh.name
        try:
            proc = subprocess.run(
                [sys.executable, str(H), path],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_empty_ledger_fails(self):
        findings = validate_ledger([])
        self.assertTrue(any(f["check_id"] == "empty_ledger" for f in findings))
        self.assertEqual(self._run("| Candidate | Disposition | Target | Reason |\n|---|---|---|---|\n").returncode, 1)

    def test_allow_empty(self):
        self.assertEqual(validate_ledger([], allow_empty=True), [])
        self.assertEqual(
            self._run(
                "| Candidate | Disposition | Target | Reason |\n|---|---|---|---|\n",
                extra=("--allow-empty",),
            ).returncode,
            0,
        )

    def test_unknown_disposition(self):
        rows = [{
            "candidate": "X",
            "disposition": "skipped",
            "target": "",
            "reason": "n/a",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "unknown_disposition" for f in findings))

    def test_captured_requires_target(self):
        rows = [{
            "candidate": "X",
            "disposition": "captured",
            "target": "",
            "reason": "",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "missing_target" for f in findings))

    def test_folded_requires_target_and_reason(self):
        rows = [{
            "candidate": "X",
            "disposition": "folded",
            "target": "",
            "reason": "",
        }]
        ids = {f["check_id"] for f in validate_ledger(rows)}
        self.assertIn("missing_target", ids)
        self.assertIn("missing_reason", ids)

    def test_needs_user_requires_reason(self):
        rows = [{
            "candidate": "X",
            "disposition": "needs-user",
            "target": "",
            "reason": "",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "missing_reason" for f in findings))

    def test_out_of_scope_requires_reason(self):
        rows = [{
            "candidate": "X",
            "disposition": "out-of-scope",
            "target": "",
            "reason": "",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "missing_reason" for f in findings))

    def test_duplicate_candidate(self):
        rows = [
            {"candidate": "CRM", "disposition": "captured",
             "target": "A @ V", "reason": ""},
            {"candidate": "CRM", "disposition": "folded",
             "target": "B", "reason": "dup"},
        ]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "duplicate_candidate" for f in findings))

    def test_two_tables_elements_first(self):
        doc = """# Specialist Result

| Element | Type | Relationships |
|---------|------|---------------|
| CRM | Application Component | realizes |

## Disposition ledger

| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| CRM | captured | CRM System @ Application Structure | |
| DTO pack | folded | CRM System | 12 request DTOs |
| Payments | needs-user | | one service or two? |
| Batch jobs | out-of-scope | | confirmed out of this pass |
"""
        rows = parse_markdown_table(doc)
        self.assertEqual(len(rows), 4)
        self.assertEqual(validate_ledger(rows), [])

    def test_disposition_table_first_then_other_table(self):
        doc = """| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| CRM | captured | CRM System @ Application Structure | |

## Elements

| Element | Type |
|---------|------|
| CRM | Application Component |
"""
        rows = parse_markdown_table(doc)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["candidate"], "CRM")
        self.assertEqual(validate_ledger(rows), [])

    def test_non_disposition_table_ignored(self):
        doc = """| Element | Type |
|---------|------|
| CRM | Application Component |
"""
        self.assertEqual(parse_markdown_table(doc), [])

    def test_non_dict_row_reported_not_crash(self):
        findings = validate_ledger(["not-a-dict"])
        self.assertTrue(any(f["check_id"] == "invalid_row" for f in findings))


if __name__ == "__main__":
    unittest.main()
