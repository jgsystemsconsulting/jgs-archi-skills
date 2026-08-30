#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Rank ArchiMate viewpoint *keys* from intent axes. Stdlib only.

Candidates are fixture keys + axis tags only. Full viewpoint definitions stay on
MCP resources (archimate://recipes/*, archimate://reference/archimate-view-patterns).
Do not embed element-type or relationship catalogs here (VISION NG-4).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Axis-tagged keys only — no metamodel tables.
CANDIDATES: list[dict[str, Any]] = [
    {
        "key": "motivation",
        "label": "Motivation",
        "purposes": {"design", "decide", "inform"},
        "abstractions": {"overview", "mixed"},
        "concern_tags": {"goals", "drivers", "principles", "requirements", "outcomes", "why"},
        "stakeholder_tags": {"executive", "sponsor", "architect", "business-owner"},
    },
    {
        "key": "business-process",
        "label": "Business Process",
        "purposes": {"design", "inform"},
        "abstractions": {"detail", "mixed"},
        "concern_tags": {"process", "workflow", "service", "roles", "operations"},
        "stakeholder_tags": {"business-analyst", "process-owner", "operations"},
    },
    {
        "key": "business-product",
        "label": "Business Product",
        "purposes": {"inform", "decide"},
        "abstractions": {"overview", "mixed"},
        "concern_tags": {"product", "value", "offering", "customer"},
        "stakeholder_tags": {"product-owner", "executive", "sales"},
    },
    {
        "key": "application-structure",
        "label": "Application Structure",
        "purposes": {"design", "inform"},
        "abstractions": {"detail", "mixed"},
        "concern_tags": {"applications", "components", "interfaces", "structure", "systems"},
        "stakeholder_tags": {"application-architect", "developer", "architect"},
    },
    {
        "key": "application-cooperation",
        "label": "Application Cooperation",
        "purposes": {"design", "decide"},
        "abstractions": {"overview", "mixed"},
        "concern_tags": {"integration", "cooperation", "interfaces", "data-exchange"},
        "stakeholder_tags": {"integration-architect", "architect", "developer"},
    },
    {
        "key": "application-usage",
        "label": "Application Usage",
        "purposes": {"inform", "design"},
        "abstractions": {"mixed", "detail"},
        "concern_tags": {"usage", "support", "business-support", "services"},
        "stakeholder_tags": {"business-analyst", "application-architect"},
    },
    {
        "key": "technology",
        "label": "Technology",
        "purposes": {"design", "inform"},
        "abstractions": {"detail", "mixed"},
        "concern_tags": {"infrastructure", "nodes", "networks", "technology", "platform"},
        "stakeholder_tags": {"infrastructure", "ops", "technology-architect"},
    },
    {
        "key": "physical",
        "label": "Physical",
        "purposes": {"design", "inform"},
        "abstractions": {"detail", "mixed"},
        "concern_tags": {"facilities", "equipment", "locations", "physical"},
        "stakeholder_tags": {"facilities", "ops", "technology-architect"},
    },
    {
        "key": "implementation-migration",
        "label": "Implementation and Migration",
        "purposes": {"decide", "design"},
        "abstractions": {"overview", "mixed"},
        "concern_tags": {"roadmap", "migration", "work-packages", "plateaus", "transition"},
        "stakeholder_tags": {"program-manager", "architect", "sponsor"},
    },
    {
        "key": "layered",
        "label": "Layered",
        "purposes": {"inform", "decide"},
        "abstractions": {"overview", "mixed"},
        "concern_tags": {"landscape", "cross-layer", "alignment", "overview"},
        "stakeholder_tags": {"architect", "executive", "enterprise-architect"},
    },
    {
        "key": "capability-map",
        "label": "Capability Map",
        "purposes": {"decide", "inform"},
        "abstractions": {"overview", "mixed"},
        "concern_tags": {"capabilities", "strategy", "heat-map", "investment"},
        "stakeholder_tags": {"executive", "strategy", "enterprise-architect", "sponsor"},
    },
    {
        "key": "project",
        "label": "Project",
        "purposes": {"decide", "inform"},
        "abstractions": {"detail", "mixed"},
        "concern_tags": {"projects", "delivery", "work-packages", "timeline"},
        "stakeholder_tags": {"program-manager", "project-manager", "sponsor"},
    },
]

DEFAULT_THRESHOLD = 3
PURPOSE_ALIASES = {
    "design": "design",
    "decide": "decide",
    "decision": "decide",
    "inform": "inform",
    "communicate": "inform",
    "explain": "inform",
}
ABSTRACTION_ALIASES = {
    "overview": "overview",
    "high": "overview",
    "high-level": "overview",
    "detail": "detail",
    "detailed": "detail",
    "low": "detail",
    "mixed": "mixed",
    "both": "mixed",
}


def _tokens(values: list[str] | None) -> set[str]:
    out: set[str] = set()
    for v in values or []:
        for part in str(v).casefold().replace("_", "-").replace("/", " ").split():
            part = part.strip("-")
            if part:
                out.add(part)
                out.add(part.replace("-", ""))
    return out


def normalize_intent(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("intent must be a JSON object")
    missing = [k for k in ("stakeholders", "concerns", "purpose", "abstraction") if k not in data]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")
    if not isinstance(data["stakeholders"], list) or not isinstance(data["concerns"], list):
        raise ValueError("stakeholders and concerns must be arrays")
    purpose_raw = str(data["purpose"]).casefold().strip()
    abs_raw = str(data["abstraction"]).casefold().strip()
    purpose = PURPOSE_ALIASES.get(purpose_raw, purpose_raw)
    abstraction = ABSTRACTION_ALIASES.get(abs_raw, abs_raw)
    if purpose not in {"design", "decide", "inform"}:
        purpose = purpose_raw
    if abstraction not in {"overview", "detail", "mixed"}:
        abstraction = abs_raw
    return {
        "stakeholders": [str(s) for s in data["stakeholders"]],
        "concerns": [str(c) for c in data["concerns"]],
        "purpose": purpose,
        "abstraction": abstraction,
    }


def score_candidate(cand: dict[str, Any], intent: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0
    matched: list[str] = []
    purpose = intent["purpose"]
    abstraction = intent["abstraction"]
    if purpose in cand["purposes"]:
        score += 2
        matched.append(f"purpose:{purpose}")
    if abstraction in cand["abstractions"]:
        score += 2
        matched.append(f"abstraction:{abstraction}")
    st_tokens = _tokens(intent["stakeholders"])
    co_tokens = _tokens(intent["concerns"])
    for tag in cand["stakeholder_tags"]:
        tset = _tokens([tag])
        if st_tokens & tset:
            score += 1
            matched.append(f"stakeholder:{tag}")
    for tag in cand["concern_tags"]:
        tset = _tokens([tag])
        if co_tokens & tset:
            score += 1
            matched.append(f"concern:{tag}")
    return score, matched


def rank(intent: dict[str, Any], threshold: int = DEFAULT_THRESHOLD) -> dict[str, Any]:
    norm = normalize_intent(intent)
    ranked = []
    for cand in CANDIDATES:
        sc, matched = score_candidate(cand, norm)
        ranked.append(
            {
                "key": cand["key"],
                "label": cand["label"],
                "score": sc,
                "matched": matched,
            }
        )
    ranked.sort(key=lambda r: (-r["score"], r["key"]))
    top = ranked[0]["score"] if ranked else 0
    return {
        "ranked": ranked,
        "threshold": threshold,
        "standard_fit": top >= threshold,
        "intent": norm,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="Intent JSON file (default: stdin)")
    parser.add_argument("--list", action="store_true", help="List candidate keys as JSON")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    parser.add_argument("--top", type=int, default=0, help="If >0, only emit top N ranked")
    args = parser.parse_args(argv)

    if args.list:
        payload = {
            "candidates": [{"key": c["key"], "label": c["label"]} for c in CANDIDATES]
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.path is None:
        raw = sys.stdin.read()
        label = "<stdin>"
    else:
        if not args.path.is_file():
            print(f"error: file not found: {args.path}", file=sys.stderr)
            return 2
        raw = args.path.read_text(encoding="utf-8")
        label = str(args.path)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON in {label}: {e}", file=sys.stderr)
        return 1

    try:
        result = rank(data, threshold=args.threshold)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.top > 0:
        result = dict(result)
        result["ranked"] = result["ranked"][: args.top]
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
