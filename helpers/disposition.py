#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Validate candidate disposition ledgers. Stdlib only.

Does not call MCP. Does not mutate the model.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DISPOSITIONS = ("captured", "folded", "needs-user", "out-of-scope")
NEEDS_TARGET = {"captured", "folded"}
NEEDS_REASON = {"folded", "needs-user", "out-of-scope"}


def _finding(check_id: str, problem: str, candidate: str = "") -> dict[str, Any]:
    out = {"check_id": check_id, "problem": problem}
    if candidate:
        out["candidate"] = candidate
    return out


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] | None = None  # [] = current table is not a disposition table
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            # Non-table line ends the current table; a new table may follow.
            header = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        if header is None:
            header = [c.casefold() for c in cells]
            if "candidate" not in header and "disposition" not in header:
                header = []  # skip tables that are not disposition ledgers
            continue
        if not header:
            continue
        if all(set(c) <= set("-: ") and c for c in cells):
            continue
        by = {header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))}
        rows.append({
            "candidate": by.get("candidate", ""),
            "disposition": by.get("disposition", ""),
            "target": by.get("target", ""),
            "reason": by.get("reason", ""),
        })
    return rows


def validate_ledger(
    rows: list[dict], *, allow_empty: bool = False
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not rows:
        if not allow_empty:
            findings.append(_finding("empty_ledger", "disposition ledger is empty"))
        return findings
    seen: dict[str, int] = {}
    for row in rows:
        if not isinstance(row, dict):
            findings.append(_finding(
                "invalid_row",
                f"ledger row is not an object: {row!r}",
            ))
            continue
        name = (row.get("candidate") or "").strip()
        disp = (row.get("disposition") or "").strip().casefold()
        target = (row.get("target") or "").strip()
        reason = (row.get("reason") or "").strip()
        if not name:
            findings.append(_finding("missing_candidate", "row has no candidate name"))
            continue
        key = name.casefold()
        if key in seen:
            findings.append(_finding(
                "duplicate_candidate",
                f"candidate appears more than once: {name}",
                name,
            ))
        seen[key] = seen.get(key, 0) + 1
        if disp not in DISPOSITIONS:
            findings.append(_finding(
                "unknown_disposition",
                f"disposition {disp!r} is not one of {DISPOSITIONS}",
                name,
            ))
            continue
        if disp in NEEDS_TARGET and not target:
            findings.append(_finding(
                "missing_target",
                f"{disp} requires target",
                name,
            ))
        if disp in NEEDS_REASON and not reason:
            findings.append(_finding(
                "missing_reason",
                f"{disp} requires reason",
                name,
            ))
    return findings


def _load(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        if not isinstance(data, list):
            raise SystemExit(f"json ledger must be a list: {path}")
        return data
    return parse_markdown_table(raw)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args(argv)
    rows = _load(args.path)
    findings = validate_ledger(rows, allow_empty=args.allow_empty)
    if args.json:
        print(json.dumps({"findings": findings, "ok": not findings}, indent=2))
    elif findings:
        print("disposition findings:")
        for f in findings:
            who = f" {f['candidate']}" if f.get("candidate") else ""
            print(f"  [{f['check_id']}]{who}: {f['problem']}")
    else:
        print(f"ok: {len(rows)} disposition row(s)")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
