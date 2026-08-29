#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""List specialist skill packages (orchestrator-dispatch set). Stdlib only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ORCH = "archi-orchestrator"
USER_FACING = {ORCH}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, default=Path("skills"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    specs: list[str] = []
    if args.skills_root.is_dir():
        for child in sorted(args.skills_root.iterdir()):
            if (
                child.is_dir()
                and (child / "SKILL.md").is_file()
                and child.name not in USER_FACING
            ):
                specs.append(child.name)

    if args.json:
        print(
            json.dumps(
                {"orchestrator": ORCH, "specialists": specs, "count": len(specs)},
                indent=2,
            )
        )
    else:
        print(f"orchestrator: {ORCH}")
        print(f"specialists ({len(specs)}):")
        for name in specs:
            print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
