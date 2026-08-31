#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""NL-change impact planning over a view/element inventory. Stdlib only.

OBJ-6 / RATE-02 offline helper. Deterministic token/keyword match only.
Never mutates a model. Never recreates shared elements — reports must-reuse IDs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TOKEN = re.compile(r"[a-z0-9]+", re.I)


def _tokens(text: str) -> set[str]:
    return {t.casefold() for t in TOKEN.findall(text or "") if len(t) > 1}


def plan_impact(note: str, inventory: dict[str, Any]) -> dict[str, Any]:
    """Return impact plan from change note + inventory snapshot."""
    views = list(inventory.get("views") or [])
    elements = list(inventory.get("elements") or [])
    note_cf = (note or "").casefold()
    note_toks = _tokens(note)

    affected: list[dict[str, str]] = []
    for v in views:
        vid = str(v.get("id") or "")
        name = str(v.get("name") or "")
        kws = v.get("keywords") or []
        if isinstance(kws, str):
            kws = [kws]
        hay_toks = _tokens(name) | _tokens(" ".join(str(k) for k in kws))
        explicit = False
        if vid and vid.casefold() in note_cf:
            explicit = True
        if name and name.casefold() in note_cf:
            explicit = True
        overlap = note_toks & hay_toks
        strong = any(len(t) >= 4 for t in overlap)
        if explicit or (overlap and strong) or (name and name.casefold() in note_cf):
            affected.append({"id": vid, "name": name})

    seen: set[str] = set()
    uniq: list[dict[str, str]] = []
    for a in affected:
        key = a["id"] or a["name"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(a)
    affected = uniq

    affected_ids = {a["id"] for a in affected if a["id"]}

    must_reuse: list[str] = []
    for el in elements:
        eid = str(el.get("id") or "")
        if not eid or not affected:
            continue
        shared = bool(el.get("shared", False))
        view_ids = [str(x) for x in (el.get("view_ids") or [])]
        multi = len(view_ids) >= 2
        touches = bool(affected_ids & set(view_ids)) if view_ids else False
        if shared and (touches or not view_ids):
            must_reuse.append(eid)
        elif multi and touches:
            must_reuse.append(eid)

    must_reuse = sorted(set(must_reuse))

    exclusions = [
        "Do not delete shared structure to refresh visuals",
        "Do not recreate elements listed in must_reuse_element_ids",
        "Do not auto-apply NL changes without user confirmation (NG-3)",
    ]

    notes: list[str] = []
    if not affected:
        notes.append(
            "no views matched note tokens; refine keywords or name views explicitly"
        )
    if affected and not must_reuse:
        notes.append(
            "no shared elements flagged on affected views; "
            "still reuse by name+type inspect before create"
        )

    return {
        "affected_views": affected,
        "regenerate_scope": [a["id"] or a["name"] for a in affected],
        "must_reuse_element_ids": must_reuse,
        "exclusions": exclusions,
        "notes": notes,
        "change_note": note.strip(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path, help="path to change-note text file")
    parser.add_argument("inventory", type=Path, help="path to inventory JSON")
    parser.add_argument("--text", action="store_true", help="human-readable output")
    args = parser.parse_args(argv)
    note = args.note.read_text(encoding="utf-8")
    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    plan = plan_impact(note, inventory)
    if args.text:
        print(
            "affected_views:",
            ", ".join(f"{v.get('id')}({v.get('name')})" for v in plan["affected_views"])
            or "(none)",
        )
        print("must_reuse:", ", ".join(plan["must_reuse_element_ids"]) or "(none)")
        for n in plan["notes"]:
            print("note:", n)
    else:
        print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
