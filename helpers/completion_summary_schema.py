#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Validate modelling-run completion summary structure. Stdlib only.

OBJ-6 / RATE-03. Does not call MCP. Does not mutate the model.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_BLOCKS = [
    "Views Touched",
    "Decisions",
    "Open Questions",
    "Confirmation Status",
    "Specialists Run",
    "Deliberately Deferred",
    "Improve Next",
]

ALIASES = {
    "views touched": "Views Touched",
    "view touched": "Views Touched",
    "decisions": "Decisions",
    "decision": "Decisions",
    "open questions": "Open Questions",
    "open question": "Open Questions",
    "confirmation status": "Confirmation Status",
    "confirmation": "Confirmation Status",
    "specialists run": "Specialists Run",
    "specialists": "Specialists Run",
    "specialist list": "Specialists Run",
    "deferred": "Deliberately Deferred",
    "deliberately deferred": "Deliberately Deferred",
    "improve next": "Improve Next",
    "next": "Improve Next",
}

H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)
LABEL = re.compile(
    r"^(?:[-*]\s+)?(?:\*\*)?([A-Za-z][A-Za-z ]+?)(?:\*\*)?\s*:\s*(.*)$",
    re.M,
)


def _canon(title: str) -> str | None:
    key = re.sub(r"\s+", " ", title.strip().lower())
    return ALIASES.get(key)


def _blocks(text: str) -> dict[str, str]:
    """Collect bodies keyed by canonical required name."""
    out: dict[str, str] = {}
    matches = list(H2.finditer(text))
    for i, m in enumerate(matches):
        raw = m.group(1).strip()
        canon = _canon(raw) or (raw if raw in REQUIRED_BLOCKS else None)
        if not canon:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[canon] = text[start:end]
    for m in LABEL.finditer(text):
        canon = _canon(m.group(1))
        if not canon or canon in out:
            continue
        out[canon] = m.group(2) or ""
    return out


def validate_completion_summary(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    blocks = _blocks(text)
    for req in REQUIRED_BLOCKS:
        if req not in blocks:
            findings.append(
                {
                    "check_id": "missing_block",
                    "block": req,
                    "problem": f"missing required block: {req}",
                    "severity": "error",
                }
            )
            continue
        body = (blocks[req] or "").strip()
        if not body:
            findings.append(
                {
                    "check_id": "empty_block",
                    "block": req,
                    "problem": f"block empty: {req}",
                    "severity": "error",
                }
            )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    text = args.path.read_text(encoding="utf-8")
    findings = validate_completion_summary(text)
    if args.json:
        print(json.dumps({"findings": findings}, indent=2))
    elif findings:
        print("completion-summary findings:")
        for f in findings:
            print(f"  [{f['check_id']}] {f['problem']}")
    else:
        print(f"ok: completion summary has {len(REQUIRED_BLOCKS)} required blocks")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
