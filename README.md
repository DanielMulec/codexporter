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

Each contributor should create a local virtual environment in `.venv/`.

`.venv/` is machine-specific and is intentionally not committed to Git. Create it locally, recreate it when needed, and do not copy it between machines.

### macOS and Linux

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the current quality gates:

```bash
python -m pytest
python -m mypy skills/export tests
python -m ruff check .
python -m ruff format --check .
```

Run the exporter directly from the repo during development:

```bash
python skills/export/scripts/export_skill.py \
  --project-root "$PWD" \
  --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

### Windows (PowerShell)

Create and activate the virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the current quality gates:

```powershell
python -m pytest
python -m mypy skills/export tests
python -m ruff check .
python -m ruff format --check .
```

Run the exporter directly from the repo during development:

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }

python skills/export/scripts/export_skill.py `
  --project-root $PWD `
  --codex-home $codexHome
```

When invoking the installed global skill on Windows without an activated virtual environment, prefer `py -3` over plain `python`. On some Windows setups, `python` resolves to the Microsoft Store stub instead of a working interpreter.

### Notes

- Prefer `python -m ...` after activating the virtual environment. This avoids platform-specific `.venv/bin/...` and `.venv\\Scripts\\...` command paths.
- Validation evidence in `docs/validation/` may contain machine-specific example paths. Those are recorded observations, not required contributor paths.
- The supported development baseline is Python 3.12 or newer.

## Validation Snapshot

Current automated baseline:

- 31 passing `pytest` cases on the maintained macOS-local baseline across unit behavior, service flow, public invocation flow, degraded mode, checkpoint edge cases, thread-accurate session targeting, Windows-style path-shape equivalence, Windows-safe fixture rendering, localized CLI failure and omission messaging, explicit hidden-reasoning and internal-instruction exclusion, optional-metadata omission, and timezone-fallback behavior
- On March 27, 2026, fresh Linux and Windows `.venv` reruns also passed `pytest`, `mypy`, `ruff check`, and `ruff format --check`
- `mypy` in `strict` mode
- `ruff check`
- `ruff format --check`

Current manual validation status:

- macOS Codex app: validated
- macOS Codex CLI: validated
- Linux Codex CLI: validated
- Windows Codex CLI: validated
- Windows Codex app: validated

See:

- `docs/spec/22_platform_validation.md`
- `docs/validation/macos_app.md`
- `docs/validation/macos_cli.md`
- `docs/validation/linux_cli.md`
- `docs/validation/windows_cli.md`
- `docs/validation/windows_app.md`

Windows automated validation note:

- On March 27, 2026, the cross-platform Windows test-harness close-out landed: UTC-only unit test construction is now host-independent, fenced markdown JSON expectations are rendered structurally, and repo-root `ruff` traversals now ignore `pytest-cache-files-*` temp directories.
- On March 27, 2026, a fresh Windows `.venv` rerun passed `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .`.
- On March 27, 2026, controlled Windows CLI and Windows app close-out replays captured German checkpoint-failure messaging, explicit persisted-session-history failures under denied read access, and same-workspace ambiguity recovery from isolated temporary Codex homes derived from copied real thread rows and copied rollout artifacts.
- The Windows validation close-out and remaining non-blocking follow-up are tracked in `docs/spec/05_open_questions_and_next_steps.md`.

## Notes

This repository documents and implements the current canonical skill behavior.

It does not aim to preserve older local skill names or compatibility shims.
