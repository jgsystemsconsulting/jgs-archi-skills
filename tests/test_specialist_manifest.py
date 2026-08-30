#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
import json, subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "specialist_manifest.py"

class T(unittest.TestCase):
    def test_lists_specialists(self):
        proc = subprocess.run(
            [sys.executable, str(H), "--json"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["orchestrator"], "archi-orchestrator")
        self.assertGreaterEqual(data["count"], 12)
        self.assertIn("archi-viewpoint-select", data["specialists"])
        self.assertNotIn("archi-orchestrator", data["specialists"])

if __name__ == "__main__":
    unittest.main()
