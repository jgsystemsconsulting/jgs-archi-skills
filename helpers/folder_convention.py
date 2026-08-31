#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Offline Archi folder-placement checker over model-slice snapshots. Stdlib only.

House-style layer folder placement. Does not call MCP. Does not mutate the model.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_LAYER_FOLDERS = (
    "Motivation",
    "Strategy",
    "Business",
    "Application",
    "Technology",
    "Physical",
    "Implementation & Migration",
    "Views",
)

JUNCTION_TYPES = {"Junction", "AndJunction", "OrJunction"}

EXACT_FOLDER = {
    "Stakeholder": "Motivation",
    "Driver": "Motivation",
    "Assessment": "Motivation",
    "Goal": "Motivation",
    "Outcome": "Motivation",
    "Principle": "Motivation",
    "Requirement": "Motivation",
    "Constraint": "Motivation",
    "Meaning": "Motivation",
    "Value": "Motivation",
    "Resource": "Strategy",
    "Capability": "Strategy",
    "CourseOfAction": "Strategy",
    "ValueStream": "Strategy",
    "DataObject": "Application",
    "Equipment": "Physical",
    "Facility": "Physical",
    "DistributionNetwork": "Physical",
    "Material": "Physical",
    "WorkPackage": "Implementation & Migration",
    "Deliverable": "Implementation & Migration",
    "ImplementationEvent": "Implementation & Migration",
    "Plateau": "Implementation & Migration",
    "Gap": "Implementation & Migration",
}

PREFIX_FOLDER = (
    ("Business", "Business"),
    ("Application", "Application"),
    ("Technology", "Technology"),
    ("Node", "Technology"),
    ("Device", "Technology"),
    ("SystemSoftware", "Technology"),
    ("Path", "Technology"),
    ("CommunicationNetwork", "Technology"),
    ("Artifact", "Technology"),
)


def expected_folder(element_type: str) -> str | None:
    t = (element_type or "").strip()
    if t in JUNCTION_TYPES:
        return None
    if t in EXACT_FOLDER:
        return EXACT_FOLDER[t]
    for prefix, folder in PREFIX_FOLDER:
        if t.startswith(prefix):
            return folder
    return None


def _under(path: str, folder: str) -> bool:
    p = (path or "").strip().strip("/")
    return p == folder or p.startswith(folder + "/")


def validate_slice(slice_data: dict) -> list[dict]:
    layer_set = {f for f in DEFAULT_LAYER_FOLDERS if f != "Views"}
    findings: list[dict] = []
    for el in slice_data.get("elements") or []:
        eid = str(el.get("id") or "?")
        name = str(el.get("name") or "")
        etype = str(el.get("type") or el.get("element_type") or "")
        path = el.get("folder_path")
        refs = [f"{name or etype or '?'} ({eid})"]
        path_s = "" if path is None else str(path).strip()
        if etype in JUNCTION_TYPES:
            top = path_s.split("/")[0] if path_s else ""
            if top in layer_set:
                findings.append({
                    "check_id": "folder_junction_in_layer",
                    "object_refs": refs,
                    "problem": "Junction sits in a layer folder",
                    "proposed_alternative": "Leave Junction unfoldered or outside layer folders",
                })
            continue
        if not path_s:
            findings.append({
                "check_id": "folder_missing",
                "object_refs": refs,
                "problem": "element has no folder_path",
                "proposed_alternative": "Move to the matching layer folder via move-to-folder",
            })
            continue
        expected = expected_folder(etype)
        if expected and not _under(path_s, expected):
            findings.append({
                "check_id": "folder_layer_mismatch",
                "object_refs": refs,
                "problem": f"element folder {path_s!r} is not under {expected!r}",
                "proposed_alternative": f"Move to {expected} (nested subfolder allowed)",
            })
    for view in slice_data.get("views") or []:
        vid = str(view.get("id") or "?")
        vname = str(view.get("name") or "")
        path = view.get("folder_path")
        path_s = "" if path is None else str(path).strip()
        refs = [f"{vname or '?'} ({vid})"]
        if not _under(path_s, "Views"):
            findings.append({
                "check_id": "folder_view_not_under_views",
                "object_refs": refs,
                "problem": f"view folder {path_s!r} is not under Views",
                "proposed_alternative": "Move the view to Views or Views/<name>",
            })
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slice", type=Path, help="Model-slice JSON path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    slice_data = json.loads(args.slice.read_text(encoding="utf-8"))
    findings = validate_slice(slice_data)
    if args.json:
        print(json.dumps({"findings": findings, "ok": not findings}, indent=2))
    elif not findings:
        print("ok: 0 findings")
    else:
        print(f"folder findings: {len(findings)}")
        for f in findings:
            print(f"  - [{f['check_id']}] refs={f['object_refs']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
