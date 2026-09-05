#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Validate that a View Plan markdown file has required H2 sections.

Stdlib only. Exit 0 if all required headings present; exit 1 listing missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = [
    "Intent Summary",
    "Stakeholders and Concerns",
    "Proposed Viewpoints",
    "Layers Involved",
    "Modelling Sequence",
    "Dependencies",
    "Validation Points",
    "Open Questions for User",
    "Confirmation Gate",
]

H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)


def missing_headings(text: str) -> list[str]:
    found = {m.group(1).strip() for m in H2.finditer(text)}
    return [h for h in REQUIRED if h not in found]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="Markdown file (default: stdin)",
    )
    args = parser.parse_args(argv)

    if args.path is None:
        text = sys.stdin.read()
        label = "<stdin>"
    else:
        if not args.path.is_file():
            print(f"error: file not found: {args.path}", file=sys.stderr)
            return 2
        text = args.path.read_text(encoding="utf-8")
        label = str(args.path)

    missing = missing_headings(text)
    if missing:
        print(f"missing headings in {label}:")
        for h in missing:
            print(f"  ## {h}")
        return 1

    print(f"ok: {label} has {len(REQUIRED)} required headings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
