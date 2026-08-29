#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "compliance_checklist.py"
CHECKS = [
    "element_type_known","relationship_endpoints_valid","relationship_type_permitted",
    "abstraction_level_consistent","cross_view_naming_consistent","inspect_before_create",
]

class T(unittest.TestCase):
    def _run(self, obj):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(obj, fh)
            path = fh.name
        try:
            return subprocess.run([sys.executable, str(H), path], capture_output=True, text=True, cwd=str(ROOT))
        finally:
            Path(path).unlink(missing_ok=True)

    def test_all_pass(self):
        self.assertEqual(self._run({c: True for c in CHECKS}).returncode, 0)

    def test_fail_explains(self):
        obj = {c: True for c in CHECKS}
        obj["inspect_before_create"] = False
        proc = self._run(obj)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("inspect_before_create", proc.stdout)
        self.assertIn("compliant alternative", proc.stdout)

if __name__ == "__main__":
    unittest.main()
