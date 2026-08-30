#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Published tree: end-user files only; no machine-local paths."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DROP_PREFIXES = (
    ".planning/",
    "docs/eval/",
    "docs/evidence/",
    "docs/superpowers/",
    "docs/specs/",
    ".claude/",
)

DROP_FILES = (
    "GATES.md",
    "scripts/add_headers.py",
)

LOCAL_MARKERS = (
    "C:/Users/",
    "C:\\Users\\",
    "/Users/gower",
    "OneDrive\\Documents",
    "OneDrive/Documents",
)


def tracked() -> list[str]:
    return subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()


class PublishedTreeTests(unittest.TestCase):
    def test_no_drop_prefixes(self) -> None:
        files = tracked()
        bad = [
            f
            for f in files
            if f in DROP_FILES
            or any(f == p.rstrip("/") or f.startswith(p) for p in DROP_PREFIXES)
        ]
        self.assertEqual(bad, [], msg="end user does not need: " + ", ".join(bad[:20]))

    def test_no_machine_local_paths(self) -> None:
        hits: list[str] = []
        for rel in tracked():
            path = ROOT / rel
            if not path.is_file():
                continue
            if path.suffix.lower() in {".png", ".woff2", ".archimate"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in LOCAL_MARKERS:
                if marker in text:
                    hits.append(f"{rel}: {marker}")
                    break
        self.assertEqual(hits, [], msg="machine-local path in: " + ", ".join(hits[:20]))


if __name__ == "__main__":
    unittest.main()
