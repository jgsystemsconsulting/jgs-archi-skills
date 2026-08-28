#!/usr/bin/env python3
"""Eval-run MCP session wrapper. Stdlib only.

Thin, transcript-recording driver used by eval-loop iterations. The skill
flow decides WHAT to create; this module records every call (tool, args)
incrementally so docs/eval/export_eval_slice.py can join relationship
documentation later (bridge read tools do not expose relationship docs).
Guarded: refuses to operate unless get-model-info reports the expected model.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

URL = "http://127.0.0.1:18090/mcp"


class MCP:
    """Same wire protocol as tests/live_mcp_smoke.py."""

    def __init__(self, url=URL):
        self.url = url
        self.sid = None
        self.seq = 0

    def _post(self, payload):
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(),
                                     method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        if self.sid:
            req.add_header("mcp-session-id", self.sid)
        with urllib.request.urlopen(req, timeout=60) as r:
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
        if isinstance(data, dict) and "error" in data and "id" not in data:
            raise RuntimeError(f"{name}: {data['error']}")
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


class EvalSession:
    def __init__(self, expected_model: str, transcript_path: str | Path):
        self.mcp = MCP()
        init = self.mcp.request("initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "jgs-archi-skills-eval", "version": "1.0"}})
        self.mcp.notify("notifications/initialized")
        info = self.mcp.call("get-model-info", {})
        name = info.get("name") if isinstance(info, dict) else str(info)
        if name != expected_model:
            raise SystemExit(
                f"GUARD: active model is {name!r}, expected {expected_model!r}; "
                "refusing to run against a non-eval model")
        self.transcript_path = Path(transcript_path)
        self.transcript_path.parent.mkdir(parents=True, exist_ok=True)
        self.transcript: list[dict] = []
        self.log("session", {"model": name,
                             "server": init["result"]["serverInfo"]["name"]})

    def log(self, tool: str, args: dict, outcome: str = "ok"):
        self.transcript.append(
            {"tool": tool, "args": args, "outcome": outcome,
             "ts": time.strftime("%Y-%m-%dT%H:%M:%S")})
        self.transcript_path.write_text(json.dumps(self.transcript, indent=1),
                                        encoding="utf-8")

    # -- model operations -------------------------------------------------

    def ensure(self, etype: str, name: str, doc: str | None = None) -> str:
        args = {"type": etype, "name": name}
        if doc:
            args["documentation"] = doc
        r = self.mcp.call("get-or-create-element", args)
        eid = pick_id(r)
        self.log("get-or-create-element", args,
                 r.get("action", "ok") if isinstance(r, dict) else "ok")
        return eid

    def relate(self, rtype: str, src: str, tgt: str, doc: str | None = None) -> str:
        args = {"type": rtype, "sourceId": src, "targetId": tgt}
        rid = pick_id(self.mcp.call("create-relationship", args))
        self.log("create-relationship", args)
        if doc:
            self.mcp.call("update-relationship", {"id": rid, "documentation": doc})
            self.log("update-relationship", {"id": rid, "documentation": doc})
        return rid

    def views(self) -> list[dict]:
        vs = self.mcp.call("get-views", {})
        self.log("get-views", {})
        return vs if isinstance(vs, list) else vs.get("views", [])

    def find_view(self, name: str) -> str | None:
        for v in self.views():
            if v.get("name") == name:
                return v["id"]
        return None

    def view(self, name: str) -> str:
        vid = self.find_view(name)
        if vid:
            return vid
        vid = pick_id(self.mcp.call("create-view", {"name": name}))
        self.log("create-view", {"name": name})
        return vid

    def place(self, view_id: str, element_id: str, x: int, y: int,
              width: int | None = None, height: int | None = None) -> None:
        args = {"viewId": view_id, "elementId": element_id, "x": x, "y": y,
                "autoConnect": True}
        if width:
            args["width"] = width
        if height:
            args["height"] = height
        self.mcp.call("add-to-view", args)
        self.log("add-to-view", args)

    def group(self, view_id: str, name: str, x: int, y: int,
              width: int, height: int) -> str:
        args = {"viewId": view_id, "name": name, "x": x, "y": y,
                "width": width, "height": height}
        r = self.mcp.call("add-group-to-view", args)
        self.log("add-group-to-view", args)
        return pick_id(r)


if __name__ == "__main__":
    print("module only; import EvalSession from eval scripts", file=sys.stderr)
    raise SystemExit(2)
