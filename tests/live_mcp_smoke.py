#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Live end-to-end smoke of the archi skill-suite contract against a running
JGS Archi Bridge inside Archi. Stdlib only. Mirrors the orchestrator flow:
inspect model, reuse gate, create, relate, view, rationale, layout, validate,
export. Run with Archi open, MCP server started, and the scratch model
"JGS Skills Live Smoke" active (Approval Mode off or approvals granted).

Usage: python tests/live_mcp_smoke.py [--evidence-dir DIR]
Exit 0 = all steps passed; non-zero = a step failed. Writes transcript.json
and a PNG export into the evidence dir.
"""
import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

URL = "http://127.0.0.1:18090/mcp"
EXPECTED_MODEL = "JGS Skills Live Smoke"

ABSTRACTION = {
    "Business": "business", "Application": "application",
    "Technology": "technology", "Physical": "technology",
    "Motivation": "motivation", "Strategy": "strategy",
    "Implementation": "implementation", "Plateau": "implementation",
    "WorkPackage": "implementation", "Gap": "implementation",
}

RATIONALE_MD = """# View Rationale: Live Smoke - Customer Support

## Purpose
Live verification that the archi skill suite drives the JGS Archi Bridge correctly.

## Stakeholders and Concerns
Repo owner: does the suite work against a real Archi instance?

## Viewpoint
Default composite view over business and application layers.

## Questions Answered
Which application support exists for the customer-support process?

## Assumptions
Scratch model; names are illustrative only.

## Decisions
Used Serving from ApplicationService to BusinessProcess to stay cross-layer legal.

## Exclusions
Technology layer; motivational elements.

## Open Questions
None; smoke scope.
"""


def abstraction(etype):
    for prefix, layer in ABSTRACTION.items():
        if etype.startswith(prefix):
            return layer
    return "other"


class MCP:
    def __init__(self, url):
        self.url = url
        self.sid = None
        self.seq = 0

    def _post(self, payload):
        req = urllib.request.Request(
            self.url, data=json.dumps(payload).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        if self.sid:
            req.add_header("mcp-session-id", self.sid)
        with urllib.request.urlopen(req, timeout=30) as r:
            sid = r.headers.get("mcp-session-id")
            if sid:
                self.sid = sid
            body = r.read().decode()
        if not body:
            return None
        if "text/event-stream" in (r.headers.get("Content-Type") or ""):
            data = "\n".join(l[5:].strip() for l in body.splitlines()
                             if l.startswith("data:"))
            return json.loads(data)
        return json.loads(body)

    def request(self, method, params=None):
        self.seq += 1
        payload = {"jsonrpc": "2.0", "id": self.seq, "method": method}
        if params is not None:
            payload["params"] = params
        return self._post(payload)

    def notify(self, method):
        self._post({"jsonrpc": "2.0", "method": method})

    def call(self, name, args):
        res = self.request("tools/call", {"name": name, "arguments": args})
        if "error" in res:
            raise RuntimeError(f"{name}: {res['error']}")
        content = res["result"].get("content", [])
        text = "\n".join(c.get("text", "") for c in content
                         if c.get("type") == "text")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return text
        if isinstance(data, dict) and "result" in data and "id" not in data:
            return data["result"]
        return data


def pick_id(r):
    if isinstance(r, str):
        return r
    if "id" in r:
        return r["id"]
    for key in ("element", "relationship", "view", "object"):
        inner = r.get(key)
        if isinstance(inner, dict) and "id" in inner:
            return inner["id"]
    raise KeyError(f"no id in {r!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir",
                    default="live-smoke-out")
    args = ap.parse_args()
    ev = Path(args.evidence_dir)
    ev.mkdir(parents=True, exist_ok=True)
    transcript = []

    def step(name, detail=""):
        transcript.append({"step": name, "detail": detail})
        print(f"[smoke] {name}" + (f": {detail}" if detail else ""))

    mcp = MCP(URL)
    init = mcp.request("initialize", {
        "protocolVersion": "2025-03-26", "capabilities": {},
        "clientInfo": {"name": "jgs-archi-skills-live-smoke", "version": "1.0"}})
    server = init["result"]["serverInfo"]
    mcp.notify("notifications/initialized")
    step("initialize", f"{server['name']} {server.get('version', '?')}")

    tools = mcp.request("tools/list")["result"]["tools"]
    step("tools/list", f"{len(tools)} tools")

    info = mcp.call("get-model-info", {})
    model_name = info.get("name") if isinstance(info, dict) else str(info)
    step("get-model-info", str(model_name))
    assert model_name == EXPECTED_MODEL, (
        f"active model is {model_name!r}, expected {EXPECTED_MODEL!r}; "
        "refusing to mutate a non-scratch model")

    res_list = mcp.request("resources/list", {})
    uris = [r["uri"] for r in res_list["result"]["resources"]]
    step("resources/list", f"{len(uris)} resources")
    ref_uri = next((u for u in uris if "layers" in u), uris[0])
    ref = mcp.request("resources/read", {"uri": ref_uri})
    ref_text = ref["result"]["contents"][0].get("text", "")
    step("resources/read", f"{ref_uri} ({len(ref_text)} chars)")

    hits = mcp.call("search-elements", {"query": "Customer", "limit": 50})
    if isinstance(hits, dict):
        hits = hits.get("elements", hits.get("results", []))
    step("search-elements 'Customer'", f"{len(hits)} hits")

    created = mcp.call("get-or-create-element",
                       {"type": "BusinessActor", "name": "Customer"})
    cust_id = pick_id(created)
    created_action = created.get("action") if isinstance(created, dict) else ""
    step("get-or-create-element Customer", f"{cust_id} ({created_action})")

    again = mcp.call("get-or-create-element",
                     {"type": "BusinessActor", "name": "Customer"})
    again_id = pick_id(again)
    again_action = again.get("action") if isinstance(again, dict) else ""
    step("get-or-create-element Customer (2nd)",
         f"{again_id} ({again_action})")
    assert again_id == cust_id, "reuse gate failed: second call made a new id"
    assert again_action == "found_existing", (
        f"reuse gate failed: second call {again_action!r}, "
        "expected found_existing")

    mcp.call("update-element", {"id": cust_id, "documentation": "Smoke actor"})
    step("update-element documentation", cust_id)

    els = {}
    for etype, name in [("BusinessProcess", "Handle Support Case"),
                        ("ApplicationService", "Customer Support Service"),
                        ("ApplicationComponent", "CRM System")]:
        r = mcp.call("get-or-create-element", {"type": etype, "name": name})
        els[name] = pick_id(r)
        step(f"get-or-create-element {etype}", f"{name} -> {els[name]}")

    rels = []
    for rtype, src, tgt in [
            ("AssignmentRelationship", cust_id, els["Handle Support Case"]),
            ("ServingRelationship", els["Customer Support Service"],
             els["Handle Support Case"]),
            ("RealizationRelationship", els["CRM System"],
             els["Customer Support Service"])]:
        r = mcp.call("create-relationship",
                     {"type": rtype, "sourceId": src, "targetId": tgt})
        rid = pick_id(r)
        rels.append({"id": rid, "type": rtype, "source": src, "target": tgt})
        step("create-relationship", f"{rtype} -> {rid}")

    view = mcp.call("create-view", {"name": "Live Smoke - Customer Support"})
    view_id = pick_id(view)
    step("create-view", str(view_id))

    positions = [(60, 60), (340, 60), (340, 300), (640, 300)]
    view_els = {"Customer": cust_id, **els}
    for (name, (x, y)) in zip(["Customer", "Handle Support Case",
                               "Customer Support Service", "CRM System"],
                              positions):
        mcp.call("add-to-view", {"viewId": view_id,
                                 "elementId": view_els[name],
                                 "x": x, "y": y, "autoConnect": True})
        step("add-to-view", name)

    verdict = mcp.call("assess-layout", {"viewId": view_id})
    step("assess-layout", str(verdict)[:120])

    mcp.call("auto-layout-and-route", {"viewId": view_id})
    step("auto-layout-and-route", view_id)

    contents = mcp.call("get-view-contents", {"viewId": view_id})
    if isinstance(contents, str):
        contents = json.loads(contents)
    objs = contents.get("objects", contents.get("elements", []))
    conns = contents.get("connections", contents.get("relationships", []))
    step("get-view-contents", f"{len(objs)} objects, {len(conns)} connections")
    assert len(objs) >= 4, f"expected >=4 view objects, got {len(objs)}"
    assert len(conns) >= 3, f"expected >=3 connections, got {len(conns)}"

    mcp.call("export-view", {"viewId": view_id, "format": "png",
                             "outputDirectory": str(ev.resolve()),
                             "inline": False})
    step("export-view png", str(ev))

    all_hits = mcp.call("search-elements", {"query": "", "limit": 200})
    if isinstance(all_hits, dict):
        all_hits = all_hits.get("elements", all_hits.get("results", []))
    inventory = {"elements": [
        {"id": e["id"], "name": e.get("name", ""),
         "type": e.get("type", "")} for e in all_hits]}
    slice_path = ev / "live-slice.json"
    slice_path.write_text(json.dumps({
        "elements": [{"id": e["id"], "name": e.get("name", ""),
                      "type": e.get("type", ""),
                      "abstraction": abstraction(e.get("type", ""))}
                     for e in all_hits],
        "relationships": rels,
        "view_usages": [{"view": view_id, "element": e["id"]}
                        for e in all_hits],
    }, indent=1))
    (ev / "inventory.json").write_text(json.dumps(inventory, indent=1))
    (ev / "rationale.md").write_text(RATIONALE_MD)
    step("captured slice/inventory/rationale", str(ev))

    helpers_ok = True
    root = Path(__file__).resolve().parents[1]
    checks = [
        ("compliance_validate",
         [sys.executable, "helpers/compliance_validate.py",
          "--json", str(slice_path)]),
        ("rationale_schema",
         [sys.executable, "helpers/rationale_schema.py",
          "--json", str(ev / "rationale.md")]),
    ]
    for label, cmd in checks:
        p = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        status = "pass" if p.returncode == 0 else "FAIL"
        step(f"helper {label}", f"{status} :: {p.stdout.strip()[:200]}")
        helpers_ok &= p.returncode == 0

    (ev / "transcript.json").write_text(json.dumps(transcript, indent=1))
    print("[smoke] PASS" if helpers_ok else "[smoke] HELPER FAIL")
    return 0 if helpers_ok else 1


if __name__ == "__main__":
    sys.exit(main())
