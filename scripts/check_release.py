# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Release gate (RR-B-15): required files, forbidden paths, forbidden
content, headers present. Exits non-zero on any failure.

CI (validate.yml) inlines the same checks and MUST NOT execute this file.
Run locally: python scripts/check_release.py
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

fails: list[str] = []

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
for f in REQUIRED:
    if not pathlib.Path(f).is_file():
        fails.append(f"required file missing: {f}")

tracked = subprocess.run(
    ["git", "ls-files"], capture_output=True, text=True, check=True
).stdout.splitlines()
FORBIDDEN_PATH_PARTS = [
    "__pycache__",
    ".venv",
    ".worktrees",
    ".pytest_cache",
    ".ruff_cache",
    ".bak",
]
for f in tracked:
    if any(part in f for part in FORBIDDEN_PATH_PARTS):
        fails.append(f"forbidden tracked path: {f}")

FORBIDDEN_CONTENT = [
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"CONFIDENTIAL\s+[-—]\s+Not for external distribution"),
]
for f in tracked:
    if f.startswith(".github/"):
        continue
    if not f.endswith(
        (".py", ".md", ".txt", ".yml", ".yaml", ".json", ".cff", ".html")
    ):
        continue
    text = pathlib.Path(f).read_text(encoding="utf-8", errors="ignore")
    for rx in FORBIDDEN_CONTENT:
        if rx.search(text):
            fails.append(f"forbidden content in {f}: {rx.pattern}")

HEADER_SENTINEL = "Copyright (c) 2026 JG Systems Consulting Ltd"
for f in tracked:
    if not f.endswith(".py"):
        continue
    head = pathlib.Path(f).read_text(encoding="utf-8", errors="ignore")[:600]
    if HEADER_SENTINEL not in head:
        fails.append(f"header missing: {f}")
    if "SPDX-License-Identifier" not in head:
        fails.append(f"SPDX missing: {f}")

if fails:
    print("RELEASE GATE FAILED:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("release gate: PASS")
