#!/usr/bin/env python3
"""Reset the eval model to a verified-empty state via MCP. Stdlib only.

"Fresh model" for an eval iteration = the dedicated eval model wiped to zero
elements, relationships, and views, verified via get-model-info before the
run starts (no create-model tool exists on the bridge; the GUI dance to make
a new file model is not scriptable from MCP).

Usage: python docs/eval/reset_model.py [--evidence docs/evidence/eval-loop/iter-0]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_run import EvalSession  # noqa: E402


def all_relationships(s) -> list[dict]:
    rels = s.mcp.call("search-relationships", {"query": "", "limit": 500})
    if isinstance(rels, dict):
        rels = rels.get("relationships", rels.get("results", []))
    return rels


def all_elements(s) -> list[dict]:
    els = s.mcp.call("search-elements", {"query": "", "limit": 500})
    if isinstance(els, dict):
        els = els.get("elements", els.get("results", []))
    return els


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="JGS Eval Loop")
    ap.add_argument("--evidence", type=Path, default=None)
    args = ap.parse_args()
    s = EvalSession(args.model, (args.evidence or Path("_scratch"))
                    / "transcript-reset.json")
    for r in all_relationships(s):
        s.mcp.call("delete-relationship", {"relationshipId": r["id"]})
        s.log("delete-relationship", {"relationshipId": r["id"]})
    for e in all_elements(s):
        s.mcp.call("delete-element", {"elementId": e["id"]})
        s.log("delete-element", {"elementId": e["id"]})
    for v in s.views():
        s.mcp.call("delete-view", {"viewId": v["id"]})
        s.log("delete-view", {"viewId": v["id"]})
    info = s.mcp.call("get-model-info", {})
    counts = {k: info.get(k) for k in
              ("elementCount", "relationshipCount", "viewCount")}
    s.log("verify-empty", counts)
    if any(v != 0 for v in counts.values()):
        print(f"RESET FAILED: model not empty: {counts}")
        return 1
    print(f"reset ok: {args.model!r} is empty ({counts})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
