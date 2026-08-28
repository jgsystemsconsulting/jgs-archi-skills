#!/usr/bin/env python3
"""Regression for shared specialist contract (Phase 9 / SPEC-D-*)."""
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREATE = ROOT / "docs" / "CREATE_PATH.md"
ELICIT = ROOT / "skills" / "archi-elicit" / "SKILL.md"
VSEL = ROOT / "skills" / "archi-viewpoint-select" / "SKILL.md"
# Digest over the canonical LF bytes as stored in git; Windows checkouts use
# CRLF in the working tree, so line endings are normalized before hashing.
FROZEN = "95c18a9ac4407d09352b47fc1a3887148353e7a6c09f020dbba5bf1a320b623f"

MUTATING = [
    "archi-motivation",
    "archi-capability-strategy",
    "archi-business",
    "archi-application",
    "archi-technology-physical",
    "archi-implementation-migration",
    "archi-traceability",
    "archi-model-qa",
    "archi-layout",
    "archi-documentation",
]


class SpecialistContractTests(unittest.TestCase):
    def test_create_path_markers(self) -> None:
        text = CREATE.read_text(encoding="utf-8")
        self.assertIn("View Plan confirmation", text)
        self.assertIn("SPEC-02", text)
        self.assertIn("NG-4", text)
        self.assertIn("shared specialist", text.lower())

    def test_elicit_complete(self) -> None:
        text = ELICIT.read_text(encoding="utf-8")
        self.assertIn("## Purpose", text)
        self.assertIn("No MCP mutations", text)
        self.assertNotIn("Contract stub", text)
        self.assertIn("Normalized Intent", text)

    def test_mutating_reference_create_path(self) -> None:
        for name in MUTATING:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(
                "docs/CREATE_PATH.md",
                text,
                msg=f"{name} missing CREATE_PATH reference",
            )
            self.assertIn("View Plan confirmation", text)

    def test_specialists_not_stubs(self) -> None:
        for name in MUTATING:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Purpose", text, msg=name)
            self.assertIn("## Procedure", text, msg=name)
            self.assertNotIn("Contract stub for suite completeness", text, msg=name)

    def test_create_path_obj4_coherence(self) -> None:
        text = CREATE.read_text(encoding="utf-8")
        self.assertIn("Model coherence and reuse", text)
        self.assertIn("reuse_registry", text)
        self.assertIn("ambiguous", text.lower())

    def test_viewpoint_select_frozen(self) -> None:
        digest = hashlib.sha256(
            VSEL.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        self.assertEqual(digest, FROZEN)


if __name__ == "__main__":
    unittest.main()
