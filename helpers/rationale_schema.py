#!/usr/bin/env python3
"""Validate structured view rationale markdown sections. Stdlib only."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    text = args.path.read_text(encoding="utf-8")
    missing = missing_headings(text)
    if missing:
        print("missing rationale sections:")
        for heading in missing:
            print(f"  ## {heading}")
        return 1
    print(f"ok: rationale has {len(REQUIRED)} sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
