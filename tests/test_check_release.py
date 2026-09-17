#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Unit checks for scripts/check_release.py against synthetic temp trees.

Leak samples are built by concatenation so this tracked test file never
contains a full literal match for the live gate's own sentinels.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_release  # noqa: E402


class CheckReleaseBase(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


class TrackedFilesTest(CheckReleaseBase):
    def test_fail_closed_outside_git_repo(self) -> None:
        with self.assertRaises(RuntimeError):
            check_release.tracked_files(cwd=self.root)


class RequiredFilesTest(CheckReleaseBase):
    def test_missing_required_file_flagged(self) -> None:
        (self.root / "LICENSE").write_text("x", encoding="utf-8")
        fails = check_release.check_required_files(self.root)
        self.assertIn("required file missing: README.md", fails)
        self.assertNotIn("required file missing: LICENSE", fails)

    def test_all_present_passes(self) -> None:
        for f in check_release.REQUIRED:
            p = self.root / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("x", encoding="utf-8")
        self.assertEqual(check_release.check_required_files(self.root), [])


class ForbiddenPathsTest(CheckReleaseBase):
    def test_forbidden_part_flagged(self) -> None:
        fails = check_release.check_forbidden_paths(
            ["src/__pycache__/m.pyc", "ok.py"]
        )
        self.assertEqual(fails, ["forbidden tracked path: src/__pycache__/m.pyc"])

    def test_clean_paths_pass(self) -> None:
        self.assertEqual(check_release.check_forbidden_paths(["src/ok.py"]), [])


class ForbiddenContentTest(CheckReleaseBase):
    MARKER = "CONFIDENTIAL" + " - " + "Not for external distribution"

    def test_marker_flagged(self) -> None:
        self.write("notes.md", f"secret\n{self.MARKER}\n")
        fails = check_release.check_forbidden_content(self.root, ["notes.md"])
        self.assertEqual(len(fails), 1)
        self.assertIn("forbidden content in notes.md", fails[0])

    def test_github_dir_skipped(self) -> None:
        self.write(".github/workflows/w.yml", self.MARKER)
        self.assertEqual(
            check_release.check_forbidden_content(
                self.root, [".github/workflows/w.yml"]
            ),
            [],
        )

    def test_unscoped_extension_skipped(self) -> None:
        self.write("notes.log", self.MARKER)
        self.assertEqual(
            check_release.check_forbidden_content(self.root, ["notes.log"]), []
        )


class HeadersTest(CheckReleaseBase):
    HEADER = (
        "# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.\n"
        "# SPDX-License-Identifier: MIT\n"
    )

    def test_missing_header_flagged(self) -> None:
        self.write("bare.py", "print(1)\n")
        fails = check_release.check_headers(self.root, ["bare.py"])
        self.assertEqual(fails, ["header missing: bare.py", "SPDX missing: bare.py"])

    def test_header_present_passes(self) -> None:
        self.write("good.py", self.HEADER + "print(1)\n")
        self.assertEqual(check_release.check_headers(self.root, ["good.py"]), [])


if __name__ == "__main__":
    unittest.main()
