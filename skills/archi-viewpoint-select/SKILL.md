---
name: archi-viewpoint-select
description: "Ground ArchiMate viewpoint choices to stakeholder, concern, purpose, and abstraction level. Orchestrator-dispatched."
---

# archi-viewpoint-select

Orchestrator-dispatched specialist. Not a primary user entrypoint.

## Purpose

Given intent plus draft viewpoints, produce a Viewpoint Trace Table proving each choice maps to stakeholder, concern, purpose, and abstraction level (VIEW-01). When no standard viewpoint fits, propose an organisation-specific viewpoint with justification that stays ArchiMate-compliant (VIEW-02).

## MCP resources (read-only)

- `archimate://recipes/index`
- `archimate://reference/archimate-view-patterns`
- `archimate://reference/archimate-layers`

## Output

```markdown
## Viewpoint Trace Table
| Viewpoint | Stakeholder | Concern | Purpose | Abstraction | Standard? | Justification |

## Organisation-Specific Proposals

## Rejected Alternatives
```

## Rules

- Prefer standard viewpoints from recipes and view-patterns.
- No MCP mutations in this skill.
- Dispatch only via orchestrator (SPEC-02).
