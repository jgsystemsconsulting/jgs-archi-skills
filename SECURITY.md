<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Security Policy

## Reporting a vulnerability

Report security issues privately via GitHub security advisories on this
repository (Security, Advisories, New advisory), or open a pull request with
the fix when that is safe. Do not open a public issue for a suspected
vulnerability. Use GitHub Security, Advisories, New advisory on this
repository.

We aim to acknowledge reports within 5 business days. Include the affected
version (see RELEASE-INFO.txt), reproduction steps, and impact.

## Scope notes

These skills drive a local Archi model through the JGS Archi Bridge MCP on
loopback. Sensitive surfaces are: the model file on disk, any documentation
fields written into that model, and the MCP endpoint the operator points at.
The pack does not hold API keys and does not phone home.

## General support

Non-security questions: open a bug report using the issue form. Do not use
the advisory channel for ordinary defects.
