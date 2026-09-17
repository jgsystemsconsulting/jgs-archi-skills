# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Release gate (RR-B-15). Run locally: python scripts/check_release.py

Local coverage: required files, forbidden tracked paths, forbidden-content
leak sentinels, Python headers and SPDX, UTF-8 BOM in parser-critical files,
version consistency across the six version-bearing sources, and SKILL.md
frontmatter lint.

CI (.github/workflows/validate.yml) runs equivalent inline checks and is the
authority. CI must not execute checkout code, so the two implementations are
kept in sync by comment cross-references in this file, not by shared code.

Both sides skip `.github/` in the content scan because workflow files
legitimately discuss secret plumbing. Residual risk: a real secret pasted
into a workflow file, or into an unscanned file extension, passes this gate.

Exits non-zero on any failure.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

REQUIRED = [
    "LICENSE",
    "COPYRIGHT",
    "NOTICE",
    "README.md",
    "CHANGELOG.md",
    "RELEASE-INFO.txt",
    "CITATION.cff",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".gitignore",
    "SKILLS.md",
    "docs/skill-usage.md",
    "docs/prompts/README.md",
    "docs/other-agents.md",
    "docs/MCP.md",
    "docs/MODELLING_CONVENTIONS.md",
    "install.py",
    "install.sh",
    "install.ps1",
    ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json",
    ".cursor-plugin/marketplace.json",
    ".cursor-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "gemini-extension.json",
]

FORBIDDEN_PATH_PARTS = [
    "__pycache__",
    ".venv",
    ".worktrees",
    ".pytest_cache",
    ".ruff_cache",
    ".bak",
]

# keep in sync with .github/workflows/validate.yml (Forbidden content)
FORBIDDEN_CONTENT = [
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"CONFIDENTIAL\s+[-—]\s+Not for external distribution"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"),
]

HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd"


def tracked_files(cwd: pathlib.Path | None = None) -> list[str]:
    """Git-tracked files relative to cwd.

    Fails closed: any git failure or an empty listing raises RuntimeError.
    """
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(cwd) if cwd is not None else None,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        detail = getattr(exc, "stderr", None)
        if isinstance(detail, str) and detail.strip():
            msg = detail.strip()
        else:
            msg = str(exc)
        raise RuntimeError(f"git ls-files failed: {msg}") from exc
    tracked = proc.stdout.splitlines()
    if not tracked:
        raise RuntimeError("git ls-files returned no files; refusing to pass")
    return tracked


def check_required_files(root: pathlib.Path) -> list[str]:
    return [
        f"required file missing: {f}"
        for f in REQUIRED
        if not (root / f).is_file()
    ]


def check_forbidden_paths(tracked: list[str]) -> list[str]:
    return [
        f"forbidden tracked path: {f}"
        for f in tracked
        if any(part in f for part in FORBIDDEN_PATH_PARTS)
    ]


def check_forbidden_content(root: pathlib.Path, tracked: list[str]) -> list[str]:
    fails: list[str] = []
    for f in tracked:
        if f.startswith(".github/"):
            continue
        if not f.endswith(
            (".py", ".md", ".txt", ".yml", ".yaml", ".json", ".cff", ".html")
        ):
            continue
        text = (root / f).read_text(encoding="utf-8", errors="ignore")
        for rx in FORBIDDEN_CONTENT:
            if rx.search(text):
                fails.append(f"forbidden content in {f}: {rx.pattern}")
    return fails


def check_headers(root: pathlib.Path, tracked: list[str]) -> list[str]:
    fails: list[str] = []
    for f in tracked:
        if not f.endswith(".py"):
            continue
        head = (root / f).read_text(encoding="utf-8", errors="ignore")[:600]
        if HEADER_SENTINEL not in head:
            fails.append(f"header missing: {f}")
        if "SPDX-License-Identifier" not in head:
            fails.append(f"SPDX missing: {f}")
    return fails


# keep in sync with .github/workflows/validate.yml (BOM check)
# Local difference: tracked files only, because a local checkout has .venv/
# with hundreds of vendored .json files a blind rglob would drown the signal.
# On a clean checkout tracked files and rglob agree, so parity holds in CI.
def check_bom(root: pathlib.Path, tracked: list[str]) -> list[str]:
    fails: list[str] = []
    for f in tracked:
        if not f.endswith((".toml", ".json", ".yaml", ".yml", ".cff")):
            continue
        if (root / f).read_bytes()[:3] == b"\xef\xbb\xbf":
            fails.append(f"UTF-8 BOM in parser-critical file: {f}")
    return fails


# keep in sync with .github/workflows/validate.yml (Version consistency)
def check_versions(root: pathlib.Path) -> list[str]:
    def changelog_top() -> str | None:
        p = root / "CHANGELOG.md"
        if not p.is_file():
            return None
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^##\s*\[?v?(\d+\.\d+\.\d+)", t, re.M)
        return m.group(1) if m else None

    def release_info() -> str | None:
        p = root / "RELEASE-INFO.txt"
        if not p.is_file():
            return None
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^Version:\s*(\d+\.\d+\.\d+)", t, re.M)
        return m.group(1) if m else None

    def citation() -> str | None:
        p = root / "CITATION.cff"
        if not p.is_file():
            return None
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", t, re.M)
        return m.group(1) if m else None

    def plugin(path: str) -> str | None:
        p = root / path
        if not p.is_file():
            return None
        return json.loads(p.read_text(encoding="utf-8")).get("version")

    vals = {
        "CHANGELOG": changelog_top(),
        "RELEASE-INFO": release_info(),
        "CITATION.cff": citation(),
        "claude plugin.json": plugin(".claude-plugin/plugin.json"),
        "cursor plugin.json": plugin(".cursor-plugin/plugin.json"),
        "gemini-extension.json": plugin("gemini-extension.json"),
    }
    uniq = {v for v in vals.values() if v}
    if None in vals.values() or len(uniq) != 1:
        return [f"version mismatch across sources: {vals}"]
    return []


# keep in sync with .github/workflows/validate.yml (SKILL.md frontmatter lint)
def check_frontmatter(root: pathlib.Path) -> list[str]:
    fails: list[str] = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        return ["no skills/*/SKILL.md found"]
    for p in skills:
        t = p.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", t, re.S)
        if not m:
            fails.append(f"{p.relative_to(root).as_posix()}: missing YAML frontmatter")
            continue
        fm = m.group(1)
        body = t[m.end():]
        nm = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not nm:
            fails.append(f"{p.relative_to(root).as_posix()}: frontmatter missing name")
        else:
            name = nm.group(1).strip().strip('"').strip("'")
            if name != p.parent.name:
                fails.append(
                    f"{p.relative_to(root).as_posix()}: name {name!r} != dir {p.parent.name!r}"
                )
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                fails.append(
                    f"{p.relative_to(root).as_posix()}: name not kebab-case: {name}"
                )
        if not re.search(r"^description:\s*\S", fm, re.M):
            fails.append(
                f"{p.relative_to(root).as_posix()}: frontmatter missing description"
            )
        if "## When to use" not in body:
            fails.append(f"{p.relative_to(root).as_posix()}: missing ## When to use")
        if not re.search(r"Prerequisites|Requirements|^compatibility:", body, re.M):
            fails.append(
                f"{p.relative_to(root).as_posix()}: missing prerequisites marker"
            )
    return fails


def main() -> int:
    root = pathlib.Path(".")
    try:
        tracked = tracked_files()
    except RuntimeError as exc:
        print(f"RELEASE GATE FAILED:\n  - {exc}")
        return 1
    fails: list[str] = []
    fails += check_required_files(root)
    fails += check_forbidden_paths(tracked)
    fails += check_forbidden_content(root, tracked)
    fails += check_headers(root, tracked)
    fails += check_bom(root, tracked)
    fails += check_versions(root)
    fails += check_frontmatter(root)
    if fails:
        print("RELEASE GATE FAILED:")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("release gate: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
