#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Normalize Archi element labels and detect cross-view naming conflicts. Stdlib only.

OBJ-4 naming consistency. Policy is deterministic and documented; does not call MCP.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Default policy: trim, collapse whitespace, Title Case words.
POLICY = {
    "id": "title-collapse-v1",
    "trim": True,
    "collapse_whitespace": True,
    "case": "title",  # title | lower | preserve
}


def normalize_name(name: str, policy: dict[str, Any] | None = None) -> str:
    p = {**POLICY, **(policy or {})}
    s = name or ""
    if p.get("trim", True):
        s = s.strip()
    if p.get("collapse_whitespace", True):
        s = re.sub(r"\s+", " ", s)
    case = p.get("case", "title")
    if case == "lower":
        s = s.lower()
    elif case == "title":
        parts = s.split(" ")
        small = {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on"}
        out: list[str] = []
        for i, w in enumerate(parts):
            if not w:
                continue
            low = w.lower()
            if i > 0 and low in small:
                out.append(low)
            else:
                out.append(low[:1].upper() + low[1:] if low else w)
        s = " ".join(out)
    return s


def _norm_type(t: str) -> str:
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def detect_conflicts(
    usages: list[dict[str, Any]],
    *,
    policy: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Find naming conflicts across views / duplicate labels.

    Each usage: {id, name, view?} or {element_id, name, view_id?}.
    """
    p = {**POLICY, **(policy or {})}
    by_id: dict[str, list[dict[str, Any]]] = {}
    by_label: dict[str, list[dict[str, Any]]] = {}
    conflicts: list[dict[str, Any]] = []

    for u in usages:
        eid = str(u.get("id") or u.get("element_id") or "")
        name = str(u.get("name") or "")
        view = u.get("view") or u.get("view_id") or u.get("view_name")
        etype = str(u.get("type") or u.get("element_type") or "")
        norm = normalize_name(name, p)
        rec = {
            "id": eid,
            "name": name,
            "normalized": norm,
            "view": view,
            "type": etype,
        }
        if eid:
            by_id.setdefault(eid, []).append(rec)
        key = f"{norm}||{_norm_type(etype)}"
        by_label.setdefault(key, []).append(rec)

    for eid, rows in by_id.items():
        norms = {r["normalized"] for r in rows}
        if len(norms) > 1:
            conflicts.append(
                {
                    "kind": "cross_view_name_divergence",
                    "element_id": eid,
                    "names": sorted({r["name"] for r in rows}),
                    "normalized": sorted(norms),
                    "views": sorted({str(r["view"]) for r in rows if r["view"]}),
                    "severity": "high",
                    "proposal": "Pick one canonical display name; update_element to unify.",
                }
            )

    for key, rows in by_label.items():
        ids = {r["id"] for r in rows if r["id"]}
        if len(ids) > 1:
            norm, _, typ = key.partition("||")
            conflicts.append(
                {
                    "kind": "duplicate_label",
                    "normalized": norm,
                    "type": typ,
                    "element_ids": sorted(ids),
                    "names": sorted({r["name"] for r in rows}),
                    "severity": "medium",
                    "proposal": (
                        "Reuse one element via search/get-or-create; "
                        "retire duplicate if same concept."
                    ),
                }
            )
    return conflicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("normalize", help="Normalize one name")
    n.add_argument("name")
    n.add_argument("--case", choices=["title", "lower", "preserve"], default=None)

    c = sub.add_parser("conflicts", help="Detect conflicts from JSON usages file")
    c.add_argument("usages", type=Path, help="JSON list of {id,name,view?,type?}")

    args = parser.parse_args(argv)
    if args.cmd == "normalize":
        policy = {}
        if args.case:
            policy["case"] = args.case
        print(normalize_name(args.name, policy or None))
        return 0
    raw = json.loads(args.usages.read_text(encoding="utf-8"))
    usages = raw.get("usages", raw) if isinstance(raw, dict) else raw
    found = detect_conflicts(usages)
    print(
        json.dumps(
            {"policy": POLICY, "conflict_count": len(found), "conflicts": found},
            indent=2,
        )
    )
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
