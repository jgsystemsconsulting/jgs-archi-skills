# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Contract tests for JGS modelling house style (not ArchiMate reference)."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers.docs_coverage import validate_slice as validate_docs
from helpers.naming_convention import aspect_hints

DOC = ROOT / "docs" / "MODELLING_CONVENTIONS.md"
CREATE = ROOT / "docs" / "CREATE_PATH.md"
FIXTURE = ROOT / "helpers" / "fixtures" / "modelling_conventions_examples.json"

REQUIRED_H2 = [
    "## Purpose and non-goals",
    "## Naming",
    "## Element descriptions",
    "## Relationship descriptions",
    "## Folder structure",
    "## View hygiene",
    "## Overrides",
    "## Checks agents must run",
]

DENYLIST = [
    "permitted_patterns",
    "CompositionRelationship",
    "archimate://reference/archimate-relationships",
]


class ModellingConventionsDocTests(unittest.TestCase):
    def test_doc_exists(self) -> None:
        self.assertTrue(DOC.is_file(), "docs/MODELLING_CONVENTIONS.md missing")

    def test_required_headings_in_order(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        positions = [text.find(h) for h in REQUIRED_H2]
        self.assertTrue(all(p >= 0 for p in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_no_metamodel_dump_markers(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        for token in DENYLIST:
            self.assertNotIn(token, text, msg=token)

    def test_create_path_points_at_doc(self) -> None:
        text = CREATE.read_text(encoding="utf-8")
        self.assertIn("docs/MODELLING_CONVENTIONS.md", text)
        self.assertIn("House style", text)

    def test_copyright_header(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertTrue(
            text.startswith(
                "<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->"
            )
        )

    def test_skill_usage_points_at_doc(self) -> None:
        text = (ROOT / "docs" / "skill-usage.md").read_text(encoding="utf-8")
        self.assertIn("MODELLING_CONVENTIONS.md", text)

    def test_orchestrator_points_at_doc(self) -> None:
        text = (
            ROOT / "skills" / "archi-orchestrator" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("MODELLING_CONVENTIONS.md", text)


class ModellingConventionsFixtureTests(unittest.TestCase):
    def test_fixture_exists_and_has_pairs(self) -> None:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["names"]), 8)
        self.assertGreaterEqual(len(data["docs"]), 4)

    def test_name_examples_match_aspect_hints(self) -> None:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for row in data["names"]:
            hints = aspect_hints([{
                "id": row["name"],
                "name": row["name"],
                "type": row["type"],
            }])
            if row["ok"]:
                self.assertEqual(hints, [], msg=row)
            else:
                self.assertTrue(hints, msg=row)
                if row.get("hint"):
                    self.assertTrue(
                        any(h["kind"] == row["hint"] for h in hints), msg=row
                    )

    def test_doc_examples_match_docs_coverage(self) -> None:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for i, row in enumerate(data["docs"]):
            findings = validate_docs(
                {"elements": [{
                    "id": f"e{i}",
                    "name": row["name"],
                    "type": row["type"],
                    "documentation": row["documentation"],
                }], "relationships": []},
                require_evidence=True,
            )
            if row["ok"]:
                self.assertEqual(findings, [], msg=row)
            else:
                self.assertTrue(findings, msg=row)


if __name__ == "__main__":
    unittest.main()
