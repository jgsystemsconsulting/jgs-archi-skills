#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Unit tests for helpers/naming_convention.py (COH-02/03)."""
from __future__ import annotations

import unittest

from helpers.naming_convention import aspect_hints, detect_conflicts, normalize_name


class NamingConventionTests(unittest.TestCase):
    def test_normalize_collapse_and_title(self) -> None:
        self.assertEqual(normalize_name("  customer   portal  "), "Customer Portal")

    def test_normalize_small_words(self) -> None:
        self.assertEqual(normalize_name("order of service"), "Order of Service")

    def test_cross_view_divergence(self) -> None:
        usages = [
            {"id": "e1", "name": "Customer Portal", "view": "App Structure"},
            {"id": "e1", "name": "customer portal app", "view": "App Usage"},
        ]
        c = detect_conflicts(usages)
        kinds = {x["kind"] for x in c}
        self.assertIn("cross_view_name_divergence", kinds)

    def test_duplicate_label(self) -> None:
        usages = [
            {"id": "a", "name": "Billing", "type": "BusinessService", "view": "v1"},
            {"id": "b", "name": "billing", "type": "BusinessService", "view": "v2"},
        ]
        c = detect_conflicts(usages)
        kinds = {x["kind"] for x in c}
        self.assertIn("duplicate_label", kinds)

    def test_clean_usages(self) -> None:
        usages = [
            {
                "id": "e1",
                "name": "Customer Portal",
                "view": "v1",
                "type": "ApplicationComponent",
            },
            {
                "id": "e1",
                "name": "Customer Portal",
                "view": "v2",
                "type": "ApplicationComponent",
            },
        ]
        self.assertEqual(detect_conflicts(usages), [])



    def test_structure_type_suffix_hint(self) -> None:
        hints = aspect_hints([
            {"id": "a", "name": "CRM Application", "type": "ApplicationComponent"},
        ])
        self.assertTrue(any(h["kind"] == "structure_type_suffix" for h in hints))

    def test_acronym_skips_structure_hint(self) -> None:
        hints = aspect_hints([
            {"id": "a", "name": "CRM", "type": "ApplicationComponent"},
        ])
        self.assertEqual(hints, [])

    def test_behaviour_single_noun_hint(self) -> None:
        hints = aspect_hints([
            {"id": "p", "name": "Invoice", "type": "BusinessProcess"},
        ])
        self.assertTrue(any(h["kind"] == "behaviour_not_verb_noun" for h in hints))

    def test_behaviour_verb_noun_clean(self) -> None:
        hints = aspect_hints([
            {"id": "p", "name": "Handle Customer Inquiry", "type": "BusinessProcess"},
        ])
        self.assertEqual(hints, [])

    def test_aspect_hints_never_rename(self) -> None:
        hints = aspect_hints([
            {"id": "a", "name": "CRM Application", "type": "ApplicationComponent"},
        ])
        self.assertTrue(hints)
        self.assertNotIn("normalized", hints[0])

    def test_aspect_hints_cli(self) -> None:
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "u.json"
            p.write_text(json.dumps([
                {"id": "a", "name": "CRM Application", "type": "ApplicationComponent"},
            ]), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(root / "helpers" / "naming_convention.py"),
                 "aspect-hints", str(p)],
                capture_output=True, text=True, cwd=str(root),
            )
            self.assertNotEqual(proc.returncode, 0)
            data = json.loads(proc.stdout)
            self.assertGreater(data["hint_count"], 0)
            self.assertIn("hints", data)
            self.assertNotIn("conflicts", data)



if __name__ == "__main__":
    unittest.main()
