#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Tests for helpers.validate_skill_mcp_refs (stdlib unittest)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "helpers" / "validate_skill_mcp_refs.py"
INVENTORY = ROOT / "docs" / "mcp" / "archi-bridge-inventory.json"


def run_validator(skills_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--inventory",
            str(INVENTORY),
            "--skills-root",
            str(skills_root),
        ],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


class ValidateSkillMcpRefsTests(unittest.TestCase):
    def setUp(self) -> None:
        data = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(data.get("tool_count"), 69)
        self.assertEqual(data.get("resource_count"), 14)

    def _write_skill(self, root: Path, body: str) -> None:
        d = root / "sample-skill"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(body, encoding="utf-8")

    def test_known_tool_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_skill(
                root,
                "# Sample\n\nCall `get-model-info` first.\n",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_unknown_tool_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_skill(
                root,
                "# Sample\n\nCall `create-unicorn-element` never.\n",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("create-unicorn-element", proc.stdout)

    def test_known_resource_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_skill(
                root,
                "# Sample\n\nRead archimate://reference/archimate-layers\n",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_unknown_resource_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_skill(
                root,
                "# Sample\n\nRead archimate://reference/nope\n",
            )
            proc = run_validator(root)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            self.assertIn("archimate://reference/nope", proc.stdout)


if __name__ == "__main__":
    unittest.main()
