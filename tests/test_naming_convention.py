#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Unit tests for helpers/naming_convention.py (COH-02/03)."""
from __future__ import annotations

import unittest

from helpers.naming_convention import detect_conflicts, normalize_name


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


if __name__ == "__main__":
    unittest.main()
