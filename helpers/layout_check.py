#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""View layout checker over exported view snapshots. Stdlib only.

Consumes a views.json snapshot (list of views with nested elements and bounds):
object bounding boxes, connection endpoints, and the bridge's own assess-layout
metrics per view. Flags what "readable without manual cleanup" means here:
- overlapping shapes (partial intersections, or improper containment
  where the container is not a Grouping),
- backward flow on the dominant axis (right-to-left or bottom-to-top),
- interleaved layer groups (centroids closer than the grouping threshold),
- nonzero hard counts from the bridge assessor (overlaps, label overlaps,
  orphaned connections) and a poor/fair overall rating.
Edge-crossing counts are recorded as stats, not findings, because some
crossings are unavoidable in dense views. Does not call MCP.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOL = 2.0          # px of tolerated intersection before calling it an overlap
FLOW_TOL = 40.0    # px of tolerated backward drift on the dominant axis
LAYER_SEP = 50.0   # min px separation between layer-group centroids on one axis
BAD_RATINGS = {"poor", "fair"}

ABSTRACTION = {
    "Business": "business", "Application": "application",
    "Technology": "technology", "Motivation": "motivation",
    "Strategy": "strategy", "Implementation": "implementation",
    "Composite": "composite",
}


def _finding(check_id: str, view: str, refs: list[str], problem: str,
             proposal: str) -> dict:
    return {
        "check_id": check_id,
        "view": view,
        "object_refs": refs,
        "problem": problem,
        "proposed_alternative": proposal,
    }


def _layer(etype: str) -> str:
    for prefix, layer in ABSTRACTION.items():
        if (etype or "").startswith(prefix):
            return layer
    return "other"


def _boxes_overlap(a: dict, b: dict) -> bool:
    ox = min(a["x"] + a["width"], b["x"] + b["width"]) - max(a["x"], b["x"])
    oy = min(a["y"] + a["height"], b["y"] + b["height"]) - max(a["y"], b["y"])
    return ox > TOL and oy > TOL


def _contains(outer: dict, inner: dict) -> bool:
    return (outer["x"] <= inner["x"] + TOL and outer["y"] <= inner["y"] + TOL
            and outer["x"] + outer["width"] >= inner["x"] + inner["width"] - TOL
            and outer["y"] + outer["height"] >= inner["y"] + inner["height"] - TOL)


def _segment_cross(s1: tuple, e1: tuple, s2: tuple, e2: tuple) -> bool:
    def orient(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)

    def on_seg(p, q, r):
        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0])
                and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

    o1, o2 = orient(s1, e1, s2), orient(s1, e1, e2)
    o3, o4 = orient(s2, e2, s1), orient(s2, e2, e1)
    if o1 != o2 and o3 != o4:
        return True
    return ((o1 == 0 and on_seg(s1, s2, e1)) or (o2 == 0 and on_seg(s1, e2, e1))
            or (o3 == 0 and on_seg(s2, s1, e2)) or (o4 == 0 and on_seg(s2, e1, e2)))


def check_view(view: dict) -> tuple[list[dict], dict]:
    name = view.get("view", view.get("viewId", "?"))
    findings: list[dict] = []
    stats = {"view": name, "connections": 0, "edge_crossings": 0}
    objs = view.get("objects", [])
    by_vid = {}
    for o in objs:
        if o.get("viewObjectId"):
            by_vid[o["viewObjectId"]] = o
        if any(o.get(k) is None for k in ("x", "y", "width", "height")):
            findings.append(_finding(
                "layout_missing_geometry", name, [o.get("name", o.get("id", "?"))],
                "view object has no complete bounding box",
                "Re-place the object on the view with explicit coordinates"))

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            a, b = objs[i], objs[j]
            if any(a.get(k) is None or b.get(k) is None
                   for k in ("x", "y", "width", "height")):
                continue
            if not _boxes_overlap(a, b):
                continue
            nested = _contains(a, b) or _contains(b, a)
            if _contains(b, a):
                container, inner = b, a
            else:
                container, inner = a, b
            if nested and _layer(container.get("type", "")) == "other":
                continue
            refs = [a.get("name", a.get("id", "?")), b.get("name", b.get("id", "?"))]
            findings.append(_finding(
                "layout_containment_violation" if nested else "layout_overlap",
                name, refs,
                "object fully inside a non-group object" if nested
                else "two objects partially overlap",
                "Move or resize so shapes are disjoint (group with a Grouping element)"))

    obj_by_id = {o.get("id"): o for o in objs}
    centers: list[tuple[tuple[float, float], tuple[float, float], bool]] = []
    conns = view.get("connections", [])
    stats["connections"] = len(conns)
    for c in conns:
        s = obj_by_id.get(c.get("source"))
        t = obj_by_id.get(c.get("target"))
        if not s or not t:
            continue
        if any(s.get(k) is None or t.get(k) is None
               for k in ("x", "y", "width", "height")):
            continue
        sc = (s["x"] + s["width"] / 2, s["y"] + s["height"] / 2)
        tc = (t["x"] + t["width"] / 2, t["y"] + t["height"] / 2)
        dx, dy = tc[0] - sc[0], tc[1] - sc[1]
        if abs(dx) >= abs(dy):
            backward = dx < -FLOW_TOL
        else:
            backward = dy < -FLOW_TOL
        if backward:
            findings.append(_finding(
                "layout_backward_flow", name,
                [s.get("name", s["id"]), t.get("name", t["id"])],
                "connection runs backward on its dominant axis (right-to-left or bottom-to-top)",
                "Reposition so the dominant flow direction stays left-to-right / top-to-bottom"))
        centers.append((sc, tc, c.get("routed") is True))
        if c.get("routed") is not True:
            stats["unrouted_connections"] = stats.get("unrouted_connections", 0) + 1

    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            if _segment_cross(centers[i][0], centers[i][1],
                              centers[j][0], centers[j][1]):
                stats["edge_crossings"] += 1

    groups: dict[str, list[dict]] = {}
    for o in objs:
        if all(o.get(k) is not None for k in ("x", "y", "width", "height")):
            groups.setdefault(_layer(o.get("type", "")), []).append(o)
    layers = {k: v for k, v in groups.items() if len(v) >= 2}
    names = sorted(layers)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ga, gb = layers[names[i]], layers[names[j]]
            ca = (sum(o["x"] + o["width"] / 2 for o in ga) / len(ga),
                  sum(o["y"] + o["height"] / 2 for o in ga) / len(ga))
            cb = (sum(o["x"] + o["width"] / 2 for o in gb) / len(gb),
                  sum(o["y"] + o["height"] / 2 for o in gb) / len(gb))
            if abs(ca[0] - cb[0]) < LAYER_SEP and abs(ca[1] - cb[1]) < LAYER_SEP:
                findings.append(_finding(
                    "layout_layer_interleave", name, [names[i], names[j]],
                    f"layer groups {names[i]} and {names[j]} occupy the same area",
                    "Cluster each layer into its own region (columns or bands)"))

    assess = view.get("assessment") or {}
    hard = [("overlapCount", "mcp_overlap", "bridge assessor reports overlapping shapes"),
            ("containmentOverlaps", "mcp_containment_overlap",
             "bridge assessor reports containment overlaps"),
            ("labelOverlapCount", "mcp_label_overlap", "bridge assessor reports label overlaps"),
            ("orphanedConnections", "mcp_orphaned_connections",
             "bridge assessor reports connections without visible endpoints")]
    for key, cid, msg in hard:
        if assess.get(key, 0) > 0:
            findings.append(_finding(
                cid, name, [view.get("viewId", "?")], f"{msg} ({key}={assess[key]})",
                "Re-run auto-layout-and-route and fix remaining issues manually via positions"))
    rating = str(assess.get("overallRating", "")).casefold()
    if rating in BAD_RATINGS:
        findings.append(_finding(
            "mcp_rating", name, [view.get("viewId", "?")],
            f"bridge assessor overallRating is {rating!r}",
            "Improve spacing and alignment until the assessor rates the view good"))
    return findings, stats


def validate_views(views_data: dict) -> tuple[list[dict], list[dict]]:
    findings: list[dict] = []
    stats: list[dict] = []
    for view in views_data.get("views", []):
        f, s = check_view(view)
        findings.extend(f)
        stats.append(s)
    return findings, stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("views", type=Path, help="views.json path")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    args = parser.parse_args(argv)
    views_data = json.loads(args.views.read_text(encoding="utf-8"))
    findings, stats = validate_views(views_data)
    if args.json:
        print(json.dumps({"findings": findings, "stats": stats,
                          "ok": not findings}, indent=2))
    elif not findings:
        n_views = len(views_data.get("views", []))
        crossings = sum(s["edge_crossings"] for s in stats)
        print(f"ok: 0 findings ({n_views} views, {crossings} edge crossings)")
    else:
        print(f"layout findings: {len(findings)}")
        for f in findings:
            print(f"  - [{f['check_id']}] view={f['view']} refs={f['object_refs']}")
            print(f"      problem: {f['problem']}")
            print(f"      proposed: {f['proposed_alternative']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
