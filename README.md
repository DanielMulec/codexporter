# Codex Exporter

Codex Exporter is a Codex skill that exports the current live session to markdown.

The user-facing skill name is `export`, so the intended invocations are `$export` and
`$export --compact`.

## Current State

- Installable skill boundary: `skills/export/`
- User commands: `$export`, `$export --compact`
- Internal Python package: `codexporter`
- Primary artifact: one markdown file per successful export
- Output location: `codex_exports/` under the active project root
- Incremental behavior: later exports only include new session content and advance a JSON sidecar checkpoint
- Compact behavior: `--compact` keeps chronology but deterministically omits bulky raw tool payloads
- Failure behavior: fail clearly instead of guessing or writing into the installed skill directory

## What The Skill Exports

The v1 export stays close to what the user visibly experienced in Codex:

- visible user messages
- visible assistant replies
- visible commentary or progress updates
- visible tool calls and tool outputs
- compact session metadata

The exporter does not include hidden reasoning or raw internal instruction payloads.

The implemented compact profile is additive:

- plain `$export` keeps the current full-fidelity default
- `$export --compact` keeps the same session chronology and checkpoint model while omitting bulky raw tool payloads such as full file-read bodies, raw `apply_patch` bodies, large raw diffs, and oversized low-signal tool output

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

When `$export --compact` runs successfully, it writes the same kind of markdown artifact and sidecar, but the markdown uses the compact render profile and records that in the export metadata.

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

Stages 1 through 3 of the staged no-`Any` hardening plan are now landed in `pyproject.toml`, so the `mypy` command above already blocks explicit `Any`, import-degraded `Any`, and `Any` expressions across the repository. The remaining `Any` discussion in `docs/spec/28_no_any_rollout.md` is now about whether lower-value extra flags are worth adopting later.

Run the exporter directly from the repo during development:

```bash
python skills/export/scripts/export_skill.py \
  --project-root "$PWD" \
  --codex-home "${CODEX_HOME:-$HOME/.codex}"

python skills/export/scripts/export_skill.py \
  --project-root "$PWD" \
  --codex-home "${CODEX_HOME:-$HOME/.codex}" \
  --compact
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

Stages 1 through 3 of the staged no-`Any` hardening plan are now landed in `pyproject.toml`, so the `mypy` command above already blocks explicit `Any`, import-degraded `Any`, and `Any` expressions across the repository. The remaining `Any` discussion in `docs/spec/28_no_any_rollout.md` is now about whether lower-value extra flags are worth adopting later.

Run the exporter directly from the repo during development:

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }

python skills/export/scripts/export_skill.py `
  --project-root $PWD `
  --codex-home $codexHome

python skills/export/scripts/export_skill.py `
  --project-root $PWD `
  --codex-home $codexHome `
  --compact
```

When invoking the installed global skill on Windows without an activated virtual environment, prefer `py -3` over plain `python`. On some Windows setups, `python` resolves to the Microsoft Store stub instead of a working interpreter.

### Notes

- Prefer `python -m ...` after activating the virtual environment. This avoids platform-specific `.venv/bin/...` and `.venv\\Scripts\\...` command paths.
- Validation evidence in `docs/validation/` may contain machine-specific example paths. Those are recorded observations, not required contributor paths.
- The supported development baseline is Python 3.12 or newer.

## Validation Snapshot

Current automated baseline:

- 42 passing `pytest` cases on the maintained macOS-local baseline across unit behavior, service flow, public invocation flow, degraded mode, checkpoint edge cases, thread-accurate session targeting, Windows-style path-shape equivalence, Windows-safe fixture rendering, localized CLI failure and omission messaging, explicit hidden-reasoning and internal-instruction exclusion, optional-metadata omission, timezone-fallback behavior, compact CLI invocation, deterministic bulky-payload compaction including oversized JSON-output suppression, compact/profile checkpoint-sharing behavior, malformed-rollout timestamp handling, tool-output instruction-payload omission, boolean checkpoint-field rejection, and `shell_command` compaction coverage for JSON-backed, plain-string, and sanitized app-style rollout payloads
- On March 27, 2026, fresh Linux and Windows `.venv` reruns also passed `pytest`, `mypy`, `ruff check`, and `ruff format --check`
- On April 3, 2026, a fresh Linux `.venv` rerun on Python `3.14.3` again passed `./.venv/bin/python -m pytest`, `./.venv/bin/python -m mypy skills/export tests`, `./.venv/bin/python -m ruff check .`, and `./.venv/bin/python -m ruff format --check .`
- On April 5, 2026, the current Linux `.venv` on Python `3.14.3` again passed `./.venv/bin/python -m pytest`, `./.venv/bin/python -m mypy skills/export tests`, `./.venv/bin/python -m ruff check .`, and `./.venv/bin/python -m ruff format --check .`
- `mypy` in `strict` mode
- `ruff check`
- `ruff format --check`

Current manual validation status:

- macOS Codex app: validated
- macOS Codex CLI: validated
- Linux Codex CLI: validated
- Windows Codex CLI: historical validated baseline retained, but broader Windows post-refactor sign-off is still open
- Windows Codex app: not currently revalidated on the current repo state

Latest post-refactor reconfirmation:

- On April 2-3, 2026, Daniel reran live macOS happy-path checks after the Stage 2 no-`Any` refactor and confirmed the broader manual matrix on both app and CLI: full export, full incremental export, full compact export, and compact incremental export all succeeded from the current repo state across multiple invocation orders. The retained local transcripts document example slices of that retest rather than its full breadth.
- On April 5, 2026, the current macOS app surface was revalidated again on the current repo state: the installed `~/.codex/skills/export/` skill matched the repo on disk, a live compact export on the active Desktop thread succeeded, and isolated app-style replays re-confirmed `shell_command` compact behavior, no-new-content handling, compact/full checkpoint sharing, German checkpoint-failure localization, same-workspace ambiguity fail-closed behavior plus targeted recovery, restricted-rollout honesty, workspace-mismatch rejection, and unsafe installed-skill-directory rejection.
- On April 3, 2026, a fresh Linux-host post-refactor rerun refreshed more than the earlier happy-path note: it recreated `.venv`, reran all four binding gates cleanly, then captured live current-thread full export, live ambiguity fail-closed behavior, live compact incremental export, compact-first/full-second shared-checkpoint replay, explicit no-new-content behavior, German checkpoint-failure localization, denied rollout access, explicit workspace-mismatch failure, and unsafe-project-root rejection from isolated temporary Codex homes derived from the current live Linux CLI thread.
- On April 3, 2026, Daniel also reran live Windows happy-path checks after the same refactor and confirmed the same broader manual matrix on both app and CLI: full export, full incremental export, full compact export, and compact incremental export all still worked from the current repo state across multiple invocation orders.
- The macOS and Windows notes above still describe happy-path-only reconfirmations; the Linux rerun now also refreshes direct failure-path coverage on the current repo state.
- On April 5, 2026, a second Linux-host validation rerun then checked the installed-skill path directly on the current repo revision: the installed skill matched the repo copy, a live installed-skill run created `/home/dmulec/projekte/codexporter/codex_exports/20260405-141623-Hi-GPT-1.md`, a live installed-skill `--compact` rerun created compact incremental export `/home/dmulec/projekte/codexporter/codex_exports/20260405-141637-Hi-GPT-2.md`, and copied-state temp homes under `/tmp/codexporter-linux-manual-validate-gee_dyuf` re-confirmed compact-first/full-second checkpoint sharing, explicit no-new-content behavior, denied rollout access, ambiguity fail-closed behavior, targeted recovery, workspace-mismatch rejection, German checkpoint-failure localization, and unsafe installed-skill-directory rejection without mutating live `~/.codex` state.
- That same April 5 Linux-host validation also replayed a sanitized Windows app-style `shell_command` compact export under `/tmp/codexporter-linux-manual-validate-gee_dyuf/shell_command`; the resulting `Tool Output · shell_command` block used `Raw file contents omitted in compact mode.` and did not leak the raw `pyproject.toml` body, which confirms the shared compaction fix outside the automated suite as well.
- The April 5 macOS app rerun also surfaced one lower-priority path-alias seam during the isolated replay harness: `/var/...` and `/private/var/...` were not treated as equivalent during same-workspace session matching until the disposable validation homes were normalized to the same resolved path spelling. That seam is explicitly deferred behind higher-priority Windows follow-up and does not overturn the current macOS app validation baseline.
- On April 3, 2026, a deeper Windows 11 ARM audit then reran the current repo in a fresh temporary `.venv`, replayed copied Windows Codex homes derived from the live app thread, and re-confirmed Windows ambiguity fail-closed behavior, targeted `\\?\` recovery, workspace-mismatch rejection, denied rollout access handling, German checkpoint-failure localization, and unsafe installed-skill-directory rejection. That same audit also found three current blockers for broader Windows post-refactor sign-off on this machine: real app-style compact exports still leak bulky raw `shell_command` file-read output, the installed global skill is stale relative to the repo, and a long-path Windows project root still fails during export writing on the repo entrypoint. See `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md`.

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
- The current Windows validation blockers and follow-up are tracked in `docs/spec/05_open_questions_and_next_steps.md` and `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md`.

## Notes

This repository documents and implements the current canonical skill behavior.

It does not aim to preserve older local skill names or compatibility shims.
