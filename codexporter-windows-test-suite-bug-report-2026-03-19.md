# Codexporter Windows Test Suite Bug Report

Date: 2026-03-19

Scope: Windows validation of the updated `codexporter` repo after the runtime happy-path fix landed.

## Executive Summary

The Windows runtime happy path now works, but the automated test suite is still not Windows-clean.

Observed on a fresh Windows repo checkout:

1. `mypy` passes.
2. `ruff check` passes.
3. `ruff format --check` passes.
4. `pytest` fails on Windows for two distinct reasons:
   - the test harness assumes timezone data is available in the virtual environment
   - the JSONL fixture templating is not Windows-safe because it injects raw backslash paths into JSON strings without escaping them

This means the repository now has some important Windows-specific regression tests, but the suite itself cannot yet serve as reliable Windows CI evidence.

## Environment

- Host OS: Windows
- Shell: PowerShell
- Validation date: 2026-03-19
- Python: `3.13.7`
- Repo checkout:
  `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-review-20260319`
- Validation venv:
  `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-review-20260319\.venv`

## What Was Run

Inside a fresh Windows virtual environment:

1. `python -m pip install -e ".[dev]"`
2. `python -m pytest`
3. `python -m mypy skills/export tests`
4. `python -m ruff check .`
5. `python -m ruff format --check .`

## Observed Results

### Static quality gates

These all passed on Windows:

- `mypy`
- `ruff check`
- `ruff format --check`

### Pytest failure 1: timezone data assumption in test harness

On the first Windows run, `pytest` failed before collection because:

- `tests/conftest.py` constructs `ZoneInfo("Europe/Vienna")`
- the Windows virtual environment did not have `tzdata`

Observed failure shape:

`zoneinfo._common.ZoneInfoNotFoundError: 'No time zone found with key Europe/Vienna'`

The failing line is in `tests/conftest.py`:

`TIMEZONE = ZoneInfo("Europe/Vienna")`

This is a test-harness problem, not a runtime exporter problem. The runtime exporter itself was already fixed to fall back to built-in UTC without requiring tzdata.

### Pytest failure 2: invalid JSON fixture generation on Windows

After installing `tzdata` into the Windows virtual environment, `pytest` collected 23 tests but still failed broadly.

Observed summary:

- 13 failed
- 10 passed

The common failure cause was:

`json.decoder.JSONDecodeError: Invalid \escape`

The error originates when `skills/export/codexporter/rollout_parser.py` does:

`record = json.loads(line)`

The test rollout file itself had become invalid JSON on Windows.

## Root Cause Of The JSON Fixture Failure

The fixture system uses raw text substitution of `__PROJECT_ROOT__` into JSONL templates.

Relevant files:

- `tests/conftest.py`
- `tests/fixtures/session_alpha/rollout_initial.jsonl`
- `tests/fixtures/session_alpha/rollout_incremental.jsonl`

Current behavior in `tests/conftest.py`:

- `_read_template(...)` does `replace(PLACEHOLDER, str(project_root))`
- `project_root` on Windows contains backslashes, for example:
  `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\...`
- that replacement is inserted directly into JSON strings inside the rollout fixture templates

Example template fragments:

- `"cwd":"__PROJECT_ROOT__"`
- `"cwd":"__PROJECT_ROOT__"` inside `turn_context`
- `"arguments":"{\"cmd\":\"rg --files\",\"workdir\":\"__PROJECT_ROOT__\"}"`

After naive string replacement on Windows, those become invalid JSON because the backslashes are not escaped.

That is why `json.loads(...)` later fails with `Invalid \escape`.

## Why This Matters

The repo now contains important Windows-specific tests, especially:

- `tests/test_session_selection.py`
  - covers `CODEX_THREAD_ID`
  - covers explicit `session_id`
  - covers the `\\?\` Windows path spelling case
- `tests/test_unit_contracts.py`
  - covers timezone fallback when named timezone resolution fails

But because the fixture layer is still Windows-hostile, Windows CI or local Windows contributors cannot currently rely on `pytest` to validate the repo.

That weakens the claim that Windows support is validated, even though the interactive runtime happy path has been fixed.

## Affected Tests

The failing pytest run showed breakage in multiple areas, including:

- `tests/test_checkpoint_edges.py`
- `tests/test_degraded_mode.py`
- `tests/test_exporter.py`
- `tests/test_full_flow.py`
- `tests/test_session_selection.py`

These failures were not caused by those features being broken individually. They were mostly downstream of the invalid JSON fixture content generated on Windows.

## Expected Behavior

On Windows, after creating the venv and installing dev dependencies:

1. `pytest` should collect and run without requiring extra undocumented dependency fixes.
2. The fixture generation path should produce valid JSONL rollout files on Windows.
3. The Windows-specific session-selection tests should run as ordinary regression tests, not be blocked by fixture serialization issues.

## Actual Behavior

1. `pytest` initially failed because `tzdata` was not present in the Windows venv.
2. After adding `tzdata`, `pytest` still failed because the rollout fixture templating emitted invalid JSON on Windows.

## Recommendation

Treat this as a separate test-infrastructure bug, not as proof that the runtime exporter fix is incomplete.

The runtime app behavior on Windows is now working. The remaining work is to make the test harness and fixture generation truly cross-platform so Windows validation can be automated and trusted.
