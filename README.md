# Codex Exporter

Codex Exporter is a Codex skill that exports the current live session to markdown.

The user-facing skill name is `export`, so the intended invocation is `$export`.

## Current State

- Installable skill boundary: `skills/export/`
- User command: `$export`
- Internal Python package: `codexporter`
- Primary artifact: one markdown file per successful export
- Output location: `codex_exports/` under the active project root
- Incremental behavior: later exports only include new session content and advance a JSON sidecar checkpoint
- Failure behavior: fail clearly instead of guessing or writing into the installed skill directory

## What The Skill Exports

The v1 export stays close to what the user visibly experienced in Codex:

- visible user messages
- visible assistant replies
- visible commentary or progress updates
- visible tool calls and tool outputs
- compact session metadata

The exporter does not include hidden reasoning or raw internal instruction payloads.

## Install Boundary

The repository root is the development surface.

The supported install target is only:

- `skills/export/`

The skill is intended to be installed once globally and then reused across project contexts.

The installed skill directory must never become the export destination.

## Runtime Behavior

When `$export` runs successfully, it writes:

- a markdown export artifact into `codex_exports/`
- a JSON checkpoint sidecar into the same directory

Repeated exports in the same session are incremental.

If there is no new exportable content since the last successful export, the skill reports that directly and does not create a new markdown file.

If the active project root cannot be determined safely, the skill stops with a user-facing error instead of writing into the installed skill directory.

## Repository Layout

- `skills/export/`: installable skill payload
- `skills/export/scripts/export_skill.py`: development entry script
- `skills/export/codexporter/`: exporter implementation
- `tests/`: automated test suite
- `docs/spec/`: product and engineering specification
- `docs/validation/`: manual validation records

## Local Development

Create a virtual environment and install the dev dependencies:

```bash
python3 -m venv .venv
./.venv/bin/pip install -e .[dev]
```

Run the current quality gates:

```bash
./.venv/bin/pytest
./.venv/bin/mypy skills/export tests
./.venv/bin/ruff check .
./.venv/bin/ruff format --check .
```

Run the exporter directly from the repo during development:

```bash
./.venv/bin/python skills/export/scripts/export_skill.py \
  --project-root "$PWD" \
  --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

## Validation Snapshot

Current automated baseline:

- 18 passing `pytest` cases across unit behavior, service flow, public invocation flow, degraded mode, and checkpoint edge cases
- `mypy` in `strict` mode
- `ruff check`
- `ruff format --check`

Current manual validation status:

- macOS Codex app: partial validation recorded
- macOS Codex CLI: target, but manual evidence still needs to be recorded
- Linux Codex CLI: target, not yet validated
- Windows Codex CLI: target, not yet validated
- Windows Codex app: target, not yet validated

See:

- `docs/spec/22_platform_validation.md`
- `docs/validation/macos_app.md`

## Notes

This repository documents and implements the current canonical skill behavior.

It does not aim to preserve older local skill names or compatibility shims.
