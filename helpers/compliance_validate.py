#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Offline compliance validation over model-slice snapshots. Stdlib only.

OBJ-5 depth beyond the thin boolean checklist. Does not call MCP. Does not
mutate the model. Every finding explains the problem and proposes a compliant
alternative (never silent-apply).

Live SoT for ArchiMate legality remains MCP resources (NG-4). The allowlist
fixture is a minimal captured snapshot for offline tests and pre-create gates.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_HELPERS = Path(__file__).resolve().parent
if str(_HELPERS) not in sys.path:
    sys.path.insert(0, str(_HELPERS))

from naming_convention import detect_conflicts, normalize_name  # noqa: E402

DEFAULT_ALLOWLIST = _HELPERS / "fixtures" / "compliance_allowlist.json"

CHECK_IDS = (
    "element_type_known",
    "relationship_type_permitted",
    "relationship_endpoints_valid",
    "abstraction_level_consistent",
    "cross_view_naming_consistent",
)


def _norm_type(t: str) -> str:
    s = re.sub(r"\s+", "", (t or "").strip())
    # strip trailing "Relationship" for comparison flexibility
    if s.lower().endswith("relationship"):
        s = s[: -len("Relationship")]
    return s


def _type_key(t: str) -> str:
    return _norm_type(t).lower()


def load_allowlist(path: Path | None = None) -> dict[str, Any]:
    p = path or DEFAULT_ALLOWLIST
    data = json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("allowlist must be a JSON object")
    return data


def _index_elements(elements: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for el in elements:
        eid = str(el.get("id") or el.get("element_id") or "")
        if eid:
            out[eid] = el
    return out


def _finding(
    check_id: str,
    object_refs: list[str],
    problem: str,
    proposed_alternative: str,
    **extra: Any,
) -> dict[str, Any]:
    f: dict[str, Any] = {
        "check_id": check_id,
        "object_refs": object_refs,
        "problem": problem,
        "proposed_alternative": proposed_alternative,
    }
    f.update(extra)
    return f


def validate_slice(
    slice_data: dict[str, Any],
    allowlist: dict[str, Any] | None = None,
    *,
    allowlist_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Validate a model-slice snapshot; return findings (empty = pass).

    slice_data keys:
      elements: [{id, name, type, abstraction?}, ...]
      relationships: [{id?, type, source, target}, ...]
      view_usages?: [{view_id, element_id, name?, type?}, ...]
    """
    al = allowlist if allowlist is not None else load_allowlist(allowlist_path)
    elements = list(slice_data.get("elements") or [])
    relationships = list(slice_data.get("relationships") or [])
    view_usages = list(slice_data.get("view_usages") or slice_data.get("usages") or [])

    known_types = {_type_key(t) for t in (al.get("element_types") or [])}
    # preserve canonical casing map
    type_canon = {_type_key(t): t for t in (al.get("element_types") or [])}

    rel_types_raw = al.get("relationship_types") or []
    known_rels = {_type_key(t) for t in rel_types_raw}
    rel_canon = {_type_key(t): _norm_type(t) for t in rel_types_raw}

    patterns: set[tuple[str, str, str]] = set()
    for pat in al.get("permitted_patterns") or []:
        patterns.add(
            (
                _type_key(str(pat.get("source", ""))),
                _type_key(str(pat.get("relationship", ""))),
                _type_key(str(pat.get("target", ""))),
            )
        )

    abs_map_raw = al.get("abstraction_levels") or {}
    abs_map = {_type_key(k): str(v).lower() for k, v in abs_map_raw.items()}

    by_id = _index_elements(elements)
    findings: list[dict[str, Any]] = []

    # --- element types ---
    for el in elements:
        eid = str(el.get("id") or el.get("element_id") or "?")
        et = str(el.get("type") or el.get("element_type") or "")
        tk = _type_key(et)
        if not tk:
            findings.append(
                _finding(
                    "element_type_known",
                    [eid],
                    f"Element {eid!r} has empty type.",
                    "Set a known ArchiMate element type from MCP archimate-layers "
                    f"(offline allowlist examples: {sorted(type_canon.values())[:5]}…).",
                )
            )
        elif tk not in known_types:
            findings.append(
                _finding(
                    "element_type_known",
                    [eid],
                    f"Element type {et!r} is not in the offline allowlist.",
                    "Replace with a known type from MCP archimate-layers / fixture "
                    f"(e.g. ApplicationComponent, BusinessProcess). Do not invent types.",
                    element_type=et,
                )
            )

    # --- relationships ---
    for rel in relationships:
        rid = str(rel.get("id") or rel.get("relationship_id") or "?")
        rtype = str(rel.get("type") or rel.get("relationship_type") or "")
        src = str(rel.get("source") or rel.get("source_id") or "")
        tgt = str(rel.get("target") or rel.get("target_id") or "")
        rk = _type_key(rtype)
        refs = [rid, src, tgt]

        if not rk or rk not in known_rels:
            findings.append(
                _finding(
                    "relationship_type_permitted",
                    refs,
                    f"Relationship type {rtype!r} is not permitted by the offline allowlist.",
                    "Use a permitted ArchiMate relationship type from MCP "
                    "archimate-relationships (e.g. Serving, Realization, Assignment). "
                    "Do not silent-apply an illegal type.",
                    relationship_type=rtype,
                )
            )
            # still try endpoints if types known
        src_el = by_id.get(src)
        tgt_el = by_id.get(tgt)
        if src_el is None or tgt_el is None:
            missing = []
            if src_el is None:
                missing.append(f"source={src!r}")
            if tgt_el is None:
                missing.append(f"target={tgt!r}")
            findings.append(
                _finding(
                    "relationship_endpoints_valid",
                    refs,
                    f"Relationship endpoints not found in slice elements ({', '.join(missing)}).",
                    "Point source/target at existing element IDs in the model slice, "
                    "or include the missing elements before relating.",
                )
            )
            continue

        st = _type_key(str(src_el.get("type") or src_el.get("element_type") or ""))
        tt = _type_key(str(tgt_el.get("type") or tgt_el.get("element_type") or ""))
        if rk and rk in known_rels and st and tt:
            trip = (st, rk, tt)
            if patterns and trip not in patterns:
                sc = type_canon.get(st, st)
                tc = type_canon.get(tt, tt)
                rc = rel_canon.get(rk, rtype)
                # suggest any pattern with same source type, else generic
                alts = [
                    p
                    for p in patterns
                    if p[0] == st or p[2] == tt
                ][:3]
                if alts:
                    alt_txt = "; ".join(
                        f"{type_canon.get(a[0], a[0])} -{rel_canon.get(a[1], a[1])}-> "
                        f"{type_canon.get(a[2], a[2])}"
                        for a in alts
                    )
                    proposal = (
                        f"Illegal combo {sc} -{rc}-> {tc}. Prefer a permitted pattern "
                        f"such as: {alt_txt}. Confirm full legality via MCP "
                        "archimate-relationships before create-relationship."
                    )
                else:
                    proposal = (
                        f"Illegal combo {sc} -{rc}-> {tc} for this offline fixture. "
                        "Choose a permitted source/type/target triple from MCP "
                        "archimate-relationships; do not silent-apply."
                    )
                findings.append(
                    _finding(
                        "relationship_endpoints_valid",
                        refs,
                        f"Relationship endpoints {sc} -{rc}-> {tc} are not a permitted pattern.",
                        proposal,
                        source_type=sc,
                        target_type=tc,
                        relationship_type=rc,
                    )
                )

    # --- abstraction consistency ---
    for el in elements:
        eid = str(el.get("id") or el.get("element_id") or "?")
        et = str(el.get("type") or el.get("element_type") or "")
        tk = _type_key(et)
        declared = el.get("abstraction") or el.get("abstraction_level") or el.get("layer")
        if declared is None or declared == "":
            continue
        expected = abs_map.get(tk)
        if expected is None:
            continue
        if str(declared).strip().lower() != expected:
            findings.append(
                _finding(
                    "abstraction_level_consistent",
                    [eid],
                    f"Element {eid} type {et!r} declares abstraction {declared!r} "
                    f"but fixture expects {expected!r}.",
                    f"Set abstraction/layer to {expected!r} for type {type_canon.get(tk, et)}, "
                    "or correct the element type to match the intended layer.",
                    declared=str(declared),
                    expected=expected,
                )
            )

    # also: relationship crossing wildly inconsistent layers without Association
    for rel in relationships:
        rid = str(rel.get("id") or "?")
        src = str(rel.get("source") or rel.get("source_id") or "")
        tgt = str(rel.get("target") or rel.get("target_id") or "")
        rtype = str(rel.get("type") or rel.get("relationship_type") or "")
        src_el, tgt_el = by_id.get(src), by_id.get(tgt)
        if not src_el or not tgt_el:
            continue
        st = _type_key(str(src_el.get("type") or src_el.get("element_type") or ""))
        tt = _type_key(str(tgt_el.get("type") or tgt_el.get("element_type") or ""))
        sa, ta = abs_map.get(st), abs_map.get(tt)
        if not sa or not ta:
            continue
        if sa == ta or sa == "cross" or ta == "cross":
            continue
        # adjacent layers ok; distant jump without Influence/Association/Realization flagged lightly
        layer_order = [
            "motivation",
            "strategy",
            "business",
            "application",
            "technology",
            "physical",
            "implementation",
        ]
        try:
            di = abs(layer_order.index(sa) - layer_order.index(ta))
        except ValueError:
            continue
        rk = _type_key(rtype)
        soft_ok = rk in {
            "influence",
            "association",
            "realization",
            "serving",
            "aggregation",
            "composition",
            "flow",
            "triggering",
            "access",
            "assignment",
            "specialization",
        }
        if di >= 3 and not soft_ok:
            findings.append(
                _finding(
                    "abstraction_level_consistent",
                    [rid, src, tgt],
                    f"Relationship spans distant layers ({sa} → {ta}) with type {rtype!r}.",
                    "Prefer Realization/Serving/Influence/Association across layers, "
                    "or introduce intermediate elements; confirm with MCP recipes.",
                )
            )

    # --- cross-view naming ---
    if view_usages:
        # enrich usages with element names/types when missing
        enriched: list[dict[str, Any]] = []
        for u in view_usages:
            eid = str(u.get("id") or u.get("element_id") or "")
            el = by_id.get(eid, {})
            name = str(u.get("name") or el.get("name") or "")
            et = str(
                u.get("type")
                or u.get("element_type")
                or el.get("type")
                or el.get("element_type")
                or ""
            )
            enriched.append(
                {
                    "id": eid,
                    "element_id": eid,
                    "name": name,
                    "type": et,
                    "view": u.get("view") or u.get("view_id") or u.get("view_name"),
                }
            )
        for c in detect_conflicts(enriched):
            refs = []
            if c.get("element_id"):
                refs.append(str(c["element_id"]))
            refs.extend(str(x) for x in (c.get("element_ids") or []))
            kind = c.get("kind", "naming")
            problem = (
                f"Naming conflict ({kind}): names={c.get('names')}, "
                f"normalized={c.get('normalized')}, views={c.get('views')}"
            )
            proposal = str(
                c.get("proposal")
                or "Unify display names via update-element; reuse one ID across views."
            )
            # ensure proposal mentions normalize when divergence
            if kind == "cross_view_name_divergence" and "normalize" not in proposal.lower():
                sample = ""
                names = c.get("names") or []
                if names:
                    sample = f" Canonical example: {normalize_name(str(names[0]))!r}."
                proposal = proposal.rstrip(".") + "." + sample
            findings.append(
                _finding(
                    "cross_view_naming_consistent",
                    refs or ["?"],
                    problem,
                    proposal,
                    naming_kind=kind,
                )
            )

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slice", type=Path, help="Model-slice JSON path")
    parser.add_argument(
        "--allowlist",
        type=Path,
        default=None,
        help="Allowlist fixture path (default: helpers/fixtures/compliance_allowlist.json)",
    )
    parser.add_argument("--json", action="store_true", help="Emit findings as JSON")
    args = parser.parse_args(argv)
    slice_data = json.loads(args.slice.read_text(encoding="utf-8"))
    findings = validate_slice(slice_data, allowlist_path=args.allowlist)
    if args.json:
        print(json.dumps({"findings": findings, "ok": not findings}, indent=2))
    elif not findings:
        print(f"ok: 0 findings ({len(CHECK_IDS)} check dimensions)")
    else:
        print(f"compliance findings: {len(findings)}")
        for f in findings:
            print(f"  - [{f['check_id']}] refs={f['object_refs']}")
            print(f"      problem: {f['problem']}")
            print(f"      proposed: {f['proposed_alternative']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
