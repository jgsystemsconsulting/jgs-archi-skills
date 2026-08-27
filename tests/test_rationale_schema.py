#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "rationale_schema.py"
HEADS = [
    "Purpose",
    "Stakeholders and Concerns",
    "Viewpoint",
    "Questions Answered",
    "Assumptions",
    "Decisions",
    "Exclusions",
    "Open Questions",
]
VALID = "\n".join(["## %s\nx" % h for h in HEADS])


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

    def test_ok(self):
        self.assertEqual(self._run(VALID).returncode, 0)

    def test_missing(self):
        self.assertEqual(self._run("## Purpose\nx").returncode, 1)


if __name__ == "__main__":
    unittest.main()
