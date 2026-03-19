# Codexporter Windows Test Suite Fix Proposal

Date: 2026-03-19

Audience: maintainer Codex instance

Goal: make the repo's automated validation actually work on Windows, not just the interactive runtime happy path.

## Executive Summary

The runtime exporter is now in much better shape on Windows, but the test harness still needs a Windows pass.

There are two main gaps:

1. the tests assume timezone data is always available
2. the rollout fixture templating is not JSON-safe when Windows backslash paths are substituted into templates

The highest-value next step is to fix the fixture generation path so Windows path strings are serialized into JSON correctly. Without that, the new Windows-specific regression tests cannot serve as reliable CI protection.

## Proposed Fixes

### 1. Stop using raw string replacement for JSONL rollout fixtures

Files involved:

- `tests/conftest.py`
- `tests/fixtures/session_alpha/rollout_initial.jsonl`
- `tests/fixtures/session_alpha/rollout_incremental.jsonl`

Current problem:

- `_read_template(...)` currently does plain `.replace(PLACEHOLDER, str(project_root))`
- that is unsafe for JSON when `project_root` contains Windows backslashes

Recommended fix:

- do not inject raw path strings directly into JSON fixture text
- instead, serialize substituted values with `json.dumps(...)` where the placeholder is inside JSON string content

Two reasonable implementation patterns:

#### Option A: structured fixture builder

- store the rollout fixture as structured Python records or per-line JSON objects
- render the final JSONL using `json.dumps(record, separators=(",", ":"))`

Why this is best:

- it removes string-escaping bugs entirely
- it makes future fixture edits less fragile
- it is the cleanest long-term approach

#### Option B: JSON-escaped placeholder replacement

- keep the template files
- replace placeholders with a JSON-escaped string value rather than the raw path
- use separate placeholders for JSON-string positions and plain markdown/text positions if needed

Example:

- `__PROJECT_ROOT_JSON__` for JSON string values
- `__PROJECT_ROOT_TEXT__` for expected markdown text output

Why this is acceptable:

- smaller patch
- lower churn in the fixture layout

I would still prefer Option A if you expect fixture growth.

### 2. Make test timezone setup independent of system tzdata

Files involved:

- `tests/conftest.py`
- possibly `pyproject.toml`

Current problem:

- `TIMEZONE = ZoneInfo("Europe/Vienna")` fails on Windows when the venv has no `tzdata`

Recommended fix:

Pick one of these and be explicit:

#### Option A: add `tzdata` to the dev dependency set

In `pyproject.toml`, add `tzdata` under `[project.optional-dependencies].dev`.

Pros:

- closest to current test design
- simple

Cons:

- still depends on an external timezone package just for tests

#### Option B: remove named-zone dependency from shared test fixtures

- use `datetime.timezone.utc` in `tests/conftest.py`
- keep named timezone behavior only in tests that intentionally validate timezone conversion
- monkeypatch or explicitly install `tzdata` only inside those targeted tests if needed

Pros:

- leaner and more portable
- avoids hidden Windows assumptions in the global fixture layer

Cons:

- slightly more refactoring in expected rendered timestamps

I would favor Option B for base fixtures and reserve named-zone tests for dedicated renderer-focused cases.

### 3. Add a Windows CI job or at least a documented Windows verification lane

Why:

- the repo now has Windows-specific logic and tests
- without a Windows run, future regressions can quietly return

Minimum useful coverage:

- `pytest`
- `mypy`
- `ruff check`
- `ruff format --check`

If full CI is not desired yet:

- add a documented manual Windows verification recipe
- keep a validation record current in `docs/validation/windows_app.md`

### 4. Add one or two direct tests for fixture generation itself

Right now the fixture bug is discovered only indirectly, after many tests fail.

Add tests that assert:

1. generated rollout fixture lines remain valid JSON when `project_root` is a Windows path
2. generated expected markdown still renders the intended plain-text Windows path output

That turns the current broad failure into one tight, explanatory failure.

## Missing Or Still-Needed Windows Tests

The new suite already added the most important runtime regression cases:

- current-thread selection via `CODEX_THREAD_ID`
- explicit `session_id`
- `\\?\` Windows path normalization
- UTC fallback when named timezone resolution fails

What is still missing or incomplete:

1. a test that validates the fixture-generation path itself on a Windows-style input path
2. a green Windows `pytest` run across the whole suite
3. ideally a Windows full-flow test that mimics the documented launcher choice more closely, though this is less urgent than fixing the broken fixtures

## Suggested Implementation Order

### Phase 1: unbreak Windows pytest

1. Fix fixture generation so JSONL remains valid with Windows paths.
2. Remove or explicitly satisfy the `ZoneInfo("Europe/Vienna")` dependency in `tests/conftest.py`.
3. Re-run `pytest` on Windows.

### Phase 2: harden regression coverage

1. Add direct tests for Windows-safe fixture generation.
2. Keep the existing `test_session_selection.py` and timezone-fallback tests.
3. Re-run `mypy` and `ruff` on Windows as a sanity check.

### Phase 3: automate

1. Add a Windows CI lane if practical.
2. Update `README.md` validation snapshot once Windows `pytest` is green.
3. Update `docs/spec/22_platform_validation.md` and `docs/validation/windows_app.md` to reflect a stronger validation level if earned.

## Acceptance Criteria

This work should be considered complete only when:

1. a fresh Windows venv can run `python -m pytest` without manual ad hoc fixes beyond the documented dev install flow
2. the rollout fixture generation path produces valid JSONL on Windows
3. the Windows-specific regression tests run and pass
4. `mypy`, `ruff check`, and `ruff format --check` still pass
5. the documentation no longer needs to warn that Windows `pytest` is currently broken

## Minimal Patch Recommendation

If you want the smallest effective patch:

1. add `tzdata` to `dev` dependencies or remove the named-zone dependency from `tests/conftest.py`
2. split placeholder replacement into JSON-safe and text-safe placeholders
3. add one direct test that validates Windows-path fixture rendering
4. re-run `pytest` on Windows and update the docs

That should be enough to convert the current Windows validation from "runtime happy path works, but test suite is still broken" into something that can credibly support automated Windows validation.
