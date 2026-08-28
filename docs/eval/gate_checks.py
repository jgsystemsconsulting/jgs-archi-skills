#!/usr/bin/env python3
"""Gate checks for the eval loop (GATES.md G1, G8, G9 oracles). Stdlib only.

Subcommands:
  scenario      frozen scenario file is complete (G1)
  iterations    iteration logs are complete (G8)
  confirmation  re-run all model-quality helpers on the confirmation dir (G9)
Prints a success-only marker after every assertion passes; exits 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "docs" / "evidence" / "eval-loop"

REQUIRED_SECTIONS = ["## Problem", "## Stakeholders", "## Drivers", "## Goals",
                     "## Expected Views", "## Quality Expectations"]
VIEW_NAMES = ["Motivation Overview", "Capability Map", "Customer Service Operations",
              "Application Support", "Technology Platform", "End-to-End Traceability"]


def fail(msg: str):
    print(f"gate_checks FAIL: {msg}")
    raise SystemExit(1)


def cmd_scenario() -> None:
    path = ROOT / "docs" / "eval" / "reference-scenario.md"
    if not path.exists():
        fail(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    if "FROZEN" not in text:
        fail("scenario is not marked FROZEN")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(f"scenario missing required section {section!r}")
    for vname in VIEW_NAMES:
        if vname not in text:
            fail(f"scenario missing expected view name {vname!r}")
    print("scenario check passed")


def cmd_iterations() -> None:
    logs = sorted(EVAL.glob("ITERATION-*.md"))
    if not logs:
        fail("no ITERATION-*.md logs under docs/evidence/eval-loop")
    for log in logs:
        text = log.read_text(encoding="utf-8")
        for section in ("## Scores", "## Skill Changes", "## Evidence"):
            if section not in text:
                fail(f"{log.name} missing section {section!r}")
    if not (EVAL / "iter-final").exists():
        fail("docs/evidence/eval-loop/iter-final does not exist (final run not recorded)")
    print("iterations check passed")


def run_helper(cmd: list[str], expect: str) -> None:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    combined = p.stdout + p.stderr
    if p.returncode != 0:
        fail(f"{' '.join(cmd)} exited {p.returncode}: {combined.strip()[:400]}")
    if expect not in combined:
        fail(f"{' '.join(cmd)} output missing {expect!r}: {combined.strip()[:400]}")


def cmd_confirmation() -> None:
    d = EVAL / "iter-confirm"
    for name in ("slice.json", "usages.json", "views.json"):
        if not (d / name).exists():
            fail(f"iter-confirm/{name} missing (confirmation run not exported)")
    if not (d / "rationale").is_dir() or not list((d / "rationale").glob("*.md")):
        fail("iter-confirm/rationale has no .md files")
    py = sys.executable
    run_helper([py, "helpers/compliance_validate.py", "--json", str(d / "slice.json")],
               '"ok": true')
    run_helper([py, "helpers/naming_convention.py", "conflicts", str(d / "usages.json")],
               '"conflict_count": 0')
    run_helper([py, "helpers/rationale_schema.py", "--bundle", str(d / "rationale"),
                "--json"], '"findings": []')
    run_helper([py, "helpers/docs_coverage.py", "--json", str(d / "slice.json")],
               '"ok": true')
    run_helper([py, "helpers/layout_check.py", "--json", str(d / "views.json")],
               '"ok": true')
    print("confirmation check passed")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["scenario", "iterations", "confirmation"])
    args = ap.parse_args()
    {"scenario": cmd_scenario, "iterations": cmd_iterations,
     "confirmation": cmd_confirmation}[args.command]()


if __name__ == "__main__":
    main()
