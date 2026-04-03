 # Windows Post-Refactor Validation Bug Report

Date: 2026-04-03

Audience: Daniel and maintainer Codex instance

Scope: record the April 3, 2026 Windows 11 ARM validation audit of the current `main` repo state after the no-`Any` refactor, compare it to the March 28 session-discovery proposal, and document why Windows should not yet be treated as fully revalidated on the current repo revision.

Check date for upstream docs that affect this report: 2026-04-03.

## Executive Summary

The current repository state passed the Windows automated gates on this host and still succeeds on the ordinary happy path, but the Windows post-refactor validation close-out is not clean.

Two blocking findings were reproduced:

1. real compact exports from a Windows Codex Desktop-style session still preserve bulky raw `shell_command` file-read output, so the implemented compact profile does not satisfy the compact-mode contract on that live Windows surface
2. the globally installed Windows skill under `C:\Users\Daniel\.codex\skills\export` is not the same revision as the current repository, so installed-skill manual runs cannot be treated as validation evidence for the current `main` repo state without first refreshing the install

Two secondary findings were also reproduced:

1. a long but already-existing Windows project path failed during export writing on this host once the final export path reached about `276` characters
2. when current-thread recovery succeeds against a persisted `\\?\` Windows path spelling, the success message surfaces that raw extended-length path directly to the user

This means:

- the historical Windows validation baseline still matters
- the March 28 session-discovery proposal is still relevant
- but Windows should not yet be marked fully revalidated for the current post-refactor repo state

## Relationship To The March 28 Proposal

This report does not replace [codexporter-session-discovery-fix-proposal-2026-03-28.md](./codexporter-session-discovery-fix-proposal-2026-03-28.md).

That proposal investigated a different primary incident:

- live rollout exists
- current session id exists
- `state_5.sqlite.threads` is missing the current row
- exporter fails because SQLite is still treated as the only current-session authority

### What aligned with that proposal

- The April 3 audit reconfirmed the same fail-safe design expectations that the proposal argues for:
  - explicit thread targeting must override same-workspace heuristics
  - ambiguity must fail closed
  - workspace mismatch must fail closed
  - Windows `\\?\` path spelling differences must not cause the exporter to select the wrong session
- The proposal's warning that SQLite is a brittle discovery dependency still stands. Nothing in the April 3 audit disproved that architectural concern.

### What did not align

- The exact stale-SQLite or missing-thread-row condition from March 28 was not reproduced in this audit.
- On this machine and in this session, the current thread row was present in `state_5.sqlite`, and current-session discovery succeeded.

### What is new in this report

- A real Windows compact-mode regression on Codex Desktop-style `shell_command` traffic
- Proof that the installed global skill is stale relative to the current repo revision
- A real long-path Windows write failure on the current repo entrypoint
- A user-facing Windows path-normalization rough edge in the success message after `\\?\` recovery

Practical summary:

- the March 28 proposal remains partly unimplemented and still relevant
- the main blockers found on April 3 are mostly new and independent of that older discovery incident

## Audit Environment

- Host OS: Windows 11 on ARM
- Repo revision audited: `299fb6a3cb4da1920c368548fa5cbc92e9ae5c99`
- Repo branch state during audit: `main`, equal to `origin/main`
- Live current thread at audit start: `019d54ef-180a-7b02-9176-1f6677029a97`
- Live source surface for the reproduced compact regression: Codex Desktop app-style rollout source `vscode`
- Live Codex metadata observed for that thread:
  - `cli_version = 0.118.0-alpha.2`
  - `approval_mode = never`
  - `sandbox_policy = {"type":"danger-full-access"}`

## Evidence Collected

### Fresh Windows quality gates on this host

Using a fresh temporary virtual environment under `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-validate-20260403-221651`:

- `py -3 -m venv .venv`
- `python -m pip install -e "C:\projekte\codexporter[dev]"`
- `python -m pytest` passed with `39` tests
- `python -m mypy skills/export tests` passed
- `python -m ruff check .` passed
- `python -m ruff format --check .` passed

### Live repo-entrypoint happy path on the current Windows app thread

From `C:\projekte\codexporter`, running:

- `py -3 skills/export/scripts/export_skill.py --project-root . --codex-home %USERPROFILE%\.codex`

created:

- `C:\projekte\codexporter\codex_exports\20260403-221918-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-1.md`

and the matching sidecar:

- `C:\projekte\codexporter\codex_exports\019d54ef-180a-7b02-9176-1f6677029a97-checkpoint.json`

The exported markdown bytes were inspected directly and contained correct Unicode punctuation; the temporary mojibake seen in shell output was a display-layer issue, not a persisted export bug.

### Controlled copied-state Windows replays

Using isolated temporary Codex homes under:

- `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-audit-cw5tjb4v`

the current live Windows app thread row and rollout history were copied and replayed to force conditions that are hard to reproduce on demand in normal use.

Reproduced successfully:

- first export
- incremental export
- explicit no-new-content behavior
- compact incremental export sharing the same checkpoint history
- same-workspace ambiguity fail-closed behavior
- targeted current-thread recovery with persisted `\\?\` workspace spelling
- explicit workspace-mismatch fail-closed behavior
- persisted-session-history access denial behavior
- German localized checkpoint-failure messaging
- unsafe installed-skill-directory project-root rejection

### Real compact-mode failure on the current repo entrypoint

Against copied Windows app-style rollout data derived from the current live thread, running:

- `py -3 C:\projekte\codexporter\skills\export\scripts\export_skill.py --codex-home <copied-home> --compact`

created:

- `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-audit-cw5tjb4v\compact_shell_repo\project\codex_exports\20260403-224302-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-1.md`

That compact export still contained raw file-read output such as the full `pyproject.toml` body beginning with:

- `[build-system]`

inside a `Tool Output · shell_command` block.

This means the export preserved bulky raw file-read content instead of replacing it with the required deterministic compact omission marker.

## Findings

### P1: Compact mode misses real Windows Desktop `shell_command` file reads

The current compaction logic only parses `exec_command` payloads when deciding whether an output is a file read, a listing, or another compactable command shape.

Relevant implementation points:

- [skills/export/codexporter/compaction.py](./skills/export/codexporter/compaction.py)

Observed consequence:

- compact exports from a real Windows Codex Desktop-style session still include bulky raw file contents when those contents came from `shell_command` instead of `exec_command`

Why this is blocking:

- the compact-mode contract says compact export must deterministically omit bulky raw file-read bodies when they qualify
- the current Windows app-style live surface violates that requirement

### P1: Installed global skill is stale relative to the repo

The installed global skill under:

- `C:\Users\Daniel\.codex\skills\export`

is not byte-identical to the current repo.

Concrete evidence:

- installed `codexporter.__version__ = "1.1.3"`
- repo `codexporter.__version__ = "1.1.5"`
- installed `rollout_parser.py` is also materially older than the repo version

Why this is blocking:

- installed-skill manual testing on this machine no longer proves behavior of the current repo revision
- any Windows validation that relies on the installed skill must first refresh that install or explicitly prove parity

### P2: Long Windows paths still fail on this host

Using a pre-created Windows project path under `C:\t\...` whose estimated final export path was about `276` characters, the repo entrypoint failed with:

- `I couldn't write the export artifacts safely into ...\codex_exports.`

Why this matters:

- it is a real Windows runtime failure on this host
- it affects the current repo entrypoint, not just the installed skill
- the current validation stack does not cover this path-length seam

This report does not infer more than the observed result. The likely cause is a normal Win32 path-length limitation interacting with the temp-file naming strategy, but the important fact here is the reproduced exporter failure.

### P3: Success messaging exposes raw `\\?\` paths

In the ambiguity-recovery replay, the targeted rerun succeeded but reported a path beginning with:

- `\\?\C:\...`

This did not break targeting correctness, but it is still a user-facing rough edge because the success message surfaces a machine-oriented Windows path spelling instead of the normal drive-letter form.

## Current Validation Disposition

### Windows app

Do not treat Windows Codex Desktop app as fully revalidated on the current post-refactor repo state.

Reason:

- the compact checklist item is currently failed on the real Windows Desktop-style surface because bulky raw `shell_command` file reads still leak into compact exports

### Windows CLI

Keep the historical Windows CLI validation baseline recorded, but do not use it as proof that current Windows-wide post-refactor sign-off is closed.

Reason:

- this audit did not freshly rerun the live Codex CLI surface itself
- installed-skill evidence on this machine is currently ambiguous because the install is stale relative to the repo
- the long-path write failure is a Windows runtime risk on the current repo entrypoint even though it sits partly outside the existing checklist wording

## Recommended Next Steps

1. Fix compact-mode detection so the canonical compact profile understands Windows Desktop-style `shell_command` file reads and listings, not just `exec_command`.
2. Add automated regression coverage that models the real Windows Desktop-style tool names and payloads from this audit.
3. Refresh the globally installed Windows skill before counting any installed-skill manual run as validation evidence for the current repo revision.
4. Decide whether long Windows paths are part of the supported canonical path envelope. If yes, close the write failure. If no, document the explicit boundary and recovery path.
5. Normalize success-message file paths before display so `\\?\` path spellings do not leak into user-facing output.
6. Keep the March 28 session-discovery proposal open as a separate track until the stale-SQLite/live-rollout case is either implemented or explicitly rejected with rationale.

## Acceptance Criteria For Closing This Report

This report should be considered resolved only when:

1. Windows app-style `$export --compact` runs no longer leak bulky raw `shell_command` file-read bodies into compact exports
2. installed-skill validation on Windows is tied to the current repo revision rather than to a stale older install
3. the long-path Windows write behavior is either fixed or documented as an intentional unsupported boundary
4. the validation docs no longer claim Windows is fully revalidated while these findings remain open
5. the repository explicitly records how this report relates to the still-open March 28 session-discovery proposal

## Sources

Official sources checked on 2026-04-03:

- OpenAI Codex CLI setup: `https://developers.openai.com/codex/cli/#cli-setup`
- OpenAI Codex quickstart setup: `https://developers.openai.com/codex/quickstart/#setup`
- OpenAI Codex app announcement: `https://openai.com/index/introducing-the-codex-app/`
- Microsoft Windows maximum path length guidance: `https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation`

Local evidence checked on 2026-04-03:

- `C:\projekte\codexporter`
- `C:\Users\Daniel\.codex\state_5.sqlite`
- `C:\Users\Daniel\.codex\sessions\2026\04\03\rollout-2026-04-03T22-00-48-019d54ef-180a-7b02-9176-1f6677029a97.jsonl`
- `C:\Users\Daniel\.codex\skills\export`
- copied validation homes under `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-audit-cw5tjb4v`
