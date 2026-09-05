#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Installer flags: dry-run, list-agents, dest layout, agent targets."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.py"


def run(args: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
    e = os.environ.copy()
    if env:
        e.update(env)
    return subprocess.run(
        [sys.executable, str(INSTALL), *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=e,
    )


class InstallTests(unittest.TestCase):
    def test_list_agents(self) -> None:
        proc = run(["--list-agents"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for name in (
            "zcode",
            "claude",
            "codex",
            "gemini",
            "cursor",
            "copilot",
            "openclaw",
        ):
            self.assertIn(name, proc.stdout)

    def test_dry_run_default_zcode(self) -> None:
        proc = run(["--dry-run"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("archi-orchestrator", proc.stdout)
        self.assertIn("jgs-upstream-feedback", proc.stdout)
        self.assertIn("[zcode]", proc.stdout)
        self.assertIn("dry-run:", proc.stdout)

    def test_dest_flat_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "skills"
            proc = run(["--dest", str(dest)])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((dest / "archi-orchestrator" / "SKILL.md").is_file())
            self.assertTrue((dest / "archi-elicit" / "SKILL.md").is_file())
            self.assertTrue((dest / "jgs-upstream-feedback" / "SKILL.md").is_file())

    def test_agent_claude_namespaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "claude-skills"
            proc = run(["--agent", "claude", "--dest", str(dest), "--dry-run"])
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("jgs", proc.stdout.replace("\\", "/"))
            self.assertIn("archi-orchestrator", proc.stdout)

    def test_unknown_agent(self) -> None:
        proc = run(["--agent", "nope"])
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
