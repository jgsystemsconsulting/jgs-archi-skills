#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Validate docs/prompts/*.md orchestrator cards. Stdlib only. No MCP."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "Priority",
    "Invoke",
    "Problem",
    "Stakeholders",
    "Concerns",
    "Scope",
    "Current state",
    "Target state",
    "Expected views",
    "Specialists expected",
    "Pass checks",
]

KNOWN_PRIORITIES = frozenset({"P0", "P1", "P2"})

FORBIDDEN_IN_USER_FIELDS = (
    "Application Component",
    "Business Actor",
    "Business Process",
    "Technology Node",
    "ApplicationComponent",
    "BusinessActor",
    "BusinessProcess",
    "TechnologyNode",
    "create-element",
)

H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
BULLET = re.compile(r"^[-*]\s+(\S+)\s*$", re.M)
FILENAME = re.compile(r"^p\d{2}-[a-z0-9-]+\.md$")

SKILL_NAME = re.compile(r"^archi-[a-z0-9-]+$")


def _skills_root() -> Path:
    return Path(__file__).resolve().parents[1] / "skills"


def known_skill_names() -> set[str]:
    root = _skills_root()
    names = {"archi-orchestrator"}
    if root.is_dir():
        for child in root.iterdir():
            if child.is_dir() and (child / "SKILL.md").is_file():
                names.add(child.name)
    return names


def sections(text: str) -> dict[str, str]:
    matches = list(H2.finditer(text))
    out: dict[str, str] = {}
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[title] = text[start:end].strip()
    return out


def missing_headings(text: str) -> list[str]:
    found = sections(text)
    return [h for h in REQUIRED_HEADINGS if h not in found]


def invoke_line(text: str) -> str:
    body = sections(text).get("Invoke", "")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    return lines[0] if lines else ""


def specialists_listed(text: str) -> list[str]:
    body = sections(text).get("Specialists expected", "")
    return BULLET.findall(body)


def _h2_titles(text: str) -> list[str]:
    return [m.group(1).strip() for m in H2.finditer(text)]


def validate_card(text: str) -> list[str]:
    findings: list[str] = []
    titles = _h2_titles(text)
    extra = [t for t in titles if t not in REQUIRED_HEADINGS]
    for t in extra:
        findings.append(f"extra heading: {t}")
    missing = missing_headings(text)
    for h in missing:
        findings.append(f"missing heading: {h}")
    present_required = [t for t in titles if t in REQUIRED_HEADINGS]
    expected = [h for h in REQUIRED_HEADINGS if h not in missing]
    if present_required != expected:
        findings.append("required headings out of order")
    found = sections(text)
    for h in REQUIRED_HEADINGS:
        if h in found and not found[h].strip():
            findings.append(f"empty section: {h}")
    if "Priority" in found:
        pri = found["Priority"].strip()
        if pri not in KNOWN_PRIORITIES:
            findings.append(f"priority must be P0, P1, or P2; got {pri!r}")
    line = invoke_line(text)
    if not line.startswith("/archi-orchestrator "):
        findings.append("invoke must be one line starting with '/archi-orchestrator '")
    elif len(line[len("/archi-orchestrator ") :]) < 12:
        findings.append("invoke intent after skill name is too short")
    if "Invoke" in found:
        inv_lines = [ln.strip() for ln in found["Invoke"].splitlines() if ln.strip()]
        if len(inv_lines) != 1:
            findings.append("invoke must contain exactly one non-empty line")
    known = known_skill_names()
    for name in specialists_listed(text):
        if not SKILL_NAME.match(name):
            findings.append(f"specialist bullet is not a skill name: {name}")
        elif name not in known:
            findings.append(f"unknown specialist: {name}")
    for field in ("Invoke", "Problem"):
        body = found.get(field, "")
        lower = body.lower()
        for token in FORBIDDEN_IN_USER_FIELDS:
            if token.lower() in lower:
                findings.append(f"{token} is forbidden in {field}")
    return findings


def iter_cards(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    cards = [
        p
        for p in root.iterdir()
        if p.is_file() and FILENAME.match(p.name)
    ]
    return sorted(cards, key=lambda p: p.name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("docs/prompts"),
        help="Card file or directory (default: docs/prompts)",
    )
    args = parser.parse_args(argv)
    path: Path = args.path
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    targets = [path] if path.is_file() else iter_cards(path)
    if path.is_dir() and not targets:
        print(f"error: no prompt cards in {path}", file=sys.stderr)
        return 1
    failed = 0
    for card in targets:
        text = card.read_text(encoding="utf-8")
        findings = validate_card(text)
        if findings:
            failed += 1
            print(f"FAIL {card}:")
            for item in findings:
                print(f"  - {item}")
        else:
            print(f"ok: {card}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
