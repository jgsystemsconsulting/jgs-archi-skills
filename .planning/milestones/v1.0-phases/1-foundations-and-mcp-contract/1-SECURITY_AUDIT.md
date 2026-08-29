<!-- Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE. -->
<!-- SPDX-License-Identifier: LicenseRef-JGSC-Proprietary -->

# Phase 1 Security Audit

**Date:** 2026-08-27
**ASVS level:** 1
**Block on:** high (config)

## Surface

Local file install to `~/.zcode/skills/`, offline JSON allowlist, no network client, no secrets.

## Findings

### high / critical
None.

### medium / low
- L1: install.py deletes prior dest only when SKILL.md present — intentional; documented.

**Verdict:** SECURED
