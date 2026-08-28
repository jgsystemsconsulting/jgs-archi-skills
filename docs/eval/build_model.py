#!/usr/bin/env python3
"""Plan-driven model builder for eval iterations. Stdlib only.

Executes a build-plan JSON (the iteration's decision record) through the MCP
into the eval model. Neutral executor: every type/name/edge/placement decision
lives in the plan file, so per-iteration diffs show exactly what the improved
skills changed. Guarded to the eval model only.

Usage: python docs/eval/build_model.py docs/evidence/eval-loop/iter-0/build-plan.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_run import EvalSession  # noqa: E402

MODEL = "JGS Eval Loop"


def build(plan_path: Path) -> int:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    out_dir = plan_path.parent
    s = EvalSession(MODEL, out_dir / f"transcript-{plan.get('phase', 'build')}.json")

    els: dict[str, str] = {}
    for e in plan["elements"]:
        els[e["key"]] = s.ensure(e["type"], e["name"], e.get("doc"))

    for r in plan.get("relationships", []):
        rid = find_rel_id(s, r, els)
        if not rid:
            args = {"type": r["type"], "sourceId": els[r["src"]],
                    "targetId": els[r["tgt"]]}
            if r.get("accessType"):
                args["accessType"] = r["accessType"]
            if r.get("strength"):
                args["influenceStrength"] = r["strength"]
            s.mcp.call("create-relationship", args)
            s.log("create-relationship", args)
            rid = find_rel_id(s, r, els)
            if not rid:
                raise SystemExit(
                    f"create-relationship reported success but no id for "
                    f"{r['type']} {r['src']}->{r['tgt']}")
        if r.get("doc"):
            s.mcp.call("update-relationship",
                       {"id": rid, "documentation": r["doc"]})
            s.log("update-relationship", {"id": rid, "documentation": r["doc"]})
        r["_id"] = rid
    verify(s, plan, els)

    for v in plan.get("views", []):
        vid = s.view(v["name"])
        cols = v.get("cols", 4)
        for i, key in enumerate(v["elements"]):
            pos = v.get("positions", {}).get(key)
            if pos:
                x, y = pos
            else:
                x = 40 + (i % cols) * 240
                y = 40 + (i // cols) * 140
            s.place(vid, els[key], x, y)
        if v.get("autoLayout", True):
            s.mcp.call("auto-layout-and-route", {"viewId": vid})
            s.log("auto-layout-and-route", {"viewId": vid})

    print(f"built {len(els)} elements, {len(plan.get('relationships', []))} "
          f"relationships, {len(plan.get('views', []))} views")
    return 0


def find_rel_id(s: EvalSession, r: dict, els: dict) -> str | None:
    src, tgt = els[r["src"]], els[r["tgt"]]
    rels = s.mcp.call("get-relationships", {"elementId": src})
    if isinstance(rels, dict):
        rels = rels.get("relationships", [])
    for rel in rels:
        tid = rel.get("targetId") or rel.get("target", {}).get("id")
        if rel.get("type") == r["type"] and tid == tgt:
            return rel["id"]
    return None


def verify(s: EvalSession, plan: dict, els: dict) -> None:
    """Post-build verification against the live model, not in-run bookkeeping."""
    from collections import Counter

    problems = []
    all_rels = s.mcp.call("search-relationships", {"query": "", "limit": 500})
    if isinstance(all_rels, dict):
        all_rels = all_rels.get("relationships", [])
    model = Counter((r["type"], r["sourceId"], r["targetId"]) for r in all_rels)
    for r in plan["relationships"]:
        k = (r["type"], els[r["src"]], els[r["tgt"]])
        if model[k] < 1:
            problems.append(f"missing relationship {r['type']} "
                            f"{r['src']}->{r['tgt']}")
    documented = {e["args"]["id"] for e in s.transcript
                  if e["tool"] == "update-relationship"
                  and e["args"].get("documentation")}
    for r in plan["relationships"]:
        if r.get("doc") and r.get("_id") not in documented:
            problems.append(f"documentation not recorded for {r['type']} "
                            f"{r['src']}->{r['tgt']}")
    if problems:
        raise SystemExit("VERIFY FAILED:\n  " + "\n  ".join(problems))
    print(f"verify ok: {len(plan['elements'])} elements, "
          f"{len(plan['relationships'])} relationships all present and documented")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    args = ap.parse_args()
    raise SystemExit(build(args.plan))
