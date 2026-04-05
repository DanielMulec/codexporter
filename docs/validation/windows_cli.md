# Windows Codex CLI Validation

- Validation dates: March 20, March 27, April 3, and April 5, 2026
- Validation status: validated on the current repo state, with residual Windows runtime caveats outside the core checklist
- Host OS: Windows
- Codex surface: Codex CLI
- Codex versions observed: March 20 live happy-path metadata not retained, March 27 controlled close-out on `0.116.0`, April 5 live rerun on `0.118.0`
- Models observed: `gpt-5.4`
- Approval modes observed: March 20 live run not retained, March 27 controlled close-out observed `never`, April 5 live and copied-state reruns observed `never`
- Sandbox modes observed: March 20 live run not retained, March 27 controlled close-out observed `danger-full-access`, April 5 live and copied-state reruns observed `danger-full-access`

## Evidence

- Daniel directly validated the skill happy path in Windows Codex CLI on March 20, 2026.
- Daniel reported on March 22, 2026 that he had already installed this skill successfully through `skill-installer` on his Windows device and used the resulting globally installed `export` skill in real use; the exact installer transcript and installed path were not retained in the repository notes.
- The March 20 live run covered first export, default destination, success message with path, and repeated incremental behavior, but the exact runtime metadata and artifact names were not preserved then.
- On March 27, 2026, ran `.\.venv\Scripts\python.exe skills/export/scripts/export_skill.py` on Windows against isolated temporary Codex homes under `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w`, populated with copied real Windows CLI thread rows and copied rollout artifacts so the remaining Windows-only failure-path and ambiguity cases could be forced without mutating live `C:\Users\DanielMulecDatenpol\.codex` state.
- The fresh Windows-host automated gate rerun on March 31, 2026 passed `.\.venv\Scripts\python.exe -m pytest`, including the explicit compact full-flow and deterministic compaction coverage that exercises `$export --compact`, large raw payload omission, short-diff retention, oversized JSON-output compaction, and shared checkpoint behavior.
- On April 3, 2026, Daniel revalidated the post-Stage-2 live Windows CLI happy path and confirmed that full export, full incremental export, full compact export, and compact incremental export all still worked from the current repo state across multiple invocation orders, including mixed full-to-compact and compact-to-full sequences. This reconfirmation was happy-path-only; no new failure-path or ambiguity evidence was added in that pass.
- On April 3, 2026, the same Windows 11 ARM audit that re-opened Windows app sign-off also reran the current repo in a fresh temporary Windows `.venv`, which again passed `pytest`, `mypy`, `ruff check`, and `ruff format --check`, and used copied Windows Codex homes derived from the current live app thread to reconfirm ambiguity fail-closed behavior, targeted `\\?\` path recovery, workspace-mismatch rejection, denied rollout access handling, German checkpoint-failure localization, and unsafe installed-skill-directory rejection on the current repo entrypoint.
- On April 5, 2026, verified that the installed skill under `C:\Users\Daniel\.codex\skills\export` matched the repo content after normalizing line endings; the only remaining deltas were generated cache and editable-install metadata, so installed-skill runs on this machine are again valid evidence for the current repo state.
- On April 5, 2026, reran the active Windows Codex CLI thread directly through the installed skill on live thread `019d5e4b-2ed0-7423-83e8-c2341bc8d751`, source `cli`, Codex `0.118.0`, model `gpt-5.4`, approval `never`, and sandbox `danger-full-access`; the first live export created `codex_exports/20260405-174344-Is-this-chat-thread-source-cli-1.md`.
- A second April 5, 2026 live installed-skill run on that same Windows CLI thread created incremental export `codex_exports/20260405-174411-Is-this-chat-thread-source-cli-2.md`.
- A third April 5, 2026 live installed-skill run with `--compact` created compact incremental export `codex_exports/20260405-183700-Is-this-chat-thread-source-cli-3.md`, and the shared sidecar `codex_exports/019d5e4b-2ed0-7423-83e8-c2341bc8d751-checkpoint.json` advanced to export sequence `3` while preserving one canonical history.
- The first live export and the compact incremental export were inspected directly and confirmed the visible-chat-first markdown structure plus compact render metadata on the current repo state.
- On April 5, 2026, reran the current installed skill against isolated temporary Codex homes under `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7`, populated with the active real Windows CLI thread row and copied rollout history so the remaining checklist and failure-path conditions could be forced without mutating live `C:\Users\Daniel\.codex` state.
- In `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\sequence`, a compact-first run created `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\sequence\project\codex_exports\20260405-183426-Is-this-chat-thread-source-cli-1.md`; after appending one synthetic visible follow-up turn to the copied rollout, a full rerun created incremental export `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\sequence\project\codex_exports\20260405-183427-Is-this-chat-thread-source-cli-2.md`, and a third rerun with no further rollout change returned `There is no new content to export since the last successful export.` without creating a `-3` artifact.
- That same `sequence` replay kept one shared checkpoint sidecar at `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\sequence\project\codex_exports\019d5e4b-2ed0-7423-83e8-c2341bc8d751-checkpoint.json`, whose `export_sequence` advanced to `2` and whose `exported_artifacts` list preserved the raw `\\?\` path spelling from the copied CLI-style thread row.
- In `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\restricted_fresh`, denying read access to the copied rollout with `icacls` made the exporter return the explicit persisted-session-history failure for `rollout-restricted-fresh.jsonl`, and no `codex_exports` directory was created.
- In `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\ambiguous`, seeding two same-workspace CLI rows in the isolated `state_5.sqlite` reproduced the untargeted ambiguous-session failure once `CODEX_THREAD_ID` was removed from the shell environment; the targeted rerun with `--session-id 019d5e4b-2ed0-7423-83e8-c2341bc8d751` then exported `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\ambiguous\project\codex_exports\20260405-183502-Is-this-chat-thread-source-cli-1.md` successfully.
- In `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\mismatch`, explicitly targeting session `win-cli-mismatch-20260405` from `...\mismatch\project` failed clearly because the copied thread row belonged to `...\mismatch\other-project`.
- In `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\german`, a German copied rollout first created `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\german\project\codex_exports\20260405-183502-Deutscher-Validierungsverlauf-1.md`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- Running the installed production entrypoint on April 5, 2026 with `--project-root C:\Users\Daniel\.codex\skills\export` failed with the unsafe-project-root message, confirming that the installed skill directory is still rejected as an export destination on Windows CLI.
- Also on April 5, 2026, a sanitized copied-state Windows CLI `shell_command` replay under `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\shell_command` created compact export `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7\shell_command\project\codex_exports\20260405-183655-Windows-shell-compact-replay-1.md`, whose `Tool Output · shell_command` block used `Raw file contents omitted in compact mode.`, listed `pyproject.toml`, and did not leak the raw `[build-system]` file body.
- On April 5, 2026, a fresh temporary Windows virtual environment under `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-validate-20260405-1838` passed `python -m pip install -e ".[dev]"`, `python -m pytest` with `42` tests, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .` from the current repo state.
- One Windows path-length nuance changed materially on this rerun. In `...\long_path`, a copied CLI-style thread row whose persisted cwd used the Windows extended-length `\\?\` spelling succeeded and created `...\long_path\...\project\codex_exports\20260405-183502-Is-this-chat-thread-source-cli-1.md` at project-root length `221` while `LongPathsEnabled` remained `0`.
- A parallel plain-path control under `...\long_plain` with project-root length `222` still failed with `I couldn't write the export artifacts safely into ...\codex_exports.`, so the plain-path Windows path-length envelope remains open even though the copied current CLI-style `\\?\` row now succeeds on this host.

## Checklist Results

- first export: pass
- default export destination: pass
- success message with file location: pass
- incremental export: pass
- no-new-content behavior: pass
- filename sequencing: pass
- markdown rendering: pass
- language-sensitive failure messaging: pass
- restricted-environment honesty: pass
- current-thread targeting under shared-workspace ambiguity or path variation: pass
- compact export behavior: pass

## Notes

- The March 27 close-out intentionally used isolated temporary Codex state derived from real Windows CLI persisted-session records because the missing failure-path and ambiguity cases had not reproduced on demand in normal live use.
- The April 3 happy-path reconfirmation was still useful evidence, but it did not add new failure-path, no-new-content, or ambiguity evidence, so the March 27 controlled close-out remained the authoritative failure-path record until the fresh April 5 Windows CLI rerun.
- The April 5 rerun closes the earlier gap in this file: Windows Codex CLI is now revalidated directly on the current repo state rather than relying on a retained historical baseline plus cross-cutting Windows evidence from another surface.
- The current live Windows CLI surface still exposes raw `\\?\` path spellings in success messages and checkpoint artifact lists whenever the persisted thread row uses the Windows extended-length cwd form. That is now the main user-facing rough edge still observed directly on the validated CLI path.
- Windows path-length behavior is now more precise than the earlier April 3 note implied. On this host with `LongPathsEnabled = 0`, the current CLI-style copied row with extended-length `\\?\` cwd succeeded at project-root length `221`, while an otherwise parallel plain-path control still failed at length `222`. The supported plain-path envelope therefore remains open even though the active Windows CLI path is now validated on the current repo state.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- The compact checklist item is now backed by Daniel's April 3, 2026 live Windows CLI happy-path retest across full and compact export orders, the April 5, 2026 live installed-skill compact incremental rerun on the active CLI thread, the April 5 compact-first/full-second copied-state sequence replay, the April 5 copied CLI `shell_command` compact replay, and the fresh Windows-host automated full-flow and compaction tests.
- See `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md` for the historical April 3 audit findings and for the comparison with the separate March 28 session-discovery proposal.
