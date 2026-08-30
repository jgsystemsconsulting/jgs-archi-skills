#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Documentation coverage checker over model-slice snapshots. Stdlib only.

Eval-loop gate helper. Verifies that every element and relationship in the
slice carries a meaningful documentation field: present, non-empty, not a
bare placeholder, not merely a restatement of the name. Relationship
documentation reaches the slice via the exporter, which joins recorded
update-relationship transcript entries (the bridge read tools do not expose
relationship documentation). Findings follow the same JSON shape as
compliance_validate.py. Does not call MCP. Does not mutate the model.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER_DOCS = {
    "todo", "tbd", "tba", "na", "n a", "none", "unknown", "doc", "docs",
    "description", "desc", "documentation", "text", "placeholder",
}
MIN_WORDS = 3


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.casefold())


def _finding(check_id: str, refs: list[str], problem: str, proposal: str) -> dict:
    return {
        "check_id": check_id,
        "object_refs": refs,
        "problem": problem,
        "proposed_alternative": proposal,
    }


def check_docs(name: str, doc: str | None, kind: str, obj_id: str) -> list[dict]:
    refs = [f"{name or '?'} ({obj_id})"]
    if doc is None or not doc.strip():
        return [_finding(
            f"docs_missing_{kind}", refs,
            "documentation field is empty or absent",
            "Write 1-2 sentences: what it is, why it exists, or what decision it records",
        )]
    stripped = doc.strip()
    if stripped.casefold() in PLACEHOLDER_DOCS:
        return [_finding(
            "docs_placeholder", refs,
            f"documentation is a placeholder: {stripped!r}",
            "Replace with a sentence describing the concept's role or rationale",
        )]
    doc_words = set(_words(stripped))
    name_words = set(_words(name or ""))
    if doc_words and doc_words <= name_words:
        return [_finding(
            "docs_restates_name", refs,
            "documentation only repeats words from the name",
            "Describe purpose, scope, or the decision behind the concept instead",
        )]
    if len(_words(stripped)) < MIN_WORDS:
        return [_finding(
            "docs_too_short", refs,
            f"documentation has fewer than {MIN_WORDS} words: {stripped!r}",
            "Expand to a short sentence that adds information beyond the name",
        )]
    return []


def validate_slice(slice_data: dict) -> list[dict]:
    findings: list[dict] = []
    for el in slice_data.get("elements", []):
        findings.extend(
            check_docs(el.get("name", ""), el.get("documentation"),
                       "element", el.get("id", "?")))
    for rel in slice_data.get("relationships", []):
        findings.extend(
            check_docs(rel.get("name", "") or "", rel.get("documentation"),
                       "relationship", rel.get("id", "?")))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slice", type=Path, help="Model-slice JSON path")
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    args = parser.parse_args(argv)
    slice_data = json.loads(args.slice.read_text(encoding="utf-8"))
    findings = validate_slice(slice_data)
    if args.json:
        print(json.dumps({"findings": findings, "ok": not findings}, indent=2))
    elif not findings:
        n_el = len(slice_data.get("elements", []))
        n_rel = len(slice_data.get("relationships", []))
        print(f"ok: 0 findings ({n_el} elements, {n_rel} relationships)")
    else:
        print(f"documentation findings: {len(findings)}")
        for f in findings:
            print(f"  - [{f['check_id']}] refs={f['object_refs']}")
            print(f"      problem: {f['problem']}")
            print(f"      proposed: {f['proposed_alternative']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
