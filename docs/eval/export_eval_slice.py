#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Export eval artifacts (slice.json, usages.json, views.json, PNGs) from the
bound eval model via MCP. Stdlib only. Read-only toward the model.

Usage: python docs/eval/export_eval_slice.py --out docs/evidence/eval-loop/iter-0
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_run import EvalSession  # noqa: E402

EXPECTED_MODEL = "JGS Eval Loop"


def layer_of(etype: str) -> str:
    for prefix in ("Business", "Application", "Technology", "Motivation",
                   "Strategy", "Implementation", "Composite"):
        if (etype or "").startswith(prefix):
            return prefix
    return "Other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--model", default=EXPECTED_MODEL)
    args = ap.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "png").mkdir(exist_ok=True)

    s = EvalSession(args.model, out / "transcript-export.json")

    elements = s.mcp.call("search-elements", {"query": "", "limit": 500})
    if isinstance(elements, dict):
        elements = elements.get("elements", elements.get("results", []))
    s.log("search-elements", {"query": "", "limit": 500}, f"{len(elements)} hits")

    rels = s.mcp.call("search-relationships", {"query": "", "limit": 500})
    if isinstance(rels, dict):
        rels = rels.get("relationships", rels.get("results", []))
    s.log("search-relationships", {"query": "", "limit": 500}, f"{len(rels)} hits")

    rel_docs: dict[str, str] = {}
    # join relationship documentation from the run transcript(s) in the same dir
    for tp in sorted(out.glob("transcript*.json")):
        try:
            entries = json.loads(tp.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for e in entries:
            if (e.get("tool") == "update-relationship"
                    and e.get("args", {}).get("documentation")):
                rel_docs[e["args"]["id"]] = e["args"]["documentation"]

    slice_rels = []
    for r in rels:
        slice_rels.append({
            "id": r["id"], "type": r.get("type", ""),
            "source": r.get("sourceId", r.get("source", {}).get("id", "")),
            "target": r.get("targetId", r.get("target", {}).get("id", "")),
            "documentation": rel_docs.get(r["id"]),
        })

    slice_elements = [{
        "id": e["id"], "name": e.get("name", ""), "type": e.get("type", ""),
        "layer": e.get("layer", layer_of(e.get("type", ""))),
        "documentation": e.get("documentation"),
    } for e in elements]

    views_data = {"views": []}
    usages = []
    for v in s.views():
        vid, vname = v["id"], v.get("name", v["id"])
        contents = s.mcp.call("get-view-contents", {"viewId": vid})
        if isinstance(contents, str):
            contents = json.loads(contents)
        assessment = s.mcp.call("assess-layout", {"viewId": vid})
        s.log("export-view-contents", {"viewId": vid, "view": vname})
        vis = {m["viewObjectId"]: m for m in contents.get("visualMetadata", [])}
        vis_by_eid = {m["elementId"]: m for m in contents.get("visualMetadata", [])}
        el_by_id = {e["id"]: e for e in elements}
        objects = []
        for vo in contents.get("elements", []):
            oid = vo.get("elementId", vo.get("id"))
            meta = vis_by_eid.get(oid) or vis.get(vo.get("viewObjectId"), {})
            base = el_by_id.get(oid, {})
            objects.append({
                "id": oid,
                "viewObjectId": vo.get("viewObjectId"),
                "name": vo.get("name", base.get("name", "")),
                "type": vo.get("type", base.get("type", "")),
                "x": meta.get("x"), "y": meta.get("y"),
                "width": meta.get("width"), "height": meta.get("height"),
            })
            usages.append({"id": oid, "name": vo.get("name", base.get("name", "")),
                           "type": vo.get("type", base.get("type", "")),
                           "view": vname})
        connections = [{
            "id": c.get("relationshipId", c.get("id")),
            "source": None, "target": None,
            "bendpoints": c.get("bendpoints", []),
        } for c in contents.get("connections", [])]
        # resolve connection endpoints via view objects
        vo_by_id = {vo.get("viewObjectId"): vo.get("elementId", vo.get("id"))
                    for vo in contents.get("elements", [])}
        for c, raw in zip(connections, contents.get("connections", [])):
            c["source"] = vo_by_id.get(raw.get("sourceViewObjectId"))
            c["target"] = vo_by_id.get(raw.get("targetViewObjectId"))
            c["routed"] = bool(raw.get("bendpoints"))
        views_data["views"].append({
            "view": vname, "viewId": vid, "objects": objects,
            "connections": connections, "assessment": assessment,
        })
        s.mcp.call("export-view", {"viewId": vid, "format": "png",
                                   "outputDirectory": str((out / "png").resolve()),
                                   "inline": False})

    (out / "slice.json").write_text(json.dumps({
        "elements": slice_elements,
        "relationships": slice_rels,
        "view_usages": [{"view": u["view"], "element": u["id"]} for u in usages],
    }, indent=1), encoding="utf-8")
    (out / "usages.json").write_text(json.dumps({"usages": usages}, indent=1),
                                     encoding="utf-8")
    (out / "views.json").write_text(json.dumps(views_data, indent=1),
                                    encoding="utf-8")
    print(f"exported: {len(slice_elements)} elements, {len(slice_rels)} "
          f"relationships, {len(views_data['views'])} views -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
