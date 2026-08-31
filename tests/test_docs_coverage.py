# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
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


    def test_default_still_passes_without_evidence_line(self):
        slice_data = sl(
            [{"id": "e1", "name": "Customer Service Representative",
              "type": "BusinessActor",
              "documentation": "Front-line staff member who answers customer inquiries and logs cases"}],
            [])
        self.assertEqual(validate_slice(slice_data), [])

    def test_require_evidence_missing_line(self):
        slice_data = sl(
            [{"id": "e1", "name": "CRM",
              "type": "ApplicationComponent",
              "documentation": "System of record for customer accounts and cases"}],
            [])
        findings = validate_slice(slice_data, require_evidence=True)
        self.assertIn("docs_missing_evidence", [f["check_id"] for f in findings])

    def test_require_evidence_valid_line_passes(self):
        slice_data = sl(
            [{"id": "e1", "name": "CRM",
              "type": "ApplicationComponent",
              "documentation": "Evidence: stated - View Plan\nSystem of record for customer accounts and cases"}],
            [])
        self.assertEqual(validate_slice(slice_data, require_evidence=True), [])

    def test_restates_type_caught(self):
        slice_data = sl(
            [{"id": "e1", "name": "CRM",
              "type": "ApplicationComponent",
              "documentation": "application component application"}],
            [])
        findings = validate_slice(slice_data)
        self.assertIn("docs_restates_type", [f["check_id"] for f in findings])

    def test_require_evidence_not_applied_to_relationships(self):
        slice_data = sl(
            [],
            [{"id": "r1", "name": "",
              "documentation": "Rep is assigned to handle inquiry intake work"}])
        self.assertEqual(validate_slice(slice_data, require_evidence=True), [])

    def test_evidence_line_alone_is_too_short(self):
        slice_data = sl(
            [{"id": "e1", "name": "CRM",
              "type": "ApplicationComponent",
              "documentation": "Evidence: stated - View Plan"}],
            [])
        findings = validate_slice(slice_data, require_evidence=True)
        self.assertIn("docs_too_short", [f["check_id"] for f in findings])

    def test_require_evidence_cli(self):
        import json, subprocess, sys, tempfile
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "s.json"
            p.write_text(json.dumps({
                "elements": [{"id": "e1", "name": "CRM",
                              "type": "ApplicationComponent",
                              "documentation": "System of record for customer accounts and cases"}],
                "relationships": [],
            }), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(root / "helpers" / "docs_coverage.py"),
                 "--json", "--require-evidence", str(p)],
                capture_output=True, text=True, cwd=str(root),
            )
            self.assertNotEqual(proc.returncode, 0)
            data = json.loads(proc.stdout)
            self.assertFalse(data["ok"])
            self.assertIn("docs_missing_evidence",
                          [f["check_id"] for f in data["findings"]])

if __name__ == "__main__":
    unittest.main()
