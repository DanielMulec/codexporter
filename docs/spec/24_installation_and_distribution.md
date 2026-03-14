# Installation And Distribution

## Status

- Phase: analysis and discussion
- Date: March 13, 2026
- Scope: v1 installation and distribution boundary

## Purpose

This document defines how the v1 skill is packaged in the repository and what part of the repository is intended to be installed through the skill installer.

## Global Install Model

V1 is intended to be installed once as a global Codex skill.

That means:

- the user installs the skill once into the global Codex skills directory
- the same installed skill is then reused across project contexts
- the user should not need to reinstall the skill for each project workspace

## Installable Repository Boundary

The installable skill artifact lives at:

- `skills/export/`

Only that directory is the supported install target for GitHub-based skill installation.

The repository root is a development surface, not the supported install target.

## Installable Contents

The installable skill directory may include:

- `SKILL.md`
- runtime scripts or modules required by the skill
- assets required at runtime
- a minimal README or LICENSE when useful

## Non-Installable Development Surface

The following repository content is development-only and must not be part of the installable skill payload:

- `AGENTS.md`
- `CHANGELOG.md`
- `docs/spec/`
- tests
- fixtures
- development-only validation evidence
- repository-only tooling files that are not required by the installed skill

## Runtime Context Rule

The install location of the skill must not determine export destination.

At invocation time, the skill must resolve the active project root from the current session or workspace context.

Export artifacts must then be written into:

- `codex_exports/` under that active project root

The installed skill directory must never be treated as the export destination.

## Failure Rule

If the active project root cannot be determined responsibly:

- do not guess
- do not write export artifacts into the installed skill directory
- fail clearly and tell the user what could not be determined

## Future Compatibility Rule

Later packaging decisions may add release automation, version tags, or distribution refinements, but they must preserve:

- one global installable skill boundary
- reuse across project contexts without per-project reinstallation
- export destination tied to the active project context rather than the install location
