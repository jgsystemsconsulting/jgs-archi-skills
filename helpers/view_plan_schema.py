#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Validate that a View Plan markdown file has required H2 sections.

Stdlib only. Exit 0 if all required headings present and Done When is
well-formed; exit 1 listing problems.
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
    "Done When",
    "Open Questions for User",
    "Confirmation Gate",
]

STOP_RULES = frozenset({"named-deliverable", "outcome-until"})

H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
STOP_RULE = re.compile(r"^Stop rule:\s*(.+?)\s*$", re.M)
PASS_CHECKS = re.compile(r"^Pass checks:\s*$", re.M)
MUST_NOT = re.compile(r"^MUST NOT:\s*$", re.M)
BULLET = re.compile(r"^[-*]\s+(\S.*)$", re.M)


def missing_headings(text: str) -> list[str]:
    found = {m.group(1).strip() for m in H2.finditer(text)}
    return [h for h in REQUIRED if h not in found]


def _section(text: str, title: str) -> str | None:
    matches = list(H2.finditer(text))
    for i, match in enumerate(matches):
        if match.group(1).strip() != title:
            continue
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        return text[start:end]
    return None


def _bullets_between(body: str, start_re: re.Pattern[str], end_re: re.Pattern[str] | None) -> list[str]:
    start = start_re.search(body)
    if not start:
        return []
    rest = body[start.end() :]
    if end_re is not None:
        stop = end_re.search(rest)
        if stop:
            rest = rest[: stop.start()]
    return [m.group(1).strip() for m in BULLET.finditer(rest)]


def done_when_problems(text: str) -> list[str]:
    body = _section(text, "Done When")
    if body is None:
        return []
    problems: list[str] = []
    rule = STOP_RULE.search(body)
    if rule is None:
        problems.append("missing label: Stop rule:")
    else:
        value = rule.group(1).strip()
        if value not in STOP_RULES:
            problems.append(f"invalid stop rule: {value}")
    if PASS_CHECKS.search(body) is None:
        problems.append("missing label: Pass checks:")
    elif not _bullets_between(body, PASS_CHECKS, MUST_NOT):
        problems.append("empty list: Pass checks")
    if MUST_NOT.search(body) is None:
        problems.append("missing label: MUST NOT:")
    elif not _bullets_between(body, MUST_NOT, None):
        problems.append("empty list: MUST NOT")
    return problems


def problems(text: str) -> list[str]:
    out = [f"missing heading: ## {h}" for h in missing_headings(text)]
    out.extend(done_when_problems(text))
    return out


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

    found = problems(text)
    if found:
        print(f"invalid view plan in {label}:")
        for item in found:
            print(f"  {item}")
        return 1

    print(f"ok: {label} has {len(REQUIRED)} required headings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
