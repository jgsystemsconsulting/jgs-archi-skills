# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Tests for helpers/layout_check.py (eval-loop layout gate)."""
import unittest

from helpers.layout_check import validate_views


def view(**over):
    v = {
        "view": "Test View", "viewId": "v1",
        "objects": [
            {"id": "a", "viewObjectId": "va", "name": "Alpha", "type": "BusinessActor",
             "x": 40, "y": 40, "width": 120, "height": 55},
            {"id": "b", "viewObjectId": "vb", "name": "Beta", "type": "BusinessProcess",
             "x": 260, "y": 40, "width": 120, "height": 55},
        ],
        "connections": [
            {"id": "c1", "source": "a", "target": "b"},
        ],
    }
    v.update(over)
    return v


class TestLayoutCheck(unittest.TestCase):
    def test_clean_view_passes(self):
        findings, stats = validate_views({"views": [view()]})
        self.assertEqual(findings, [])
        self.assertEqual(stats[0]["edge_crossings"], 0)

    def test_overlap_caught(self):
        objs = view()["objects"]
        objs[1]["x"] = 100  # overlaps Alpha's 40..160 range
        findings, _ = validate_views({"views": [view(objects=objs)]})
        self.assertIn("layout_overlap", [f["check_id"] for f in findings])

    def test_proper_group_containment_passes(self):
        objs = [
            {"id": "g", "viewObjectId": "vg", "name": "Group", "type": "Grouping",
             "x": 20, "y": 20, "width": 400, "height": 120},
            {"id": "a", "viewObjectId": "va", "name": "Alpha", "type": "BusinessActor",
             "x": 40, "y": 40, "width": 120, "height": 55},
        ]
        findings, _ = validate_views({"views": [view(objects=objs, connections=[])]})
        self.assertEqual(findings, [])

    def test_backward_flow_caught(self):
        objs = view()["objects"]
        objs[0]["x"] = 500  # Alpha right of Beta: connection flows right-to-left
        findings, _ = validate_views({"views": [view(objects=objs)]})
        self.assertIn("layout_backward_flow", [f["check_id"] for f in findings])

    def test_layer_interleave_caught(self):
        objs = [
            {"id": "a", "name": "Actor", "type": "BusinessActor",
             "x": 40, "y": 40, "width": 120, "height": 55},
            {"id": "b", "name": "Actor 2", "type": "BusinessEvent",
             "x": 200, "y": 40, "width": 120, "height": 55},
            {"id": "c", "name": "App", "type": "ApplicationComponent",
             "x": 90, "y": 60, "width": 120, "height": 55},
            {"id": "d", "name": "App 2", "type": "ApplicationService",
             "x": 230, "y": 70, "width": 120, "height": 55},
        ]
        findings, _ = validate_views({"views": [view(objects=objs, connections=[])]})
        self.assertIn("layout_layer_interleave", [f["check_id"] for f in findings])

    def test_missing_geometry_caught(self):
        objs = [{"id": "a", "viewObjectId": "va", "name": "Alpha",
                 "type": "BusinessActor"}]
        findings, _ = validate_views({"views": [view(objects=objs, connections=[])]})
        self.assertIn("layout_missing_geometry", [f["check_id"] for f in findings])

    def test_mcp_hard_counts_caught(self):
        assessment = {"overlapCount": 2, "containmentOverlaps": 0,
                      "labelOverlapCount": 0, "orphanedConnections": 1,
                      "overallRating": "poor"}
        findings, _ = validate_views({"views": [view(assessment=assessment)]})
        ids = [f["check_id"] for f in findings]
        for expected in ("mcp_overlap", "mcp_orphaned_connections", "mcp_rating"):
            self.assertIn(expected, ids)

    def test_negative_control_dirty_view_fails(self):
        objs = view()["objects"]
        objs[1]["x"] = 120
        findings, _ = validate_views({"views": [view(objects=objs)]})
        self.assertTrue(findings)


if __name__ == "__main__":
    unittest.main()
