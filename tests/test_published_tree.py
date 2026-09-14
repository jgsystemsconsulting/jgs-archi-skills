#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Published tree: end-user files only; no machine-local paths."""
from __future__ import annotations

import re
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
    ".superpowers/",
)

DROP_FILES = (
    "GATES.md",
    "AGENTS.md",
    "scripts/add_headers.py",
    "scripts/configure_repo.sh",
    "helpers/layout_check.py",
    "helpers/specialist_manifest.py",
    "tests/test_layout_check.py",
    "tests/test_specialist_manifest.py",
)

LOCAL_MARKERS = (
    "C:/Users/",
    "C:\\Users\\",
    "/Users/gower",
    "OneDrive\\Documents",
    "OneDrive/Documents",
)

PAPER_LINK_SOURCES = (
    "README.md",
    "docs/why-soam.html",
    "docs/papers/README.md",
    "docs/papers/landing.md",
)

BLOB_PREFIX = "github.com/jgsystemsconsulting/jgs-archi-skills/blob/master/"
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HTML_HREF = re.compile(r'href="([^"]+)"')

TRACKED_PAPERS = (
    "docs/papers/README.md",
    "docs/papers/landing.md",
    "docs/papers/open-group-soam.md",
    "docs/papers/talk-abstract.md",
    "docs/papers/soam-ieee-software.md",
    "docs/papers/why-soam.md",
    "docs/papers/ieee/soam-ieee-software.pdf",
    "docs/papers/ieee/soam-ieee-long.pdf",
    "docs/papers/ieee/soam-ieee-software.tex",
    "docs/papers/ieee/soam-ieee-long.tex",
    "docs/papers/ieee/soam.bib",
    "docs/papers/ieee/build.sh",
    "docs/papers/ieee/build-long.sh",
)

DEBRIS_SUFFIXES = (".aux", ".bbl", ".blg", ".log", ".out")
DATED_PREVIEWS = (
    "docs/papers/ieee/soam-ieee-software-2026-09-07.pdf",
    "docs/papers/ieee/soam-ieee-long-2026-09-07.pdf",
)
LEFTOVER_NAMES = ("soam-workshop", "soam-ieee-software-fcl-triage-log")
REQUIRED_LINK_TARGETS = (
    "docs/papers/ieee/soam-ieee-software.pdf",
    "docs/papers/landing.md",
    "docs/papers/why-soam.md",
    "docs/papers/soam-ieee-software.md",
    "docs/papers/ieee/soam-ieee-long.pdf",
    "docs/papers/open-group-soam.md",
    "docs/papers/talk-abstract.md",
)


def paper_link_targets(rel: str) -> set[str]:
    """docs/papers/** targets linked from one published source.

    A href containing the blob/master prefix is repo-root-relative after the
    prefix is stripped. Any other non-http href resolves relative to the
    linking file's directory. Pure external URLs are ignored.
    """
    text = (ROOT / rel).read_text(encoding="utf-8")
    source_dir = (ROOT / rel).parent
    targets: set[str] = set()
    for href in MD_LINK.findall(text) + HTML_HREF.findall(text):
        if BLOB_PREFIX in href:
            candidate = href.split(BLOB_PREFIX, 1)[1].split("#", 1)[0]
        elif href.startswith(("http://", "https://")):
            continue
        else:
            candidate = href.split("#", 1)[0]
            if not candidate:
                continue
            try:
                candidate = (
                    (source_dir / candidate).resolve()
                    .relative_to(ROOT.resolve())
                    .as_posix()
                )
            except (ValueError, OSError):
                continue
        if candidate.startswith("docs/papers/"):
            targets.add(candidate)
    return targets


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
            if rel.replace("\\", "/") == "tests/test_published_tree.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in LOCAL_MARKERS:
                if marker in text:
                    hits.append(f"{rel}: {marker}")
                    break
        self.assertEqual(hits, [], msg="machine-local path in: " + ", ".join(hits[:20]))

    def test_paper_link_targets_exist(self) -> None:
        extracted = {rel: paper_link_targets(rel) for rel in PAPER_LINK_SOURCES}
        targets: set[str] = set()
        for found in extracted.values():
            targets |= found
        self.assertGreater(
            len(targets), 0, "link extraction found nothing; extractor is broken"
        )
        missing_required = sorted(set(REQUIRED_LINK_TARGETS) - targets)
        self.assertEqual(
            missing_required,
            [],
            msg="expected paper links absent from extraction: "
            + ", ".join(missing_required),
        )
        missing = sorted(t for t in targets if not (ROOT / t).is_file())
        self.assertEqual(
            missing, [], msg="linked paper path not in repo: " + ", ".join(missing)
        )

    def test_papers_tracked_set_exact(self) -> None:
        out = subprocess.check_output(
            ["git", "ls-files", "docs/papers"], cwd=ROOT, text=True
        )
        self.assertEqual(sorted(out.splitlines()), sorted(TRACKED_PAPERS))

    def test_no_debris_tracked(self) -> None:
        files = tracked()
        bad = [
            f
            for f in files
            if f.startswith("docs/papers/ieee/") and f.endswith(DEBRIS_SUFFIXES)
        ]
        bad += [f for f in files if f in DATED_PREVIEWS]
        bad += [f for f in files if f.startswith("docs/papers/ieee/_preview/")]
        bad += [f for f in files if f.startswith("docs/images/drafts/")]
        self.assertEqual(bad, [], msg="debris or previews tracked: " + ", ".join(bad))

    def test_no_leftover_names_in_published_surface(self) -> None:
        surface = [
            rel
            for rel in tracked()
            if rel == "README.md"
            or rel == "docs/why-soam.html"
            or rel.startswith("docs/papers/")
        ]
        hits: list[str] = []
        for rel in surface:
            text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
            for name in LEFTOVER_NAMES:
                if name in text:
                    hits.append(f"{rel}: {name}")
        self.assertEqual(
            hits, [], msg="deleted leftover still referenced: " + ", ".join(hits)
        )

    def test_build_scripts_marker_free(self) -> None:
        extra = ("MiKTeX", "AppData")
        hits: list[str] = []
        for rel in (
            "docs/papers/ieee/build.sh",
            "docs/papers/ieee/build-long.sh",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
            for marker in LOCAL_MARKERS + extra:
                if marker in text:
                    hits.append(f"{rel}: {marker}")
        self.assertEqual(
            hits, [], msg="build script marker leak: " + ", ".join(hits)
        )


if __name__ == "__main__":
    unittest.main()
