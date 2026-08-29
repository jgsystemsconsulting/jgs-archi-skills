<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Gates: ArchiMate eval loop (senior-bar model quality)

OWNS: GATES.md, docs/eval/**, docs/evidence/eval-loop/**, helpers/**, skills/**, tests/**

Scope: raise the skill suite until an unattended run against the frozen
scenario (docs/eval/reference-scenario.md) produces an ArchiMate model that
passes metamodel, naming, rationale, documentation-coverage, and layout gates
on a fresh model, confirmed by a second fresh-model run.

External tool requirement: all CHECK commands need Python 3.10+ on PATH
(standard for this repo); ledger designed for the default platform shell.

- [x] G0: this ledger states outcomes that can fail
  CHECK: node "C:/Users/gower/.zcode/skills/unlazy/scripts/gate-lint.mjs" GATES.md
  EXPECT: LINT OK
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=48630b7361dd44ee870917b12c3d19b9d7bdea738aaca16bb04d4cab83b772d2; output-bytes=8

- [x] G1: frozen scenario exists and is complete for unattended elicitation
  CHECK: python docs/eval/gate_checks.py scenario
  EXPECT: scenario check passed
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=7204890ebb806b3bb43e6057e9f6a1c03685c6985b76fa83b8c5bcd7307d3575; output-bytes=23

- [x] G2: full unit-test suite passes after the final iteration
  CHECK: python -m unittest discover -s tests -q
  EXPECT: /^OK$/m
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=8e221e65813a85e2c79bd82fd9ed821cfa6aabdd7360b39a205ef73f23e0f6ab; output-bytes=102

- [x] G3: final model slice has zero metamodel violations
  CHECK: python helpers/compliance_validate.py --json docs/evidence/eval-loop/iter-final/slice.json
  EXPECT: "ok": true
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=0b4b9044442475ef746f829a7ba64e8e3f69b883c086c005b4524d30eab61f62; output-bytes=39

- [x] G4: final model has zero cross-view naming conflicts
  CHECK: python helpers/naming_convention.py conflicts docs/evidence/eval-loop/iter-final/usages.json
  EXPECT: "conflict_count": 0
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=046d494270885a933e4972c353b7a0d0139cdb57c6f6a1e908c6210cbc05703f; output-bytes=176

- [x] G5: final rationale bundle passes schema with zero findings
  CHECK: python helpers/rationale_schema.py --bundle docs/evidence/eval-loop/iter-final/rationale --json
  EXPECT: "findings": []
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=c8fbc26f56dd06f22a398f7888aed59d2a2591e75b440a1794fbe986187a2d44; output-bytes=24

- [x] G6: every final-model element and relationship has a meaningful documentation field
  CHECK: python helpers/docs_coverage.py --json docs/evidence/eval-loop/iter-final/slice.json
  EXPECT: "ok": true
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=0b4b9044442475ef746f829a7ba64e8e3f69b883c086c005b4524d30eab61f62; output-bytes=39

- [x] G7: every final view passes the layout check with zero fixup findings
  CHECK: python helpers/layout_check.py --json docs/evidence/eval-loop/iter-final/views.json
  EXPECT: "ok": true
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=78d4a2aeb6028532d258091769dce8d65826734f258d2a84919d9bd130cbbb2d; output-bytes=698

- [x] G8: every iteration is logged with before/after scores, changes, and evidence paths
  CHECK: python docs/eval/gate_checks.py iterations
  EXPECT: iterations check passed
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=6b9c1225a74810168e683b7a5d56e60db7665867d592f7bdb403d074fb0c0a03; output-bytes=25

- [x] G9: confirmation run on a fresh model reproduces all model-quality gates green
  CHECK: python docs/eval/gate_checks.py confirmation
  EXPECT: confirmation check passed
  EVIDENCE: exit=0; shell=C:\Windows\system32\cmd.exe; cwd=C:\Users\gower\OneDrive\Documents\GitHub\jgs-archi-skills; path=2c6ab9c02f2d/64 entries; EXPECT=matched; output-sha256=210d81e89e67e15966cf444f03497f2fde7e1c421023670cd46f0bc28eda7f4c; output-bytes=27
