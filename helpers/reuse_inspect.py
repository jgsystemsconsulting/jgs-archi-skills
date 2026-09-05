#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Decide reuse | create | ambiguous from an element inventory snapshot. Stdlib only.

Offline helper for OBJ-4. Does not call MCP. Agents still use search-elements /
get-or-create-element live; this module scores a captured inventory for tests and
for structured decision records after MCP search.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def _norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def score_match(
    candidate_name: str, candidate_type: str | None, element: dict[str, Any]
) -> float:
    """Return 0..1 similarity. Exact name+type = 1.0; exact name only = 0.85."""
    en = _norm(str(element.get("name", "")))
    et = _norm(str(element.get("type", element.get("element_type", ""))))
    cn = _norm(candidate_name)
    ct = _norm(candidate_type or "")
    if not cn or not en:
        return 0.0
    if cn == en and ct and et and ct == et:
        return 1.0
    if cn == en:
        return 0.85 if not ct else (0.85 if not et else 0.0)
    if (
        ct
        and et
        and ct == et
        and (cn in en or en in cn)
        and min(len(cn), len(en)) >= 3
    ):
        return 0.55
    return 0.0


def inspect_reuse(
    candidate_name: str,
    inventory: list[dict[str, Any]],
    *,
    candidate_type: str | None = None,
    reuse_threshold: float = 0.85,
    ambiguous_floor: float = 0.5,
) -> dict[str, Any]:
    """Return structured decision for one candidate against inventory elements.

    Decisions:
      - reuse: one clear match at/above reuse_threshold
      - create: no match at/above ambiguous_floor
      - ambiguous: multiple high matches, or only mid-score near-matches
    """
    scored: list[dict[str, Any]] = []
    for el in inventory:
        s = score_match(candidate_name, candidate_type, el)
        if s <= 0:
            continue
        scored.append(
            {
                "id": el.get("id") or el.get("element_id"),
                "name": el.get("name"),
                "type": el.get("type", el.get("element_type")),
                "score": round(s, 3),
            }
        )
    scored.sort(key=lambda x: (-x["score"], str(x.get("id") or "")))

    high = [m for m in scored if m["score"] >= reuse_threshold]
    mid = [m for m in scored if ambiguous_floor <= m["score"] < reuse_threshold]

    if len(high) == 1:
        decision = "reuse"
        matched = high
    elif len(high) > 1:
        decision = "ambiguous"
        matched = high
    elif mid:
        decision = "ambiguous"
        matched = mid
    else:
        decision = "create"
        matched = []

    return {
        "candidate": {"name": candidate_name, "type": candidate_type},
        "decision": decision,
        "matches": matched,
        "reuse_threshold": reuse_threshold,
        "ambiguous_floor": ambiguous_floor,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Candidate element name")
    parser.add_argument("--type", default=None, help="Candidate element type")
    parser.add_argument(
        "--inventory",
        type=Path,
        required=True,
        help="JSON list of elements [{id,name,type}, ...] or {elements:[...]}",
    )
    parser.add_argument("--json", action="store_true", help="Print full JSON result")
    args = parser.parse_args(argv)
    raw = json.loads(args.inventory.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        inventory = raw.get("elements") or raw.get("inventory") or []
    else:
        inventory = raw
    result = inspect_reuse(args.name, inventory, candidate_type=args.type)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"decision: {result['decision']}")
        for m in result["matches"]:
            print(
                f"  - {m.get('id')} {m.get('name')} ({m.get('type')}) score={m['score']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
