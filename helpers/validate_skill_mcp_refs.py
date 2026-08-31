#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Scan skills for MCP tool/resource refs; fail on names absent from inventory.

Stdlib only. Offline. Exit 0 if clean or no skills; exit 1 on unknown refs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOOL_BT = re.compile(r"`([a-z][a-z0-9-]*-[a-z0-9-]+)`")
TOOL_PHRASE = re.compile(
    r"(?i)\b(?:mcp\s+)?tools?\s+`?([a-z][a-z0-9-]*-[a-z0-9-]+)`?"
)
RESOURCE_URI = re.compile(r"(archimate://[a-z0-9][a-z0-9/._-]*)")


def load_inventory(path: Path) -> tuple[set[str], set[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    tools = {str(t) for t in data.get("tools", [])}
    resources = {str(r) for r in data.get("resources", [])}
    if not tools or not resources:
        raise SystemExit(f"inventory missing tools/resources: {path}")
    return tools, resources


def iter_skill_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(root.rglob("SKILL.md"))


def scan_file(path: Path) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    tools_hit: list[tuple[int, str]] = []
    resources_hit: list[tuple[int, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines, start=1):
        for m in TOOL_BT.finditer(line):
            tools_hit.append((i, m.group(1)))
        for m in TOOL_PHRASE.finditer(line):
            tools_hit.append((i, m.group(1)))
        for m in RESOURCE_URI.finditer(line):
            resources_hit.append((i, m.group(1).rstrip(").,;]'\"")))
    return tools_hit, resources_hit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=Path("docs/mcp/archi-bridge-inventory.json"),
    )
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=Path("skills"),
    )
    args = parser.parse_args(argv)

    if not args.inventory.is_file():
        print(f"error: inventory not found: {args.inventory}", file=sys.stderr)
        return 2

    allowed_tools, allowed_resources = load_inventory(args.inventory)
    skills = iter_skill_files(args.skills_root)
    if not skills:
        print("no skills")
        return 0

    unknown: list[str] = []
    for skill in skills:
        tools_hit, resources_hit = scan_file(skill)
        for line_no, name in tools_hit:
            if name not in allowed_tools:
                unknown.append(f"{skill.as_posix()}:{line_no}: unknown tool `{name}`")
        for line_no, uri in resources_hit:
            if uri not in allowed_resources:
                unknown.append(
                    f"{skill.as_posix()}:{line_no}: unknown resource `{uri}`"
                )

    if unknown:
        print("unknown MCP references:")
        for row in unknown:
            print(f"  {row}")
        return 1

    print(f"ok: {len(skills)} skill file(s), 0 unknown refs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
