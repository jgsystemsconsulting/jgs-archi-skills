<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Multi-view reuse narrative

1. Specialist A (application) searches for "Customer Portal" → finds `el-portal-1`.
2. `reuse_inspect` decision = **reuse**.
3. Adds `el-portal-1` to Application Structure view (no create-element).
4. Specialist B (later or parallel with registry) reads `reuse_registry` → same ID.
5. Adds `el-portal-1` to Application Usage view.
6. Result: one model element, two views; duplicates minimised; naming identical.
7. model-qa runs `naming_convention conflicts` on usages → 0 conflicts.
