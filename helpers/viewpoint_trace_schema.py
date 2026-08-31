#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Validate Viewpoint Trace Table markdown. Stdlib only."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_H2 = [
    "Viewpoint Trace Table",
    "Organisation-Specific Proposals",
    "Rejected Alternatives",
]

REQUIRED_COLUMNS = [
    "Viewpoint",
    "Stakeholder",
    "Concern",
    "Purpose",
    "Abstraction",
    "Standard?",
    "Justification",
]

H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
HEADER_ROW = re.compile(r"^\|[^\n]+\|$", re.M)

def missing_headings(text: str) -> list[str]:
    found = {m.group(1).strip() for m in H2.finditer(text)}
    return [h for h in REQUIRED_H2 if h not in found]

def header_columns(text: str) -> set[str]:
    cols: set[str] = set()
    for m in HEADER_ROW.finditer(text):
        line = m.group(0).strip()
        body = line.strip("|")
        parts = [p.strip() for p in body.split("|")]
        if parts and all(re.fullmatch(r":?-{3,}:?", p or "") for p in parts):
            continue
        for p in parts:
            if p:
                cols.add(p)
    return cols

def missing_columns(text: str) -> list[str]:
    cols = header_columns(text)
    return [c for c in REQUIRED_COLUMNS if c not in cols]

def validate(text: str) -> list[str]:
    problems: list[str] = []
    for h in missing_headings(text):
        problems.append(f"missing heading: ## {h}")
    for c in missing_columns(text):
        problems.append(f"missing table column: {c}")
    return problems

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="Markdown file (default: stdin)")
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
    problems = validate(text)
    if problems:
        print(f"invalid trace table in {label}:")
        for p in problems:
            print(f"  {p}")
        return 1
    print(
        f"ok: {label} has {len(REQUIRED_H2)} required headings "
        f"and {len(REQUIRED_COLUMNS)} required columns"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
