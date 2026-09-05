#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
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
ENGAGE = DOCS / "engage.html"
CSS = DOCS / "site.css"
README = ROOT / "README.md"

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
ENGAGE_IDS = (
    "ways",
    "standup",
    "delivery",
    "enablement",
    "enquire",
    "not-sold",
)
WAY_NAMES = (
    "Stand up the practice",
    "Delivery work packages",
    "Enablement",
)
PACKAGE_NAMES = (
    "Motivation pack",
    "Single capability cut",
    "Business operations view",
    "Application landscape (bounded)",
    "Technology / landing zone",
    "Migration roadmap",
    "Layout and QA only",
    "Trace stitch",
)
ENABLEMENT_NAMES = (
    "View Plan clinic",
    "Method studio",
    "Named review",
)
NOT_SOLD = (
    "A paid licence of the MIT zip.",
    "Hosted Archi or a model that leaves their machine.",
    "Whole-estate partnership with no viewpoint list.",
    "Plugin patches or pull requests against jgs-archi-mcp",
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
META_DESCRIPTION = (
    "JG Systems Consulting Ltd work around the MIT pack: stand up, "
    "named viewpoints in Archi, or train the people who run the orchestrator."
)
BANNED_VISIBLE = ("\u2014", "£", "$", "GBP", "price", "day rate")


def _strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def _section(html: str, section_id: str) -> str:
    pattern = rf'<section[^>]*\sid="{re.escape(section_id)}"[^>]*>(.*?)</section>'
    match = re.search(pattern, html, flags=re.S)
    if not match:
        raise AssertionError(f"missing section id={section_id}")
    return match.group(1)


def _hero(html: str) -> str:
    match = re.search(r'<div class="hero">(.*?)</div>\s*</div>', html, flags=re.S)
    if not match:
        raise AssertionError("missing hero")
    return match.group(1)


class CompanionSiteTests(unittest.TestCase):
    def test_files_exist(self) -> None:
        self.assertTrue(CSS.is_file(), "docs/site.css missing")
        self.assertTrue(INDEX.is_file(), "docs/index.html missing")
        self.assertTrue(GUIDE.is_file(), "docs/guide.html missing")
        self.assertTrue(ENGAGE.is_file(), "docs/engage.html missing")

    def test_html_links_shared_css(self) -> None:
        for path in (INDEX, GUIDE, ENGAGE):
            text = path.read_text(encoding="utf-8")
            self.assertIn('href="site.css"', text, f"{path.name} missing site.css link")

    def test_landing_section_ids(self) -> None:
        text = INDEX.read_text(encoding="utf-8")
        for sid in LANDING_IDS:
            self.assertIn(f'id="{sid}"', text, f"landing missing id={sid}")
        self.assertNotIn('id="chain"', text)
        self.assertNotIn('id="engage"', text)
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
        for path in (INDEX, GUIDE, ENGAGE):
            text = path.read_text(encoding="utf-8")
            if "archimate://reference/archimate-layers" in text:
                idx = text.index("archimate://reference/archimate-layers")
                window = text[idx : idx + 1200]
                self.assertNotIn("<table", window.lower())
            self.assertNotIn("Access relationship", text)

    def test_no_em_dash_outside_comments(self) -> None:
        for path in (INDEX, GUIDE, ENGAGE):
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

    def test_landing_hero_unchanged(self) -> None:
        hero = _hero(INDEX.read_text(encoding="utf-8"))
        self.assertIn('href="guide.html"', hero)
        self.assertIn('href="#install"', hero)
        self.assertNotIn("engage.html", hero)
        self.assertEqual(hero.count("btn btn-primary"), 1)
        self.assertEqual(hero.count("btn btn-ghost"), 1)

    def test_nav_and_readme_point_at_engage(self) -> None:
        index = INDEX.read_text(encoding="utf-8")
        guide = GUIDE.read_text(encoding="utf-8")
        self.assertIn('href="engage.html"', index)
        self.assertIn('href="engage.html"', guide)
        self.assertIn("engage.html", README.read_text(encoding="utf-8"))

    def test_engage_chrome(self) -> None:
        text = ENGAGE.read_text(encoding="utf-8")
        self.assertIn("<title>Engagement: jgs-archi-skills</title>", text)
        self.assertIn(f'content="{META_DESCRIPTION}"', text)
        self.assertIn(
            'href="https://jgsystemsconsulting.github.io/jgs-archi-skills/engage.html"',
            text,
        )
        self.assertNotIn("application/ld+json", text)
        self.assertIn("MIT", text)
        self.assertIn("JG Systems Consulting Ltd", text)
        visible = _strip_comments(text)
        for token in BANNED_VISIBLE:
            self.assertNotIn(token, visible, f"banned token {token!r}")

    def test_engage_ways_and_catalog(self) -> None:
        text = ENGAGE.read_text(encoding="utf-8")
        for sid in ENGAGE_IDS:
            self.assertIn(f'id="{sid}"', text, f"engage missing id={sid}")
        for name in WAY_NAMES:
            self.assertIn(name, text, f"missing way name {name}")
        delivery = _section(text, "delivery")
        positions = [delivery.find(name) for name in PACKAGE_NAMES]
        self.assertTrue(all(p >= 0 for p in positions), positions)
        self.assertEqual(positions, sorted(positions))
        ways = _section(text, "ways")
        for href in ("#standup", "#delivery", "#enablement"):
            self.assertIn(f'href="{href}"', ways)
        self.assertEqual(ways.count(">Details<"), 3)

    def test_engage_enquire_and_hero(self) -> None:
        text = ENGAGE.read_text(encoding="utf-8")
        hero = _hero(text)
        self.assertRegex(
            hero,
            r'class="btn btn-primary"[^>]*href="#enquire"',
        )
        self.assertRegex(
            hero,
            r'class="btn btn-ghost"[^>]*href="index.html#install"',
        )
        enquire = _section(text, "enquire")
        self.assertIn("Request a conversation", enquire)
        self.assertRegex(
            enquire,
            r'class="btn btn-primary"[^>]*href="[^"]*labs\.jgsystemsconsulting\.com/licensing\.html',
        )

    def test_engage_enablement_and_not_sold(self) -> None:
        text = ENGAGE.read_text(encoding="utf-8")
        enablement = _section(text, "enablement")
        for name in ENABLEMENT_NAMES:
            self.assertIn(name, enablement)
        self.assertNotIn("What happens", enablement)
        self.assertNotIn("Done when", enablement)
        not_sold = _section(text, "not-sold")
        for line in NOT_SOLD:
            self.assertIn(line, not_sold)


if __name__ == "__main__":
    unittest.main()
