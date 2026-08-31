# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Tests for helpers/folder_convention.py."""
from __future__ import annotations

import unittest

from helpers.folder_convention import expected_folder, validate_slice


class FolderConventionTests(unittest.TestCase):
    def test_expected_folder_by_type(self) -> None:
        self.assertEqual(expected_folder("BusinessProcess"), "Business")
        self.assertEqual(expected_folder("ApplicationComponent"), "Application")
        self.assertEqual(expected_folder("DataObject"), "Application")
        self.assertEqual(expected_folder("Capability"), "Strategy")
        self.assertEqual(expected_folder("Goal"), "Motivation")
        self.assertEqual(expected_folder("Node"), "Technology")
        self.assertEqual(expected_folder("Equipment"), "Physical")
        self.assertEqual(expected_folder("WorkPackage"), "Implementation & Migration")
        self.assertIsNone(expected_folder("Junction"))
        self.assertIsNone(expected_folder("AndJunction"))

    def test_nested_layer_folder_passes(self) -> None:
        slice_data = {
            "elements": [{
                "id": "p1",
                "name": "Handle Inquiry",
                "type": "BusinessProcess",
                "folder_path": "Business/Processes",
            }],
            "views": [{
                "id": "v1",
                "name": "Business Process",
                "folder_path": "Views/Business Process",
            }],
        }
        self.assertEqual(validate_slice(slice_data), [])

    def test_mismatch_and_missing(self) -> None:
        slice_data = {
            "elements": [
                {"id": "p1", "name": "Handle Inquiry", "type": "BusinessProcess",
                 "folder_path": "Application"},
                {"id": "p2", "name": "Quote Shipment", "type": "BusinessProcess"},
            ],
            "views": [{"id": "v1", "name": "X", "folder_path": "Business"}],
        }
        kinds = {f["check_id"] for f in validate_slice(slice_data)}
        self.assertIn("folder_layer_mismatch", kinds)
        self.assertIn("folder_missing", kinds)
        self.assertIn("folder_view_not_under_views", kinds)

    def test_junction_in_layer_flagged(self) -> None:
        slice_data = {
            "elements": [{
                "id": "j1",
                "name": "",
                "type": "AndJunction",
                "folder_path": "Business",
            }],
            "views": [],
        }
        kinds = {f["check_id"] for f in validate_slice(slice_data)}
        self.assertIn("folder_junction_in_layer", kinds)


if __name__ == "__main__":
    unittest.main()
