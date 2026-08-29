<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Compliance validation offline evidence (v1.4 / OBJ-5)

Offline pack proving explain-and-propose compliance validation without live Archi MCP.

## Scenario

Validate a multi-view claims modelling slice: clean pass path, then a fail path covering unknown element type, illegal relationship type, illegal endpoints, abstraction mismatch, and cross-view naming divergence.

## Artifacts

- `pass-slice.json`: compliant model slice
- `fail-slice.json`: intentional violations across OBJ-5 dimensions
- `pass-findings.json`: validator output (expect empty findings)
- `fail-findings.json`: validator output with problem + proposed_alternative per finding
- `tool-sequence.md`: expected MCP + helper sequence for live/offline paths
- `regression.md`: suite status + viewpoint-select freeze digest

## Commands

```bash
python helpers/compliance_validate.py docs/evidence/compliance-validation-offline/pass-slice.json --json
python helpers/compliance_validate.py docs/evidence/compliance-validation-offline/fail-slice.json --json
python -m unittest discover -s tests -q
python helpers/validate_skill_mcp_refs.py
```

## Freeze

`archi-viewpoint-select` SHA256 must remain:

`01ad2cc359bb1a4e42a26d8eda383b394fc73a6409373736eba1c5bd6caf94ea`
