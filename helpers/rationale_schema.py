#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Validate structured view rationale markdown sections. Stdlib only.

OBJ-6 depth: required sections present, non-empty bodies, multi-view bundles.
Does not call MCP. Does not mutate the model.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = [
    "Purpose",
    "Stakeholders and Concerns",
    "Viewpoint",
    "Questions Answered",
    "Assumptions",
    "Decisions",
    "Exclusions",
    "Open Questions",
]
H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)


def missing_headings(text: str) -> list[str]:
    found = {m.group(1).strip() for m in H2.finditer(text)}
    return [h for h in REQUIRED if h not in found]


def _section_bodies(text: str) -> dict[str, str]:
    matches = list(H2.finditer(text))
    bodies: dict[str, str] = {}
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        bodies[title] = text[start:end]
    return bodies


def _finding(
    check_id: str,
    problem: str,
    *,
    view_id: str | None = None,
    section: str | None = None,
    severity: str = "error",
) -> dict[str, Any]:
    f: dict[str, Any] = {
        "check_id": check_id,
        "problem": problem,
        "severity": severity,
    }
    if view_id is not None:
        f["view_id"] = view_id
    if section is not None:
        f["section"] = section
    return f


def validate_rationale(
    text: str, *, view_id: str | None = None, check_order: bool = True
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    bodies = _section_bodies(text)
    found_titles = list(bodies.keys())

    for req in REQUIRED:
        if req not in bodies:
            findings.append(
                _finding(
                    "missing_section",
                    f"missing required section ## {req}",
                    view_id=view_id,
                    section=req,
                )
            )
            continue
        body = bodies[req].strip()
        if not body or body in {"-", "*", "\u2026", "..."}:
            findings.append(
                _finding(
                    "empty_section",
                    f"section ## {req} has empty body",
                    view_id=view_id,
                    section=req,
                )
            )

    if check_order:
        present_required = [t for t in found_titles if t in REQUIRED]
        expected_order = [r for r in REQUIRED if r in bodies]
        if present_required != expected_order and not missing_headings(text):
            findings.append(
                _finding(
                    "order_warning",
                    "required sections present but not in canonical order",
                    view_id=view_id,
                    severity="warn",
                )
            )

    return findings


def validate_bundle(bundle: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    if isinstance(bundle, list):
        views = bundle
    else:
        views = bundle.get("views") or []
    all_findings: list[dict[str, Any]] = []
    for v in views:
        vid = str(v.get("id") or v.get("view_id") or v.get("name") or "")
        if "text" in v and v["text"] is not None:
            text = str(v["text"])
        elif "path" in v and v["path"]:
            text = Path(v["path"]).read_text(encoding="utf-8")
        else:
            all_findings.append(
                _finding(
                    "missing_section",
                    "view entry has neither text nor path",
                    view_id=vid or None,
                )
            )
            continue
        all_findings.extend(validate_rationale(text, view_id=vid or None))
    return all_findings


def validate_bundle_dir(dir_path: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    paths = sorted(p for p in Path(dir_path).glob("*.md") if p.is_file())
    if not paths:
        return [
            _finding(
                "missing_section",
                f"no markdown files in bundle dir {dir_path}",
            )
        ]
    for p in paths:
        text = p.read_text(encoding="utf-8")
        findings.extend(validate_rationale(text, view_id=p.stem))
    return findings


def _error_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [f for f in findings if f.get("severity", "error") != "warn"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, nargs="?", help="single rationale markdown file")
    parser.add_argument("--bundle", type=Path, help="directory of *.md files or a JSON bundle file")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    args = parser.parse_args(argv)

    findings: list[dict[str, Any]] = []

    if args.bundle:
        b = args.bundle
        if b.is_dir():
            findings = validate_bundle_dir(b)
        else:
            data = json.loads(b.read_text(encoding="utf-8"))
            findings = validate_bundle(data)
    elif args.path:
        text = args.path.read_text(encoding="utf-8")
        missing = missing_headings(text)
        findings = validate_rationale(text)
        if not args.json:
            errs = _error_findings(findings)
            if errs:
                only_missing = all(f["check_id"] == "missing_section" for f in errs)
                if only_missing and missing:
                    print("missing rationale sections:")
                    for heading in missing:
                        print(f"  ## {heading}")
                else:
                    print("rationale findings:")
                    for f in errs:
                        sec = f.get("section")
                        extra = f" ({sec})" if sec else ""
                        print(f"  [{f['check_id']}]{extra} {f['problem']}")
                return 1
            print(f"ok: rationale has {len(REQUIRED)} sections")
            return 0
    else:
        parser.error("provide path or --bundle")

    if args.json:
        print(json.dumps({"findings": findings}, indent=2))
    else:
        errs = _error_findings(findings)
        if errs:
            print("rationale findings:")
            for f in errs:
                vid = f.get("view_id")
                prefix = f"view={vid} " if vid else ""
                print(f"  {prefix}[{f['check_id']}] {f['problem']}")
            return 1
        kind = "bundle" if args.bundle else "file"
        print(f"ok: rationale {kind} valid ({len(REQUIRED)} sections)")
    return 0 if not _error_findings(findings) else 1


if __name__ == "__main__":
    raise SystemExit(main())
