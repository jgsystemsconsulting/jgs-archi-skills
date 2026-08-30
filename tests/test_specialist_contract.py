#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
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
FROZEN = "17eb278636fe196928d1aa19e70e0ee919564db7fee7a23c497e8ebe5a59a1d2"

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

CREATING = [
    "archi-motivation",
    "archi-capability-strategy",
    "archi-business",
    "archi-application",
    "archi-technology-physical",
    "archi-implementation-migration",
    "archi-traceability",
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

    def test_create_path_gate_manifest(self) -> None:
        text = CREATE.read_text(encoding="utf-8")
        for gate in ("CP-G1", "CP-G2", "CP-G3", "CP-G4", "CP-G5", "CP-G6", "CP-G7"):
            self.assertIn(gate, text, msg=f"CREATE_PATH missing {gate}")
        self.assertIn("captured", text)
        self.assertIn("folded", text)
        self.assertIn("needs-user", text)
        self.assertIn("out-of-scope", text)
        self.assertIn("Evidence: stated | inferred | existing", text)
        self.assertIn("below-content", text)
        self.assertIn("export-view", text)
        self.assertIn("Deliberately Deferred", text)
        self.assertIn("Improve Next", text)

    def test_creating_specialists_have_disposition_table(self) -> None:
        for name in CREATING:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(
                "Candidate disposition",
                text,
                msg=f"{name} missing Candidate disposition",
            )
            self.assertIn("captured", text, msg=name)
            self.assertIn("folded", text, msg=name)
            self.assertIn("needs-user", text, msg=name)
            self.assertIn("out-of-scope", text, msg=name)

    def test_layout_footguns(self) -> None:
        text = (ROOT / "skills" / "archi-layout" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("export-view", text)
        self.assertIn("omit", text.casefold())
        self.assertIn("height", text.casefold())
        self.assertIn("below-content", text)
        self.assertIn("ratingBreakdown", text)
        self.assertIn("14", text)

    def test_documentation_draft_blocks(self) -> None:
        text = (
            ROOT / "skills" / "archi-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Deliberately Deferred", text)
        self.assertIn("Improve Next", text)

    def test_orchestrator_draft_checkpoint(self) -> None:
        text = (
            ROOT / "skills" / "archi-orchestrator" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Deliberately Deferred", text)
        self.assertIn("Improve Next", text)
        self.assertIn("draft", text.casefold())

    def test_model_qa_undispositioned(self) -> None:
        text = (ROOT / "skills" / "archi-model-qa" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("undispositioned", text.casefold())

    def test_elicit_inferences_survive(self) -> None:
        text = ELICIT.read_text(encoding="utf-8")
        self.assertIn("Evidence:", text)


if __name__ == "__main__":
    unittest.main()
