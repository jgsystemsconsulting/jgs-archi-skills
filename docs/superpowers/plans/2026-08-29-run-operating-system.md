# Run Operating System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make specialist runs fail visibly when they skip dispositions, invent elements, place notes before layout, or present a first-generation model as finished.

**Architecture:** One shared contract in `docs/CREATE_PATH.md` (seven hedge-free gates, working mode, provenance, layout footguns). One new stdlib helper validates disposition ledgers. The existing completion-summary schema grows two draft blocks. Structural tests force layer, layout, documentation, and orchestrator skills to carry the new slots. No live MCP, no new dependencies, no reverse-engineering product.

**Tech Stack:** Python 3.10+ standard library, unittest, existing skill markdown plus `docs/CREATE_PATH.md`.

**Spec:** `docs/specs/run-operating-system.md`

## Global Constraints

- Python 3.10+, standard library only. No pip packages.
- Skills consume JGS Archi Bridge MCP only. Tool names must exist in `docs/mcp/archi-bridge-inventory.json`.
- No ArchiMate metamodel dumps in skills (VISION NG-4).
- User governs architectural decisions (VISION NG-3).
- Do not modify `skills/archi-viewpoint-select/SKILL.md` (frozen digest `95c18a9ac4407d09352b47fc1a3887148353e7a6c09f020dbba5bf1a320b623f` in `tests/test_specialist_contract.py`).
- Do not change eval-loop `GATES.md` or require `Evidence:` on eval slices.
- Do not add specializations, label glyphs, or `repoToArchi.coverage.*` properties.
- Durable prose: technical voice, no em dashes.
- Evidence documentation line uses a spaced hyphen: `Evidence: stated | inferred | existing - <source>`.
- Full suite stays green: `python -m unittest discover -s tests -q`.
- MCP ref scan stays clean: `python helpers/validate_skill_mcp_refs.py`.

## File map

| File | Responsibility |
|------|----------------|
| `helpers/disposition.py` | Parse and validate candidate disposition ledgers (markdown table or JSON). |
| `tests/test_disposition.py` | Unit tests for that helper. |
| `helpers/completion_summary_schema.py` | Add Deliberately Deferred and Improve Next required blocks. |
| `tests/test_completion_summary_schema.py` | Seven-block fixtures; five-block fixtures fail. |
| `tests/test_specialist_contract.py` | Structural asserts for CP-G1..G7, disposition tables, layout footguns, draft close-out. |
| `docs/CREATE_PATH.md` | Gate manifest, working mode, provenance, layout footguns, disposition in hand-back, draft close-out. |
| `skills/archi-motivation/SKILL.md` through `archi-traceability/SKILL.md` (seven creating specialists) | Candidate disposition table in output template. |
| `skills/archi-model-qa/SKILL.md` | Undispositioned candidate is a finding. |
| `skills/archi-layout/SKILL.md` | Footguns, annotate-last, `export-view`, omit note height. |
| `skills/archi-documentation/SKILL.md` | Seven-block completion summary. |
| `skills/archi-orchestrator/SKILL.md` | Draft checkpoint after documentation; decide-and-log. |
| `skills/archi-elicit/SKILL.md` | Inferences survive into specialist evidence lines. |
| `CHANGELOG.md` | Unreleased note. |

Out of this plan: viewpoint-select, eval-loop gates, `helpers/docs_coverage.py`, install script.

---

### Task 1: Disposition helper

**Files:**
- Create: `tests/test_disposition.py`
- Create: `helpers/disposition.py`

**Interfaces:**
- Consumes: nothing from later tasks
- Produces:
  - `DISPOSITIONS: tuple[str, ...] = ("captured", "folded", "needs-user", "out-of-scope")`
  - `parse_markdown_table(text: str) -> list[dict[str, str]]` with keys `candidate`, `disposition`, `target`, `reason`
  - `validate_ledger(rows: list[dict], *, allow_empty: bool = False) -> list[dict]` findings with `check_id`, `problem`, optional `candidate`
  - CLI: `python helpers/disposition.py PATH` with optional json and allow-empty flags; exit 0 if no findings, else 1

- [ ] **Step 1: Write the failing tests**

Create `tests/test_disposition.py`:

```python
#!/usr/bin/env python3
"""Unit tests for helpers/disposition.py. Stdlib only."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "helpers" / "disposition.py"
sys.path.insert(0, str(ROOT / "helpers"))
from disposition import parse_markdown_table, validate_ledger  # noqa: E402

TABLE = """# Ledger

| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| CRM | captured | CRM System @ Application Structure | |
| DTO pack | folded | CRM System | 12 request DTOs |
| Payments | needs-user | | one service or two? |
| Batch jobs | out-of-scope | | confirmed out of this pass |
"""

JSON_ROWS = [
    {
        "candidate": "CRM",
        "disposition": "captured",
        "target": "CRM System @ Application Structure",
        "reason": "",
    }
]


class T(unittest.TestCase):
    def _run(self, body: str, extra=()):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(body)
            path = fh.name
        try:
            return subprocess.run(
                [sys.executable, str(H), path, *extra],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_ok_markdown(self):
        rows = parse_markdown_table(TABLE)
        self.assertEqual(len(rows), 4)
        self.assertEqual(validate_ledger(rows), [])
        self.assertEqual(self._run(TABLE).returncode, 0)

    def test_ok_json(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        ) as fh:
            json.dump(JSON_ROWS, fh)
            path = fh.name
        try:
            proc = subprocess.run(
                [sys.executable, str(H), path],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_empty_ledger_fails(self):
        findings = validate_ledger([])
        self.assertTrue(any(f["check_id"] == "empty_ledger" for f in findings))
        self.assertEqual(self._run("| Candidate | Disposition | Target | Reason |\n|---|---|---|---|\n").returncode, 1)

    def test_allow_empty(self):
        self.assertEqual(validate_ledger([], allow_empty=True), [])
        self.assertEqual(
            self._run(
                "| Candidate | Disposition | Target | Reason |\n|---|---|---|---|\n",
                extra=("--allow-empty",),
            ).returncode,
            0,
        )

    def test_unknown_disposition(self):
        rows = [{
            "candidate": "X",
            "disposition": "skipped",
            "target": "",
            "reason": "n/a",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "unknown_disposition" for f in findings))

    def test_captured_requires_target(self):
        rows = [{
            "candidate": "X",
            "disposition": "captured",
            "target": "",
            "reason": "",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "missing_target" for f in findings))

    def test_folded_requires_target_and_reason(self):
        rows = [{
            "candidate": "X",
            "disposition": "folded",
            "target": "",
            "reason": "",
        }]
        ids = {f["check_id"] for f in validate_ledger(rows)}
        self.assertIn("missing_target", ids)
        self.assertIn("missing_reason", ids)

    def test_needs_user_requires_reason(self):
        rows = [{
            "candidate": "X",
            "disposition": "needs-user",
            "target": "",
            "reason": "",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "missing_reason" for f in findings))

    def test_out_of_scope_requires_reason(self):
        rows = [{
            "candidate": "X",
            "disposition": "out-of-scope",
            "target": "",
            "reason": "",
        }]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "missing_reason" for f in findings))

    def test_duplicate_candidate(self):
        rows = [
            {"candidate": "CRM", "disposition": "captured",
             "target": "A @ V", "reason": ""},
            {"candidate": "CRM", "disposition": "folded",
             "target": "B", "reason": "dup"},
        ]
        findings = validate_ledger(rows)
        self.assertTrue(any(f["check_id"] == "duplicate_candidate" for f in findings))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_disposition -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'disposition'` (or import error on `helpers/disposition.py` missing).

- [ ] **Step 3: Write minimal implementation**

Create `helpers/disposition.py`:

```python
#!/usr/bin/env python3
"""Validate candidate disposition ledgers. Stdlib only.

Does not call MCP. Does not mutate the model.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DISPOSITIONS = ("captured", "folded", "needs-user", "out-of-scope")
NEEDS_TARGET = {"captured", "folded"}
NEEDS_REASON = {"folded", "needs-user", "out-of-scope"}


def _finding(check_id: str, problem: str, candidate: str = "") -> dict[str, Any]:
    out = {"check_id": check_id, "problem": problem}
    if candidate:
        out["candidate"] = candidate
    return out


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        if header is None:
            header = [c.casefold() for c in cells]
            continue
        if all(set(c) <= set("-: ") and c for c in cells):
            continue
        by = {header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))}
        rows.append({
            "candidate": by.get("candidate", ""),
            "disposition": by.get("disposition", ""),
            "target": by.get("target", ""),
            "reason": by.get("reason", ""),
        })
    return rows


def validate_ledger(
    rows: list[dict], *, allow_empty: bool = False
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not rows:
        if not allow_empty:
            findings.append(_finding("empty_ledger", "disposition ledger is empty"))
        return findings
    seen: dict[str, int] = {}
    for row in rows:
        name = (row.get("candidate") or "").strip()
        disp = (row.get("disposition") or "").strip().casefold()
        target = (row.get("target") or "").strip()
        reason = (row.get("reason") or "").strip()
        if not name:
            findings.append(_finding("missing_candidate", "row has no candidate name"))
            continue
        key = name.casefold()
        if key in seen:
            findings.append(_finding(
                "duplicate_candidate",
                f"candidate appears more than once: {name}",
                name,
            ))
        seen[key] = seen.get(key, 0) + 1
        if disp not in DISPOSITIONS:
            findings.append(_finding(
                "unknown_disposition",
                f"disposition {disp!r} is not one of {DISPOSITIONS}",
                name,
            ))
            continue
        if disp in NEEDS_TARGET and not target:
            findings.append(_finding(
                "missing_target",
                f"{disp} requires target",
                name,
            ))
        if disp in NEEDS_REASON and not reason:
            findings.append(_finding(
                "missing_reason",
                f"{disp} requires reason",
                name,
            ))
    return findings


def _load(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        if not isinstance(data, list):
            raise SystemExit(f"json ledger must be a list: {path}")
        return data
    return parse_markdown_table(raw)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args(argv)
    rows = _load(args.path)
    findings = validate_ledger(rows, allow_empty=args.allow_empty)
    if args.json:
        print(json.dumps({"findings": findings, "ok": not findings}, indent=2))
    elif findings:
        print("disposition findings:")
        for f in findings:
            who = f" {f['candidate']}" if f.get("candidate") else ""
            print(f"  [{f['check_id']}]{who}: {f['problem']}")
    else:
        print(f"ok: {len(rows)} disposition row(s)")
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest tests.test_disposition -v`

Expected: PASS (all tests).

- [ ] **Step 5: Commit**

```bash
git add helpers/disposition.py tests/test_disposition.py
git commit -m "feat: add offline candidate disposition ledger helper"
```

---

### Task 2: Seven-block completion summary

**Files:**
- Modify: `tests/test_completion_summary_schema.py`
- Modify: `helpers/completion_summary_schema.py`

**Interfaces:**
- Consumes: existing `validate_completion_summary(text: str) -> list[dict]`
- Produces: `REQUIRED_BLOCKS` now includes `Deliberately Deferred` and `Improve Next` after `Specialists Run`. Aliases: `"deferred"` and `"deliberately deferred"` map to `Deliberately Deferred`; `"improve next"` and `"next"` map to `Improve Next`.

- [ ] **Step 1: Update tests so the old five-block fixtures fail until the helper grows**

Replace `VALID` and `LABEL_VALID` in `tests/test_completion_summary_schema.py` with seven-block versions, and add a test that the old five-block body is invalid:

Keep the file header, imports, `ROOT`, `H`, and `_run` helper. Replace the fixtures and class body:

```python
VALID = """# Completion Summary

## Views Touched
- Business Process Cooperation

## Decisions
- Model as-is only

## Open Questions
- Include payment release?

## Confirmation Status
confirmed

## Specialists Run
documentation, layout

## Deliberately Deferred
- Payment release (out of confirmed scope)

## Improve Next
- Add application cooperation view if payments land
"""

LABEL_VALID = """# Summary
- Views Touched: v1, v2
- Decisions: keep shared Customer
- Open Questions: none
- Confirmation Status: confirmed
- Specialists Run: documentation
- Deliberately Deferred: none
- Improve Next: none
"""

OLD_FIVE = """# Completion Summary

## Views Touched
- Business Process Cooperation

## Decisions
- Model as-is only

## Open Questions
- Include payment release?

## Confirmation Status
confirmed

## Specialists Run
documentation, layout
"""


class T(unittest.TestCase):
    def _run(self, body):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(body)
            path = fh.name
        try:
            return subprocess.run(
                [sys.executable, str(H), path],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
        finally:
            Path(path).unlink(missing_ok=True)

    def test_ok_h2(self):
        self.assertEqual(validate_completion_summary(VALID), [])
        self.assertEqual(self._run(VALID).returncode, 0)

    def test_ok_labels(self):
        self.assertEqual(validate_completion_summary(LABEL_VALID), [])

    def test_old_five_block_summary_fails(self):
        findings = validate_completion_summary(OLD_FIVE)
        missing = {f["block"] for f in findings if f["check_id"] == "missing_block"}
        self.assertIn("Deliberately Deferred", missing)
        self.assertIn("Improve Next", missing)
        self.assertEqual(self._run(OLD_FIVE).returncode, 1)

    def test_missing(self):
        findings = validate_completion_summary("## Views Touched\nv1\n")
        self.assertTrue(any(f["check_id"] == "missing_block" for f in findings))
        self.assertEqual(self._run("nope").returncode, 1)

    def test_empty_block(self):
        body = """## Views Touched
x
## Decisions
x
## Open Questions
x
## Confirmation Status
confirmed
## Specialists Run
x
## Deliberately Deferred

## Improve Next
x
"""
        findings = validate_completion_summary(body)
        self.assertTrue(any(f["check_id"] == "empty_block" for f in findings))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_completion_summary_schema -v`

Expected: FAIL. `test_ok_h2` / `test_ok_labels` report missing `Deliberately Deferred` and `Improve Next`. `test_old_five_block_summary_fails` may fail because those blocks are not yet required (missing set empty).

- [ ] **Step 3: Extend the helper**

In `helpers/completion_summary_schema.py`, change `REQUIRED_BLOCKS` to:

```python
REQUIRED_BLOCKS = [
    "Views Touched",
    "Decisions",
    "Open Questions",
    "Confirmation Status",
    "Specialists Run",
    "Deliberately Deferred",
    "Improve Next",
]
```

Add to `ALIASES`:

```python
    "deferred": "Deliberately Deferred",
    "deliberately deferred": "Deliberately Deferred",
    "improve next": "Improve Next",
    "next": "Improve Next",
```

Leave `_canon`, `_blocks`, `validate_completion_summary`, and `main` unchanged.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest tests.test_completion_summary_schema -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add helpers/completion_summary_schema.py tests/test_completion_summary_schema.py
git commit -m "feat: require deferred and next blocks on completion summaries"
```

---

### Task 3: Failing specialist-contract assertions

**Files:**
- Modify: `tests/test_specialist_contract.py`

**Interfaces:**
- Consumes: `MUTATING` list already in the file
- Produces: new test methods listed below. `CREATING` is the seven content specialists. Do not change `FROZEN` or `test_viewpoint_select_frozen`.

- [ ] **Step 1: Add failing contract tests**

Keep existing tests. After `MUTATING`, add:

```python
CREATING = [
    "archi-motivation",
    "archi-capability-strategy",
    "archi-business",
    "archi-application",
    "archi-technology-physical",
    "archi-implementation-migration",
    "archi-traceability",
]
```

Add these methods to `SpecialistContractTests`:

```python
    def test_create_path_gate_manifest(self) -> None:
        text = CREATE.read_text(encoding="utf-8")
        for gate in ("CP-G1", "CP-G2", "CP-G3", "CP-G4", "CP-G5", "CP-G6", "CP-G7"):
            self.assertIn(gate, text, msg=f"CREATE_PATH missing {gate}")
        self.assertIn("captured", text)
        self.assertIn("folded", text)
        self.assertIn("needs-user", text)
        self.assertIn("out-of-scope", text)
        self.assertIn("Evidence: stated | inferred | existing", text)
        self.assertIn("below-content", text)
        self.assertIn("export-view", text)
        self.assertIn("Deliberately Deferred", text)
        self.assertIn("Improve Next", text)

    def test_creating_specialists_have_disposition_table(self) -> None:
        for name in CREATING:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(
                "Candidate disposition",
                text,
                msg=f"{name} missing Candidate disposition",
            )
            self.assertIn("captured", text, msg=name)
            self.assertIn("folded", text, msg=name)
            self.assertIn("needs-user", text, msg=name)
            self.assertIn("out-of-scope", text, msg=name)

    def test_layout_footguns(self) -> None:
        text = (ROOT / "skills" / "archi-layout" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("export-view", text)
        self.assertIn("omit", text.casefold())
        self.assertIn("height", text.casefold())
        self.assertIn("below-content", text)
        self.assertIn("ratingBreakdown", text)
        self.assertIn("14", text)

    def test_documentation_draft_blocks(self) -> None:
        text = (
            ROOT / "skills" / "archi-documentation" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Deliberately Deferred", text)
        self.assertIn("Improve Next", text)

    def test_orchestrator_draft_checkpoint(self) -> None:
        text = (
            ROOT / "skills" / "archi-orchestrator" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Deliberately Deferred", text)
        self.assertIn("Improve Next", text)
        self.assertIn("draft", text.casefold())

    def test_model_qa_undispositioned(self) -> None:
        text = (ROOT / "skills" / "archi-model-qa" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("undispositioned", text.casefold())

    def test_elicit_inferences_survive(self) -> None:
        text = ELICIT.read_text(encoding="utf-8")
        self.assertIn("Evidence:", text)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_specialist_contract -v`

Expected: existing tests PASS; new tests FAIL (CREATE_PATH missing `CP-G1`, skills missing `Candidate disposition`, layout missing `export-view` / `below-content`, and so on). Do not "fix" by weakening asserts.

- [ ] **Step 3: No production edits in this task**

Leave skills and CREATE_PATH unchanged. The next four tasks make these tests pass.

- [ ] **Step 4: Commit the failing (or rather, newly asserting) tests together with a note that they are expected red until Tasks 4-7 land. If the team's git hook rejects a red suite, skip this commit and land Task 3+4 in one commit after Task 4. Prefer one commit here if hooks allow:**

This repo has no failing-test hook in the plan's knowledge. Commit the test file:

```bash
git add tests/test_specialist_contract.py
git commit -m "test: assert run-operating-system contract slots"
```

If you skip the red commit, carry the test edits into Task 4's commit.

---

### Task 4: CREATE_PATH operating system

**Files:**
- Modify: `docs/CREATE_PATH.md`

**Interfaces:**
- Consumes: gate IDs CP-G1..CP-G7, disposition tokens, evidence line, layout footguns, seven-block summary from the spec
- Produces: CREATE_PATH text that makes `test_create_path_gate_manifest` pass

- [ ] **Step 1: Confirm the contract test is still red on CREATE_PATH**

Run: `python -m unittest tests.FAKESECRET_g2h3i4j5k6l7m8n9o0p1 -v`

Expected: FAIL on missing `CP-G1` (or whatever first missing token is).

- [ ] **Step 2: Insert the gate manifest after the Scope table** (after the `archi-documentation` row, before `## When mutations are allowed`)

Insert this block verbatim:

```markdown
## Run gates (hedge-free)

Guidance elsewhere in this file may use "prefer" or "when useful". The table below may not. If a gate is unmet, the draft is not ready unless the specialist names an exception: which gate, which view or element, and why. "Ran long" is not an exception.

| ID | Gate | Pass condition |
|----|------|----------------|
| CP-G1 | Confirm-before-mutate | No mutating MCP call unless View Plan confirmation is `approved`. |
| CP-G2 | Fresh IDs | At the start of every specialist, and after any compaction, re-query IDs with `search-elements` / `get-view-contents`. Identify unnamed notes, images, junctions, and groups by content and geometry, never by batch order. |
| CP-G3 | Disposition complete | Every candidate in the hand-off is `captured`, `folded`, `needs-user`, or `out-of-scope`. Silence is a fail. |
| CP-G4 | No invention | Every created element has `Evidence: stated \| inferred \| existing - <source>` as the first documentation line. No on-canvas element without that citation. |
| CP-G5 | Annotate last | Notes, legends, and images are the last objects placed on a view. Omit `height` on notes. Place notes with `position: below-content`. A later geometry change re-opens CP-G6. |
| CP-G6 | Render close-out | After any add, move, resize, or style on a view, including notes, the last actions are `assess-layout` (dispose every non-pass `ratingBreakdown` dimension; `partial` and `not-checked` are unverified) and an `export-view` PNG that is inspected. |
| CP-G7 | First generation is a draft | The documentation specialist ends the run at a draft checkpoint. Do not present the model as finished. |

Offline assist for CP-G3: `python helpers/disposition.py ledger.md`.
```

In the live file, write a real pipe in the evidence example (`stated | inferred | existing`), not the escaped `\|` if the table cell can hold it. The contract test looks for the substring `Evidence: stated | inferred | existing`. Put that exact substring somewhere in CREATE_PATH (the gate table cell or the provenance section). If markdown table escaping eats the pipes, also put the canonical line in a fenced code block in the provenance section:

```
Evidence: stated | inferred | existing - <source>
```

- [ ] **Step 3: Insert working mode after "When mutations are allowed"** (before `## Orchestrator-dispatched only`)

```markdown
## Working mode (the model is the checkpoint)

A modelling run can compact or stop mid-way. Conversation memory is not the ledger.

1. Re-query IDs at the start of every specialist (`search-elements`, `get-view-contents`). Do not reuse IDs remembered from an earlier turn.
2. Unnamed view objects (notes, images, junctions, groups) have no name to match. Identify them by content and geometry from a fresh `get-view-contents`. Never assume "note 2 of 3" from an earlier `bulk-mutate` batch.
3. Keep element names stable and domain-derived so `get-or-create-element` / search-before-create stay idempotent.
4. Optional: write a short run marker with `update-model` (confirmation status, viewpoints in scope, last specialist completed) so the next run diffs against the model.
```

- [ ] **Step 4: Insert provenance after "Inspect before create"** (before `## Model coherence and reuse`)

```markdown
## Provenance on create (CP-G4)

Every created element starts its `documentation` field with:

```
Evidence: stated | inferred | existing - <source>
```

- `stated` — the user or the approved View Plan said it
- `inferred` — the specialist deduced it (keep elicit inferences; do not upgrade them)
- `existing` — already in the model and reused

Never write a bare `Rationale:` line for an inferred why. Omit Rationale, or write `Rationale (inferred):`. Do not add evidence specializations or label glyphs.

Creating specialists (motivation, capability-strategy, business, application, technology-physical, implementation-migration, traceability) include a **Candidate disposition** table in the Specialist Result. Valid dispositions: `captured` (target `element @ view`), `folded` (parent plus reason), `needs-user` (question), `out-of-scope` (why). Validate with `python helpers/disposition.py`.
```

- [ ] **Step 5: Extend Return-to-orchestrator payload**

After item 6 (Confirmation assumption), add:

```markdown
7. **Candidate disposition** — table of every hand-off candidate (creating specialists). `archi-model-qa` treats an undispositioned candidate as a finding; do not silent-fix.
```

- [ ] **Step 6: Layout footguns**

After the Layout set sentence in `## Inventory tools only`, add:

```markdown
Layout footguns (layout specialist; recipes remain source of truth):

- Grouped or nested default for structure views with more than about 10 elements; flat needs a recorded reason
- Annotate last (CP-G5): omit `height` on `add-note-to-view` and note `update-view-object`; `position: below-content`, never `above-content`
- Junctions about 14 by 14; do not pass a layer-folder `folderId` for a Junction
- Nested hub (six or more connections): resize the hub, then `auto-route-connections`; re-route alone is inert
- Walk `ratingBreakdown`; do not sign off on `overallRating` alone; `partial` and `not-checked` are unverified
- Last action includes `export-view`; the PNG is authoritative where the metric under-counts
- Literal `&` in names and labels, never `&amp;`
```

Add `export-view`, `update-view-object`, `add-note-to-view`, `get-view-contents` to the layout set list if missing.

- [ ] **Step 7: Draft close-out in OBJ-6**

Replace the completion-summary minimum list (currently Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run) with:

```markdown
1. End every modelling run with a completion summary covering at minimum: Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run, Deliberately Deferred, Improve Next. First generation is a draft (CP-G7).
```

- [ ] **Step 8: Run CREATE_PATH contract test**

Run: `python -m unittest tests.FAKESECRET_g2h3i4j5k6l7m8n9o0p1 -v`

Expected: PASS.

- [ ] **Step 9: Prose check CREATE_PATH**

Run: `python ~/.zcode/scripts/prose_check.py docs/CREATE_PATH.md`

Fix em dashes or slop the checker flags. Do not introduce em dashes while editing.

- [ ] **Step 10: Commit**

```bash
git add docs/CREATE_PATH.md tests/test_specialist_contract.py
git commit -m "docs: add run gates, working mode, and provenance to CREATE_PATH"
```

If Task 3 was not committed, this commit includes `tests/test_specialist_contract.py`.

---

### Task 5: Creating specialists plus elicit and model-qa

**Files:**
- Modify: `skills/archi-motivation/SKILL.md`
- Modify: `skills/archi-capability-strategy/SKILL.md`
- Modify: `skills/archi-business/SKILL.md`
- Modify: `skills/archi-application/SKILL.md`
- Modify: `skills/archi-technology-physical/SKILL.md`
- Modify: `skills/archi-implementation-migration/SKILL.md`
- Modify: `skills/archi-traceability/SKILL.md`
- Modify: `skills/archi-model-qa/SKILL.md`
- Modify: `skills/archi-elicit/SKILL.md`

**Interfaces:**
- Consumes: disposition grammar from CREATE_PATH / `helpers/disposition.py`
- Produces: each creating skill contains the heading `Candidate disposition` and the four tokens; model-qa contains `undispositioned`; elicit contains `Evidence:`

The seven creating skills share the same output template shape. Apply the **same insertion** to each. Do not invent per-layer essays.

- [ ] **Step 1: Run creating-specialist contract test (expect fail)**

Run: `python -m unittest tests.FAKESECRET_i3j4k5l6m7n8o9p0q1r2 -v`

Expected: FAIL, first skill missing `Candidate disposition`.

- [ ] **Step 2: Insert the table into each creating skill**

In each of the seven SKILL.md files, inside the output template markdown fence, after `### Open questions` and before `### Next specialist hint` (traceability: after Open questions / before the Trace Gap Table if that heading exists; if neither, append before the closing fence), insert:

```markdown
### Candidate disposition
| Candidate | Disposition | Target | Reason |
|-----------|-------------|--------|--------|
| … | captured \| folded \| needs-user \| out-of-scope | element @ view, or parent | one line |
```

Also add to **Return to orchestrator** (or equivalent numbered list) a bullet:

```markdown
4. Candidate disposition table (every hand-off candidate; validate with `python helpers/disposition.py` when a file artifact exists)
```

Renumber only if the file already uses numbers; otherwise keep a bullet.

On create procedure (Step 2 Element set, or equivalent), add one sentence after "Create only when missing":

```markdown
5. Set the first documentation line to `Evidence: stated | inferred | existing - <source>` (CP-G4). Do not write a bare Rationale for an inferred why.
```

If Step 2 already has a numbered list of four items, this is item 5. If not numbered, use a bullet with the same sentence.

- [ ] **Step 3: model-qa**

In `skills/archi-model-qa/SKILL.md` Step 2 (Check dimensions), add item 8:

```markdown
8. Undispositioned hand-off candidates (CP-G3). A candidate with no `captured` / `folded` / `needs-user` / `out-of-scope` row is a finding; explain and propose (ask the user, or fold with a reason). Never silent-drop.
```

In the Findings table guidance, no extra columns required. The word `undispositioned` must appear (contract test is case-insensitive).

- [ ] **Step 4: elicit**

In `skills/archi-elicit/SKILL.md` under **Return to orchestrator**, after the three existing items, add:

```markdown
4. Inferred fields stay `inferred`. Downstream specialists must carry them as `Evidence: inferred - elicit` (or a more specific source). Do not upgrade an inference to stated.
```

The substring `Evidence:` must appear (contract test).

- [ ] **Step 5: Run the three contract tests**

Run:

```
python -m unittest tests.FAKESECRET_i3j4k5l6m7n8o9p0q1r2 tests.FAKESECRET_s4t5u6v7w8x9y0z1a2b3 tests.FAKESECRET_c1d2e3f4g5h6i7j8k9l0 -v
```

Expected: PASS.

- [ ] **Step 6: MCP ref scan**

Run: `python helpers/validate_skill_mcp_refs.py`

Expected: exit 0. If a new backticked tool name is unknown, fix the skill text; do not invent tools.

- [ ] **Step 7: Commit**

```bash
git add skills/archi-motivation/SKILL.md skills/archi-capability-strategy/SKILL.md skills/archi-business/SKILL.md skills/archi-application/SKILL.md skills/archi-technology-physical/SKILL.md skills/archi-implementation-migration/SKILL.md skills/archi-traceability/SKILL.md skills/archi-model-qa/SKILL.md skills/archi-elicit/SKILL.md
git commit -m "feat: require candidate disposition and evidence lines on creating specialists"
```

---

### Task 6: Layout footguns

**Files:**
- Modify: `skills/archi-layout/SKILL.md`

**Interfaces:**
- Consumes: CP-G5, CP-G6, inventory tools `export-view`, `add-note-to-view`, `update-view-object`, `assess-layout`
- Produces: skill text that makes `test_layout_footguns` pass

- [ ] **Step 1: Run layout contract test (expect fail)**

Run: `python -m unittest tests.test_specialist_contract.SpecialistContractTests.test_layout_footguns -v`

Expected: FAIL (missing `export-view` and/or `below-content`).

- [ ] **Step 2: Extend MCP tools list**

In the MCP tools section, add to Assess: `export-view`. Keep existing assess tools. Notes/groups line already mentions `add-note-to-view`; add `update-view-object`.

Exact resulting block:

```markdown
Assess: `assess-layout`, `get-view-contents`, `detect-hub-elements`, `export-view`
Layout: `auto-layout-and-route`, `layout-flat-view`, `layout-within-group`, `arrange-groups`, `optimize-group-order`, `apply-positions`
Spacing: `adjust-view-spacing`, `apply-spacing-recommendations`, `apply-element-spacing-recommendations`, `apply-group-spacing-recommendations`, `resize-elements-to-fit`
Connections: `auto-route-connections`, `auto-connect-view`
Notes/groups: `add-group-to-view`, `add-note-to-view`, `update-view-object` when hand-off allows
```

- [ ] **Step 3: Replace Step 2 (Choose strategy) with grouped default plus footguns**

Replace the current Step 2 bullet list with:

```markdown
### Step 2 — Choose strategy
- Structure views with more than about 10 elements: grouped or nested (`add-group-to-view` / `parentViewObjectId`). Flat needs a recorded reason in the hand-back.
- Flat structural views (small, or justified): `layout-flat-view` or `auto-layout-and-route`
- Grouped layered views: `arrange-groups` / `layout-within-group`
- Connection spaghetti: `auto-route-connections` after positions stable
- Nested hub (six or more connections): resize the hub, then `auto-route-connections`. Re-route alone is inert.
- Junctions: about 14 by 14. Do not pass a layer-folder `folderId` for a Junction.
- Literal `&` in names and labels, never `&amp;`.
```

- [ ] **Step 4: Annotate last and render close-out**

After current Step 4 (Re-assess), or rename it, ensure this sequence exists as Step 4 and Step 5. If Step 5 Hand-back already exists, insert the new steps before Hand-back and keep Hand-back last.

```markdown
### Step 4 — Re-assess dimensions
`assess-layout` again. Walk `ratingBreakdown`. Dispose every non-pass dimension (fix or record why accepted). Treat `partial` and `not-checked` as unverified, not passed. Do not sign off on `overallRating` alone.

### Step 5 — Annotate last (CP-G5)
Only after layout and routing are finished, add notes or legends with `add-note-to-view`. Omit `height` so the server auto-fits. Place with `position: below-content`, never `above-content`. Do not run layout, route, or resize after notes. If geometry must change, re-place the note after it.

### Step 6 — Render close-out (CP-G6)
After any add, move, resize, or style, including notes: `assess-layout` then `export-view`. Inspect the PNG. The render wins if the metric under-counts.

### Step 7 — Hand-back
```

Renumber the output template if it still says Step 5 Hand-back only. Keep the Specialist Result template; add a residual-issues column note that it must mention `ratingBreakdown` leftovers.

In the Views laid out table, change header if needed:

```markdown
| View | Tools used | Residual issues |
|------|------------|-----------------|
| … | … | ratingBreakdown leftovers or none |
```

The contract test needs `omit` and `height` in the file (case-insensitive). The sentence "Omit `height`" satisfies both.

- [ ] **Step 5: Run layout contract + MCP refs**

Run:

```
python -m unittest tests.test_specialist_contract.SpecialistContractTests.test_layout_footguns -v
python helpers/validate_skill_mcp_refs.py
```

Expected: unittest PASS, validator exit 0.

- [ ] **Step 6: Commit**

```bash
git add skills/archi-layout/SKILL.md
git commit -m "feat: encode layout footguns and render close-out in archi-layout"
```

---

### Task 7: Draft close-out in documentation and orchestrator

**Files:**
- Modify: `skills/archi-documentation/SKILL.md`
- Modify: `skills/archi-orchestrator/SKILL.md`

**Interfaces:**
- Consumes: seven `REQUIRED_BLOCKS` from Task 2
- Produces: both skills contain `Deliberately Deferred` and `Improve Next`; orchestrator also contains `draft` (case-insensitive)

- [ ] **Step 1: Run the two contract tests (expect fail)**

Run:

```
python -m unittest tests.FAKESECRET_c2d3e4f5g6h7i8j9k0l1 tests.FAKESECRET_k2l3m4n5o6p7q8r9s0t1 -v
```

Expected: FAIL on missing `Deliberately Deferred`.

- [ ] **Step 2: Documentation skill**

In `skills/archi-documentation/SKILL.md`:

Replace

```
Required completion-summary blocks: Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run.
```

with

```
Required completion-summary blocks: Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run, Deliberately Deferred, Improve Next. First generation is a draft (CP-G7). A legitimate empty deferred/next block is the word `none`.
```

In the Completion summary template list, after Specialists Run, add:

```markdown
- Deliberately Deferred: …
- Improve Next: …
```

In Step 5 (Completion summary), add one sentence:

```markdown
Do not present the model as finished. Deferred and Next are required blocks; use `none` when there is nothing to list.
```

- [ ] **Step 3: Orchestrator skill**

In `skills/archi-orchestrator/SKILL.md`, in **Documentation and NL-change loop**, replace the consume-summary bullet that lists five blocks with:

```markdown
- Consume its **completion summary** (Views Touched, Decisions, Open Questions, Confirmation Status, Specialists Run, Deliberately Deferred, Improve Next) and schema validation status.
```

In **Completion** (the section that currently says "End the run when documentation specialist returns a completion summary"), replace that paragraph with:

```markdown
End the first generation at a **draft checkpoint** (CP-G7). After the documentation specialist returns a valid completion summary, stop and ask the user to confirm, deepen (pick from Improve Next / Deliberately Deferred), or stop. Do not present the model as finished.

Decide-and-log by default. Ask only when the choice is costly to reverse, evidence is missing, and a wrong guess wastes significant work. More than about five open questions means under-deciding; log the reversible ones and continue.
```

The word `draft` must appear.

In **Completion summary (when stopping)** item 4, mention the two new blocks:

```markdown
4. Documentation outcome: completion summary (or path), including Deliberately Deferred and Improve Next, rationale validation status, NL-change impact if any
```

- [ ] **Step 4: Run contract tests**

Run:

```
python -m unittest tests.FAKESECRET_c2d3e4f5g6h7i8j9k0l1 tests.FAKESECRET_k2l3m4n5o6p7q8r9s0t1 -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/archi-documentation/SKILL.md skills/archi-orchestrator/SKILL.md
git commit -m "feat: treat first-generation modelling as a draft close-out"
```

---

### Task 8: Changelog and full verification

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: all prior tasks
- Produces: Unreleased section; green full suite; green MCP ref scan; frozen viewpoint-select digest unchanged

- [ ] **Step 1: Add Unreleased to CHANGELOG.md**

Insert at the top, after the intro paragraph and before `## v1.6 (2026-08-28)`:

```markdown
## Unreleased

Run operating system for specialists, stolen from the repo-to-archi prompt without the reverse-engineering product.

- CREATE_PATH gate manifest CP-G1 through CP-G7, working mode, provenance line, layout footguns
- `helpers/disposition.py` validates captured / folded / needs-user / out-of-scope ledgers
- Completion summaries require Deliberately Deferred and Improve Next; first generation is a draft
- Creating specialists return a candidate disposition table; model-qa flags undispositioned rows
- archi-layout annotate-last, omit note height, `export-view` close-out
```

No em dashes. Technical voice.

- [ ] **Step 2: Prose check durable files touched this plan**

Run:

```
python ~/.zcode/scripts/prose_check.py docs/CREATE_PATH.md docs/specs/run-operating-system.md CHANGELOG.md
```

Fix findings or justify (copyright HTML comments only).

- [ ] **Step 3: Full unit suite**

Run: `python -m unittest discover -s tests -q`

Expected: `OK`. If `test_viewpoint_select_frozen` fails, revert any accidental edit to `skills/archi-viewpoint-select/SKILL.md`.

- [ ] **Step 4: MCP ref scan**

Run: `python helpers/validate_skill_mcp_refs.py`

Expected: exit 0.

- [ ] **Step 5: Disposition helper smoke on a tiny ledger**

Write a temp file is unnecessary if Task 1 tests passed. Re-run:

```
python -m unittest tests.test_disposition tests.test_completion_summary_schema tests.test_specialist_contract -q
```

Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: record unreleased run operating system"
```

If prose_check also cleaned CREATE_PATH or the spec, include those files in the same commit.

---

## Self-review

**Spec coverage**

| Spec section | Task |
|--------------|------|
| Gate manifest CP-G1..G7 | Task 4 |
| Working mode / fresh IDs | Task 4 |
| Disposition grammar + helper | Task 1, 4, 5 |
| Provenance line, no glyphs | Task 4, 5 |
| Layout footguns + render | Task 4, 6 |
| Seven-block draft close-out | Task 2, 4, 7 |
| Structural tests | Task 3 |
| Elicit inferences survive | Task 5 |
| model-qa undispositioned | Task 5 |
| Out: viewpoint-select frozen | Task 8 verify |
| Out: eval GATES / docs_coverage | no task |
| CHANGELOG | Task 8 |

**Placeholder scan:** none. Each step has the markdown or Python to paste.

**Type consistency:** `captured` / `folded` / `needs-user` / `out-of-scope`; evidence grades `stated` / `inferred` / `existing`; gates `CP-G1`..`CP-G7`; completion blocks `Deliberately Deferred` and `Improve Next`; helper names `parse_markdown_table`, `validate_ledger`.
