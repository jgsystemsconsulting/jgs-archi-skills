# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Idempotently prepend org headers to first-party .py and .md (RR-B-03/04)."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY_HEADER = (
    "# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.\n"
    "# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary\n"
)
MD_HEADER = (
    "<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->\n"
    "<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->\n"
)
SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd"


def tracked() -> list[str]:
    return subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()


def header_py(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if SENTINEL in text[:600]:
        return
    if text.startswith("#!"):
        nl = text.find("\n")
        shebang = text[: nl + 1] if nl != -1 else text + "\n"
        rest = text[len(shebang) :]
        path.write_text(shebang + PY_HEADER + rest, encoding="utf-8")
    else:
        path.write_text(PY_HEADER + text, encoding="utf-8")
    print(f"headered {path.relative_to(ROOT)}")


def header_md(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if SENTINEL in text[:800]:
        return
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            close = end + 4
            if close < len(text) and text[close] == "\n":
                close += 1
            new = text[:close] + MD_HEADER + "\n" + text[close:].lstrip("\n")
            path.write_text(new, encoding="utf-8")
            print(f"headered-fm {path.relative_to(ROOT)}")
            return
    path.write_text(MD_HEADER + "\n" + text.lstrip("\n"), encoding="utf-8")
    print(f"headered {path.relative_to(ROOT)}")


def main() -> None:
    for rel in tracked():
        path = ROOT / rel
        if not path.is_file():
            continue
        if rel.endswith(".py"):
            header_py(path)
        elif rel.endswith(".md"):
            header_md(path)


if __name__ == "__main__":
    main()
