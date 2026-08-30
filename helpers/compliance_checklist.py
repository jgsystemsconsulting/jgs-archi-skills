#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Offline compliance checklist asserts for ArchiMate skill paths. Stdlib only.

Thin boolean gate (COMP-01/02 era). For OBJ-5 depth over model-slice snapshots
with explain-and-propose findings, use helpers/compliance_validate.py instead.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CHECKS = [
    "element_type_known",
    "relationship_endpoints_valid",
    "relationship_type_permitted",
    "abstraction_level_consistent",
    "cross_view_naming_consistent",
    "inspect_before_create",
]


def evaluate(report: dict) -> list[str]:
    failed: list[str] = []
    for check in CHECKS:
        val = report.get(check)
        if val is True or val == "pass":
            continue
        failed.append(check)
    return failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="JSON object of check_id -> pass/fail")
    args = parser.parse_args(argv)
    data = json.loads(args.report.read_text(encoding="utf-8"))
    failed = evaluate(data)
    if failed:
        print("compliance failures:")
        for item in failed:
            print(
                f"  - {item}: explain violation and propose compliant alternative "
                "(do not silent-apply)"
            )
        return 1
    print(f"ok: {len(CHECKS)} compliance checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
