#!/usr/bin/env python3
"""Install in-repo ZCode skills to ~/.zcode/skills/.

Stdlib only. Discovers skills/*/SKILL.md and copies (or optionally links) each package.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def discover_skills(skills_root: Path) -> list[Path]:
    if not skills_root.is_dir():
        return []
    found: list[Path] = []
    for child in sorted(skills_root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            found.append(child)
    return found


def install_one(src: Path, dest_root: Path, link: bool) -> Path:
    dest = dest_root / src.name
    dest_root.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        # Only replace prior skill installs (must contain SKILL.md).
        if (dest / "SKILL.md").is_file() or dest.is_symlink():
            if dest.is_symlink() or dest.is_file():
                dest.unlink()
            else:
                shutil.rmtree(dest)
        else:
            raise SystemExit(
                f"refusing to overwrite non-skill path: {dest}"
            )

    if link:
        try:
            os.symlink(src.resolve(), dest, target_is_directory=True)
            return dest
        except OSError as exc:
            print(
                f"notice: --link failed ({exc}); falling back to copy for {src.name}",
                file=sys.stderr,
            )

    shutil.copytree(src, dest)
    return dest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=Path(__file__).resolve().parent / "skills",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path.home() / ".zcode" / "skills",
    )
    parser.add_argument(
        "--link",
        action="store_true",
        help="Try symlink (Unix); on failure or Windows without privilege, copy",
    )
    args = parser.parse_args(argv)

    skills = discover_skills(args.skills_root)
    if not skills:
        print("no skills to install")
        return 0

    for skill in skills:
        dest = install_one(skill, args.dest, link=args.link)
        print(f"installed {skill.name} -> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
