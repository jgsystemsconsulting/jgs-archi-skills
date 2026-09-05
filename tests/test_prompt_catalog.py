#!/usr/bin/env python3
# Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE.
# SPDX-License-Identifier: MIT
"""Tests for helpers/prompt_card_schema.py and docs/prompts/ catalog."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "helpers" / "prompt_card_schema.py"
PROMPTS = ROOT / "docs" / "prompts"

from helpers.prompt_card_schema import (
    REQUIRED_HEADINGS,
    invoke_line,
    iter_cards,
    missing_headings,
    sections,
    specialists_listed,
    validate_card,
)

MINIMAL = """# x

## Priority
P0

## Invoke
/archi-orchestrator invoice-to-cash capability map for finance and ops

## Problem
Quotes sit in email and collections chase paper invoices.

## Stakeholders
- CFO

## Concerns
- Cash visibility

## Scope
In: capabilities and processes. Out: factory floor.

## Current state
ERP plus spreadsheets.

## Target state
One order-to-cash picture.

## Expected views
- Capability Map

## Specialists expected
- archi-elicit
- archi-capability-strategy

## Pass checks
- confirmation gate before mutate
"""


def specialist_dirs() -> set[str]:
    skills = ROOT / "skills"
    return {
        p.name
        for p in skills.iterdir()
        if p.is_dir()
        and (p / "SKILL.md").is_file()
        and p.name.startswith("archi-")
        and p.name != "archi-orchestrator"
    }


class SchemaUnitTests(unittest.TestCase):
    def test_required_heading_count(self) -> None:
        self.assertEqual(len(REQUIRED_HEADINGS), 11)

    def test_minimal_passes(self) -> None:
        self.assertEqual(validate_card(MINIMAL), [])

    def test_missing_confirmation_heading_fails(self) -> None:
        body = MINIMAL.replace("## Pass checks\n- confirmation gate before mutate\n", "")
        missing = missing_headings(body)
        self.assertIn("Pass checks", missing)

    def test_bad_invoke_prefix_fails(self) -> None:
        body = MINIMAL.replace(
            "/archi-orchestrator invoice-to-cash capability map for finance and ops",
            "draw a container diagram for checkout",
        )
        findings = validate_card(body)
        self.assertTrue(any("invoke" in f.lower() for f in findings))

    def test_element_type_in_problem_fails(self) -> None:
        body = MINIMAL.replace(
            "Quotes sit in email and collections chase paper invoices.",
            "Create a Business Actor named Customer.",
        )
        findings = validate_card(body)
        self.assertTrue(any("Business Actor" in f for f in findings))

    def test_unknown_specialist_fails(self) -> None:
        body = MINIMAL.replace("- archi-elicit\n", "- archi-elicit\n- archi-wizard\n")
        findings = validate_card(body)
        self.assertTrue(any("archi-wizard" in f for f in findings))

    def test_invoke_line_strips(self) -> None:
        self.assertTrue(invoke_line(MINIMAL).startswith("/archi-orchestrator "))

    def test_specialists_listed(self) -> None:
        self.assertEqual(
            specialists_listed(MINIMAL),
            ["archi-elicit", "archi-capability-strategy"],
        )

    def test_sections_keys(self) -> None:
        self.assertEqual(list(sections(MINIMAL).keys()), REQUIRED_HEADINGS)

    def test_headings_out_of_order_fails(self) -> None:
        swapped = MINIMAL.replace("## Problem\n", "## Problem_HOLD\n")
        swapped = swapped.replace("## Stakeholders\n", "## Problem\n")
        swapped = swapped.replace("## Problem_HOLD\n", "## Stakeholders\n")
        findings = validate_card(swapped)
        self.assertTrue(any("order" in f.lower() for f in findings))

    def test_extra_heading_fails(self) -> None:
        body = MINIMAL.replace("## Pass checks\n", "## Extra\nx\n## Pass checks\n")
        findings = validate_card(body)
        self.assertTrue(any("extra heading" in f.lower() for f in findings))

    def test_spaced_business_process_fails(self) -> None:
        body = MINIMAL.replace(
            "Quotes sit in email and collections chase paper invoices.",
            "Model the Business Process for quoting.",
        )
        findings = validate_card(body)
        self.assertTrue(any("Business Process" in f for f in findings))


class CatalogTests(unittest.TestCase):
    def test_fourteen_cards(self) -> None:
        cards = iter_cards(PROMPTS)
        self.assertEqual(len(cards), 14, [p.name for p in cards])

    def test_each_card_valid(self) -> None:
        cards = iter_cards(PROMPTS)
        self.assertTrue(cards)
        for path in cards:
            text = path.read_text(encoding="utf-8")
            findings = validate_card(text)
            self.assertEqual(findings, [], msg=f"{path.name}: {findings}")

    def test_priority_counts(self) -> None:
        counts = {"P0": 0, "P1": 0, "P2": 0}
        for path in iter_cards(PROMPTS):
            pri = sections(path.read_text(encoding="utf-8"))["Priority"].strip()
            counts[pri] += 1
        self.assertEqual(counts, {"P0": 4, "P1": 6, "P2": 4})

    def test_filenames_p01_to_p14(self) -> None:
        names = [p.name for p in iter_cards(PROMPTS)]
        prefixes = [n[:3] for n in names]
        self.assertEqual(prefixes, [f"p{i:02d}" for i in range(1, 15)])

    def test_all_specialists_covered(self) -> None:
        listed: set[str] = set()
        for path in iter_cards(PROMPTS):
            listed.update(specialists_listed(path.read_text(encoding="utf-8")))
        missing = specialist_dirs() - listed
        self.assertEqual(missing, set())

    def test_p06_motivation_only(self) -> None:
        path = next(p for p in iter_cards(PROMPTS) if p.name.startswith("p06-"))
        specs = set(specialists_listed(path.read_text(encoding="utf-8")))
        self.assertIn("archi-motivation", specs)
        for banned in (
            "archi-application",
            "archi-technology-physical",
            "archi-implementation-migration",
        ):
            self.assertNotIn(banned, specs)

    def test_p08_migration(self) -> None:
        path = next(p for p in iter_cards(PROMPTS) if p.name.startswith("p08-"))
        specs = set(specialists_listed(path.read_text(encoding="utf-8")))
        self.assertIn("archi-implementation-migration", specs)
        self.assertIn("archi-technology-physical", specs)

    def test_p10_layout_qa_only(self) -> None:
        path = next(p for p in iter_cards(PROMPTS) if p.name.startswith("p10-"))
        specs = set(specialists_listed(path.read_text(encoding="utf-8")))
        self.assertIn("archi-layout", specs)
        self.assertIn("archi-model-qa", specs)
        for banned in (
            "archi-motivation",
            "archi-capability-strategy",
            "archi-business",
            "archi-application",
            "archi-technology-physical",
            "archi-implementation-migration",
        ):
            self.assertNotIn(banned, specs)

    def test_p02_has_migration(self) -> None:
        path = next(p for p in iter_cards(PROMPTS) if p.name.startswith("p02-"))
        specs = set(specialists_listed(path.read_text(encoding="utf-8")))
        self.assertIn("archi-implementation-migration", specs)

    def test_p03_has_technology_physical(self) -> None:
        path = next(p for p in iter_cards(PROMPTS) if p.name.startswith("p03-"))
        specs = set(specialists_listed(path.read_text(encoding="utf-8")))
        self.assertIn("archi-technology-physical", specs)

    def test_every_card_mentions_confirmation(self) -> None:
        for path in iter_cards(PROMPTS):
            body = sections(path.read_text(encoding="utf-8"))["Pass checks"]
            self.assertIn("confirmation", body.lower(), msg=path.name)

    def test_catalog_readme_lists_every_invoke(self) -> None:
        readme = (PROMPTS / "README.md").read_text(encoding="utf-8")
        for path in iter_cards(PROMPTS):
            line = invoke_line(path.read_text(encoding="utf-8"))
            self.assertIn(line, readme, msg=path.name)

    def test_cli_on_catalog_dir(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(HELPER), str(PROMPTS)],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


@unittest.skipUnless(
    "docs/prompts" in (ROOT / "README.md").read_text(encoding="utf-8"),
    "product pointers land in Task 3",
)
class ProductDocsTests(unittest.TestCase):
    def test_product_docs_point_at_prompts(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "docs" / "skill-usage.md").read_text(encoding="utf-8")
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn("docs/prompts", readme)
        self.assertIn("docs/prompts", usage)
        self.assertIn("docs/prompts", html)


if __name__ == "__main__":
    unittest.main()
