<!-- Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/jgs-archi-skills. See LICENSE. -->
<!-- SPDX-License-Identifier: MIT -->

# Modelling conventions (JGS house style)

This is the JGS house style for Archi models produced by this skill suite.
It is not the ArchiMate language reference. Element types, relationship
legality, and viewpoint content stay on the JGS Archi Bridge MCP resources.
Read those at runtime. Do not copy catalogs into skills or into this file.

## Purpose and non-goals

Purpose: consistent names, useful documentation fields, a predictable
Archi folder tree, and views that stay projections of one model.

Non-goals: replacing MCP recipes, auto-renaming user language, locking
architectural decisions without the user.

## Naming

Apply `title-collapse-v1` for whitespace (see CREATE_PATH). Then apply
aspect rules. Do not suffix the ArchiMate type onto the name.

- Structure (actors, roles, components, objects, nodes): noun phrase.
  `CRM` not `CRM Application`. Keep acronyms and product names as the
  user said them.
- Behaviour (processes, functions, interactions): verb-noun.
  `Handle Customer Inquiry` not `Invoice`.
- Motivation: desired state or pressure, not a project slogan.

Never auto-rename. If a hint fires, propose an alternative and wait.

## Element descriptions

First line is always the evidence citation from CREATE_PATH:

```
Evidence: stated | inferred | existing - <source>
```

Then one or two sentences: what the concept is, why it exists, and a
boundary or owner when known. Do not repeat the name. Do not repeat the
type name.

## Relationship descriptions

Say why the dependency exists (who needs what, which flow, which
realization). Do not write the relationship type as the documentation.

`create-relationship` takes no documentation parameter. Set documentation
with `update-relationship` immediately after create (CREATE_PATH).

## Folder structure

Default Archi folders:

- Motivation
- Strategy
- Business
- Application
- Technology
- Physical
- Implementation & Migration
- Views

Put each element in the folder that matches its aspect. Nested folders
under that layer are allowed (`Business/Processes`). Junctions do not
belong in a layer folder. Views belong under `Views` or `Views/<name>`.

Live tools (inventory only): `get-folders`, `get-folder-tree`,
`create-folder`, `move-to-folder`. Propose a move; do not apply it
until authorized.

## View hygiene

One concern per view. Reuse the same model element across views. Do not
create a second element for the same concept. Inspect with
`search-elements` / `get-or-create-element` before create (CREATE_PATH
OBJ-4).

## Overrides

The View Plan may set `naming_policy` (already exists). Folder placement
always uses the default tree above; there is no `folder_policy` override
in this pack. Client-specific naming is an override, not a silent fork
of this document.

## Checks agents must run

Offline, on a captured slice, after a modelling batch:

```text
python helpers/docs_coverage.py slice.json --require-evidence [--json]
python helpers/naming_convention.py conflicts usages.json
python helpers/naming_convention.py aspect-hints usages.json
python helpers/folder_convention.py slice.json [--json]
```

Live legality still comes from MCP relationship and layer resources plus
`helpers/compliance_validate.py`. House-style findings are explain-and-propose
only. Eval-loop G6 runs `docs_coverage` without `--require-evidence`.
