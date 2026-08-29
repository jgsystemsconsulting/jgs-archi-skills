<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Expected tool / helper sequence (OBJ-4)

1. search-elements (name/type filters)
2. helpers/reuse_inspect.py on snapshot → reuse|create|ambiguous
3. helpers/naming_convention.py normalize (on create path)
4. get-or-create-element OR add-to-view existing ID
5. update reuse_registry in hand-back
6. model-qa: naming_convention conflicts + compliance_checklist
