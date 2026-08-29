#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Unit tests for helpers/reuse_inspect.py (COH-01/03)."""
from __future__ import annotations

import unittest

from helpers.reuse_inspect import inspect_reuse, score_match


INV = [
    {"id": "e1", "name": "Customer Portal", "type": "ApplicationComponent"},
    {"id": "e2", "name": "Order Process", "type": "BusinessProcess"},
]


class ReuseInspectTests(unittest.TestCase):
    def test_exact_reuse(self) -> None:
        r = inspect_reuse(
            "Customer Portal", INV, candidate_type="ApplicationComponent"
        )
        self.assertEqual(r["decision"], "reuse")
        self.assertEqual(r["matches"][0]["id"], "e1")

    def test_create_when_absent(self) -> None:
        r = inspect_reuse(
            "Billing Engine", INV, candidate_type="ApplicationComponent"
        )
        self.assertEqual(r["decision"], "create")
        self.assertEqual(r["matches"], [])

    def test_ambiguous_duplicate_high(self) -> None:
        inv2 = [
            {"id": "a", "name": "X", "type": "T"},
            {"id": "b", "name": "X", "type": "T"},
        ]
        r = inspect_reuse("X", inv2, candidate_type="T")
        self.assertEqual(r["decision"], "ambiguous")
        self.assertEqual(len(r["matches"]), 2)

    def test_ambiguous_near_match(self) -> None:
        inv = [
            {
                "id": "p1",
                "name": "Payment Service",
                "type": "ApplicationService",
            }
        ]
        r = inspect_reuse("Payment", inv, candidate_type="ApplicationService")
        self.assertEqual(r["decision"], "ambiguous")
        self.assertTrue(r["matches"])

    def test_score_exact(self) -> None:
        self.assertEqual(score_match("A", "T", {"name": "A", "type": "T"}), 1.0)

    def test_case_insensitive_reuse(self) -> None:
        r = inspect_reuse(
            "customer portal", INV, candidate_type="ApplicationComponent"
        )
        self.assertEqual(r["decision"], "reuse")
        self.assertEqual(r["matches"][0]["id"], "e1")


if __name__ == "__main__":
    unittest.main()
