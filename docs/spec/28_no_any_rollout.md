# No-Any Rollout

## Purpose

This document records the approved staged plan for hardening the repository against `Any` in Python type checking.

It exists to separate three concerns clearly:

- the currently enforced quality gates
- the newly approved no-`Any` policy direction
- the rollout order that keeps cross-platform interruption low

## Decision Status

- Status: approved staged implementation plan
- Decision date: April 2, 2026
- Scope: Python typing policy, mypy gate rollout, and validation posture for the rollout

## External Guidance Check

- Check date: April 2, 2026
- Sources:
  - Python typing docs for `Any` and the `object` alternative
  - mypy command-line docs for the `--disallow-any-*` family and `--strict`
  - mypy dynamic-typing docs for how implicit `Any` propagates
  - Ruff `ANN401` docs for explicit-`Any` policy framing

## Current Repo State

As of April 2, 2026:

- explicit `Any` annotations or `typing.Any` imports in Python source: `0`
- stricter one-off mypy run with `--disallow-any-expr --disallow-any-explicit --disallow-any-decorated --disallow-any-generics --disallow-subclassing-any --warn-return-any`: `68` errors across `11` files
- production-code findings: `31`
- test-code findings: `37`

Current hotspots:

- `skills/export/codexporter/session_store.py`: SQLite row access remains dynamically typed
- `skills/export/codexporter/rollout_parser.py`, `renderer.py`, `compaction.py`, and `checkpoint.py`: `json.loads(...)` values remain dynamically typed until narrowed
- `skills/export/codexporter/cli.py`: `argparse` namespace attributes remain dynamically typed
- `tests/`: fixture rendering and JSON-heavy assertions amplify dynamic typing unless helper boundaries are typed explicitly

## Policy Statement

The repository should treat uncontained `Any` as a defect in typed code.

This does not mean every dynamic boundary is banned. It means:

- explicit `Any` should be disallowed
- implicit `Any` should be narrowed quickly at I/O boundaries
- business logic should operate on typed values rather than on propagated dynamic values
- unavoidable escape hatches, if any remain, should be narrow, local, and justified

Preferred replacements for `Any` in this repository are:

- `object` for unknown external values before validation
- `dict[str, object]` and `list[object]` at raw JSON boundaries
- `TypedDict` when a persisted payload shape is known and stable enough to model
- dataclasses or existing domain models after validation and normalization
- narrow `cast(...)` only at a boundary where the runtime contract is already known but mypy cannot express it directly

## Current Binding Gates

As of April 2, 2026, Stages 1 and 2 are landed in `pyproject.toml`, so the current binding automated gates are:

- `pytest`
- `mypy` in `strict` mode with `disallow_any_explicit = true`, `disallow_any_unimported = true`, and a production-only `disallow_any_expr = true` override for `codexporter`
- `ruff check`
- `ruff format --check`

This document does not claim that repo-wide no-`Any` expression enforcement is already active in tests.

## Rollout Stages

### Stage 1: Block New Explicit Any And Import-Degraded Any

Landed first gate additions:

- `disallow_any_explicit = true`
- `disallow_any_unimported = true`

Reasoning:

- `disallow_any_explicit` is a no-op in the current repo state because no explicit `Any` is present today
- `disallow_any_unimported` closes a low-noise gap where missing import analysis could silently degrade to `Any`
- neither step required meaningful runtime refactoring

Acceptance criteria:

- the maintained macOS-local baseline remains green
- no contributor can introduce explicit `Any` without mypy failing
- no new import-analysis degradation to `Any` is silently accepted

### Stage 2: Enforce No Any Expressions In Production Modules

Landed next gate:

- enable `disallow_any_expr = true` for `codexporter` production modules first

Reasoning:

- this is the highest-value no-`Any` enforcement step
- it addresses the real current leaks without forcing test cleanup and production cleanup into one disruptive batch
- runtime risk stays lower when production refactors are kept small and validated incrementally

Approved first config shape:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_configs = true
mypy_path = ["skills/export"]
disallow_any_explicit = true
disallow_any_unimported = true

[[tool.mypy.overrides]]
module = ["codexporter", "codexporter.*"]
disallow_any_expr = true
```

Implementation guidance:

- fix `json.loads(...)` call sites by narrowing to `object` and validating immediately
- extract SQLite rows into typed structures at the fetch boundary instead of indexing `sqlite3.Row` throughout the flow
- avoid letting `argparse.Namespace` attributes flow into application code without local typed variables

Acceptance criteria:

- production modules pass mypy with `disallow_any_expr = true`
- no user-visible behavior changes regress on macOS
- future shared-behavior changes trigger Linux or Windows reruns before platform docs are updated

### Stage 3: Extend No Any Expressions To Tests

Approved later gate:

- extend `disallow_any_expr = true` to `tests/` and `tests/conftest.py`

Reasoning:

- tests should eventually meet the same typing standard
- test-only fixture plumbing is the largest remaining dynamic hotspot after production cleanup
- delaying this stage keeps the first rollout focused on shipped behavior

Implementation guidance:

- replace ad hoc JSON blobs with typed helper builders where practical
- narrow fixture-rendering helpers at the parse boundary
- prefer typed assertion helpers over indexing raw decoded payloads inline

Acceptance criteria:

- tests pass under the stronger gate
- fixture helpers no longer propagate dynamic values into the rest of the test suite

### Stage 4: Re-evaluate Lower-Value Any Flags

Defer until the earlier stages are green:

- `disallow_any_decorated`

Reasoning:

- this repository is not currently decorator-heavy
- it is lower value than expression-level hardening for the current code shape

## Boundary-Specific Refactoring Strategy

### JSON Boundaries

Use this pattern:

1. decode into `object`
2. check the runtime shape
3. convert into typed structures
4. keep unchecked decoded values from leaking deeper into the module

### SQLite Boundaries

Prefer one of:

- fetch tuples and unpack them into typed local variables
- convert `sqlite3.Row` into a typed dataclass or explicit typed mapping immediately after fetch

Do not pass indexed row access deep into the flow.

### CLI Boundaries

After `parse_args(...)`:

- assign each incoming attribute into a typed local variable
- pass typed locals into the application layer

Do not let the raw namespace act as a de facto typed contract.

### Test Boundaries

Tests should still prefer readability, but not by propagating unchecked decoded values.

Prefer:

- small typed helper constructors
- typed fixture payload models when the JSON shape is stable
- narrow parse-and-validate helpers for one-off assertions

## Validation Strategy During The Rollout

- treat typing-gate changes as low runtime risk by themselves, but treat the code refactors required to satisfy them as normal shared-behavior changes
- keep the maintained macOS-local baseline as the fast inner loop
- use Linux reruns as soon as shared exporter logic is touched materially
- keep Windows validation periodic and evidence-based rather than assumed

## Linux Validation On Daniel's Mac

If Daniel runs Fedora on this Mac, that guest may be used for supplemental Linux CLI validation for this repository.

Rules:

- record the guest run as Linux evidence only after the commands were directly observed inside the Linux guest
- identify the guest architecture in the validation note when it matters
- do not treat a Linux guest rerun as a substitute for Windows validation
- do not update Linux validated-status claims unless the observed Linux guest or Linux host evidence is actually recorded

## Exit Criteria

The staged no-`Any` rollout is complete only when:

- explicit `Any` is blocked by config
- import-degraded `Any` is blocked by config
- production modules pass without `Any` expressions
- tests pass without `Any` expressions
- the updated gates are reflected truthfully in `pyproject.toml`, `README.md`, and validation notes
