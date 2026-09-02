#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE.
# SPDX-License-Identifier: MIT
"""Structural checks for the public companion pages."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "index.html"
GUIDE = DOCS / "guide.html"
CSS = DOCS / "site.css"

LANDING_IDS = (
    "what",
    "altitudes",
    "agents",
    "ask",
    "why",
    "eval",
    "examples",
    "install",
)
AGENT_NAMES = (
    "ZCode",
    "Claude Code",
    "Cursor",
    "Gemini CLI",
    "OpenAI Codex",
    "GitHub Copilot CLI",
)
GUIDE_IDS = (
    "theory",
    "layer-motivation",
    "layer-strategy",
    "layer-business",
    "layer-application",
    "layer-technology",
    "layer-migration",
    "skip-keep",
    "pays",
    "anti",
)
INVOKE_FRAGMENTS = (
    "invoice-to-cash capability map for finance and ops",
    "Northridge and Vale insurance merger",
    "add a second CRM for the European branch",
    "cutting quote time from 4 hours to 30 minutes",
    "move the legacy TMS to a cloud landing zone",
    "the Application Support view is unreadable",
)
LAYER_SPECIALISTS = {
    "layer-motivation": "archi-motivation",
    "layer-strategy": "archi-capability-strategy",
    "layer-business": "archi-business",
    "layer-application": "archi-application",
    "layer-technology": "archi-technology-physical",
    "layer-migration": "archi-implementation-migration",
}


def _strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def _section(html: str, section_id: str) -> str:
    pattern = rf'<section[^>]*\sid="{re.escape(section_id)}"[^>]*>(.*?)</section>'
    match = re.search(pattern, html, flags=re.S)
    if not match:
        raise AssertionError(f"missing section id={section_id}")
    return match.group(1)


class CompanionSiteTests(unittest.TestCase):
    def test_files_exist(self) -> None:
        self.assertTrue(CSS.is_file(), "docs/site.css missing")
        self.assertTrue(INDEX.is_file(), "docs/index.html missing")
        self.assertTrue(GUIDE.is_file(), "docs/guide.html missing")

    def test_html_links_shared_css(self) -> None:
        for path in (INDEX, GUIDE):
            text = path.read_text(encoding="utf-8")
            self.assertIn('href="site.css"', text, f"{path.name} missing site.css link")

    def test_landing_section_ids(self) -> None:
        text = INDEX.read_text(encoding="utf-8")
        for sid in LANDING_IDS:
            self.assertIn(f'id="{sid}"', text, f"landing missing id={sid}")
        self.assertNotIn('id="chain"', text)
        agents = _section(text, "agents")
        for name in AGENT_NAMES:
            self.assertIn(name, agents, f"agents section missing {name}")
        self.assertNotIn("ZCode is the default install target", text)

    def test_guide_section_ids(self) -> None:
        text = GUIDE.read_text(encoding="utf-8")
        for sid in GUIDE_IDS:
            self.assertIn(f'id="{sid}"', text, f"guide missing id={sid}")

    def test_landing_orchestrator_and_invokes(self) -> None:
        text = INDEX.read_text(encoding="utf-8")
        self.assertIn("/archi-orchestrator", text)
        for frag in INVOKE_FRAGMENTS:
            self.assertIn(frag, text, f"landing missing invoke fragment: {frag}")
        ask = _section(text, "ask")
        self.assertGreaterEqual(ask.count("Altitudes:"), 6)
        eval_html = _section(text, "eval")
        self.assertIn("Meridian Freight", eval_html)
        self.assertIn("JGS Eval Loop", eval_html)
        self.assertIn("not a public skill-versus-no-skill A/B", eval_html)

    def test_guide_specialist_per_layer(self) -> None:
        text = GUIDE.read_text(encoding="utf-8")
        for sid, name in LAYER_SPECIALISTS.items():
            body = _section(text, sid)
            self.assertIn(name, body, f"{sid} missing {name}")

    def test_no_copied_catalog(self) -> None:
        for path in (INDEX, GUIDE):
            text = path.read_text(encoding="utf-8")
            if "archimate://reference/archimate-layers" in text:
                idx = text.index("archimate://reference/archimate-layers")
                window = text[idx : idx + 1200]
                self.assertNotIn("<table", window.lower())
            self.assertNotIn("Access relationship", text)

    def test_no_em_dash_outside_comments(self) -> None:
        for path in (INDEX, GUIDE):
            visible = _strip_comments(path.read_text(encoding="utf-8"))
            self.assertNotIn("\u2014", visible, f"em dash in {path.name}")

    def test_landing_no_private_evidence_hrefs(self) -> None:
        text = INDEX.read_text(encoding="utf-8")
        self.assertNotIn("docs/evidence/", text)
        self.assertNotIn("docs/eval/", text)
        hrefs = re.findall(r'href="([^"]+)"', text)
        for href in hrefs:
            self.assertFalse(href.startswith("evidence/"), href)
            self.assertFalse(href.startswith("eval/"), href)


if __name__ == "__main__":
    unittest.main()
