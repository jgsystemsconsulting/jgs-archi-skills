# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: LicenseRef-JGSC-Proprietary
"""Tests for helpers/docs_coverage.py (eval-loop documentation gate)."""
import unittest

from helpers.docs_coverage import validate_slice


def sl(elements=(), relationships=()):
    return {"elements": list(elements), "relationships": list(relationships)}


class TestDocsCoverage(unittest.TestCase):
    def test_clean_slice_passes(self):
        slice_data = sl(
            [{"id": "e1", "name": "Customer Service Representative",
              "documentation": "Front-line staff member who answers customer inquiries and logs cases"}],
            [{"id": "r1", "name": "",
              "documentation": "Rep is assigned to handle inquiry intake work"}])
        self.assertEqual(validate_slice(slice_data), [])

    def test_missing_documentation_caught(self):
        findings = validate_slice(sl([{"id": "e1", "name": "CRM System"}]))
        self.assertEqual([f["check_id"] for f in findings], ["docs_missing_element"])

    def test_empty_documentation_caught(self):
        findings = validate_slice(sl([{"id": "e1", "name": "CRM System",
                                       "documentation": "   "}], []))
        self.assertEqual([f["check_id"] for f in findings], ["docs_missing_element"])

    def test_placeholder_caught(self):
        findings = validate_slice(sl([{"id": "e1", "name": "CRM System",
                                       "documentation": "TODO"}], []))
        self.assertEqual([f["check_id"] for f in findings], ["docs_placeholder"])

    def test_too_short_caught(self):
        findings = validate_slice(sl([{"id": "e1", "name": "CRM System",
                                       "documentation": "Stores customers"}], []))
        self.assertEqual([f["check_id"] for f in findings], ["docs_too_short"])

    def test_name_restatement_caught(self):
        findings = validate_slice(sl([{"id": "e1", "name": "Shipment Order",
                                       "documentation": "Shipment order"}], []))
        self.assertEqual([f["check_id"] for f in findings], ["docs_restates_name"])

    def test_partial_restatement_with_extra_word_passes(self):
        slice_data = sl([{"id": "e1", "name": "Shipment Order",
                          "documentation": "Order capturing one shipment booking"}], [])
        self.assertEqual(validate_slice(slice_data), [])

    def test_relationship_missing_docs_caught(self):
        findings = validate_slice(sl([], [{"id": "r1", "name": "",
                                           "sourceId": "a", "targetId": "b"}]))
        self.assertEqual([f["check_id"] for f in findings],
                         ["docs_missing_relationship"])

    def test_negative_control_bad_slice_fails(self):
        slice_data = sl([{"id": "e1", "name": "X", "documentation": "X"}],
                        [{"id": "r1", "name": ""}])
        self.assertTrue(validate_slice(slice_data))


if __name__ == "__main__":
    unittest.main()
