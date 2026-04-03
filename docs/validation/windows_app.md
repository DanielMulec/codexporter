# Windows Codex App Validation

- Validation dates: March 18-20, March 27, April 3, and April 3, 2026 post-refactor audit
- Validation status: not currently revalidated on the current repo state
- Host OS: Windows
- Codex surface: Codex Desktop app context
- Rollout source field: `vscode`
- Codex versions observed: `0.115.0-alpha.27`, `0.112.0-alpha.3`, and `0.118.0-alpha.2`
- Models observed: `gpt-5.4`
- Approval modes observed: `never` and `on-request`
- Sandbox modes observed: `danger-full-access` and `workspace-write` without network access

## Evidence

- Verified the updated repo revision from a fresh Windows checkout at `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-review-20260319`.
- Confirmed the installed skill workflow was updated for Windows and now prefers `py -3` over plain `python` when no activated virtual environment is present.
- Ran the latest exporter from the repo checkout with `PYTHONNOUSERSITE=1` and observed first successful export creation at `codex_exports/20260318-144604-skill-installer-C-Users-DanielMulecDatenpol-codex-skills-sys-1.md`.
- Confirmed that the first successful export targeted the active thread `019cfffc-0c1c-7930-913e-e06de2b63684` rather than the earlier archived same-workspace session that had been exported incorrectly before the fix.
- Confirmed that the export artifact was written into the active project's `codex_exports/` directory rather than into the installed skill directory under `~/.codex/skills/export/`.
- Refreshed the globally installed `export` skill and observed incremental export creation through the installed skill boundary at `codex_exports/20260318-144843-skill-installer-C-Users-DanielMulecDatenpol-codex-skills-sys-2.md`.
- Observed no-new-content behavior by invoking the installed Windows skill twice inside one shell process; the first call created `codex_exports/20260319-082344-skill-installer-C-Users-DanielMulecDatenpol-codex-skills-sys-3.md` and the second call returned `There is no new content to export since the last successful export.` without creating another markdown file.
- On March 20, 2026, directly invoked `$export` in the active Windows Codex Desktop app thread for this repository and observed first export creation at `codex_exports/20260320-165437-Please-sync-the-GitHub-repo-with-the-local-repo-The-GitHub-r-1.md`.
- In the same active Windows Codex Desktop app thread, invoked `$export` again after additional visible chat content and observed incremental export creation at `codex_exports/20260320-171613-Please-sync-the-GitHub-repo-with-the-local-repo-The-GitHub-r-2.md`.
- Inspected the rendered markdown exports and matching checkpoint sidecar for session `019cfffc-0c1c-7930-913e-e06de2b63684` and confirmed the visible-chat-first structure, metadata header, tool sections, and export metadata footer.
- The successful Windows app export also covered the platform-specific current-thread targeting case that had previously failed: the live thread row persisted in `state_5.sqlite` used the Windows extended-length path spelling `\\?\C:\...`, while the invoking shell workspace used the plain drive-letter form `C:\...`; the updated exporter still targeted the active thread correctly.
- The successful repo-checkout run was performed with `PYTHONNOUSERSITE=1`, which means the Windows happy path no longer depended on the previously installed user-scoped `tzdata` package.
- On March 27, 2026, ran `.\.venv\Scripts\python.exe skills/export/scripts/export_skill.py` on Windows against isolated temporary Codex homes under `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w`, populated with copied real Windows app thread rows and copied rollout artifacts so the remaining non-happy-path cases could be forced without mutating live app state.
- The fresh Windows-host automated gate rerun on March 31, 2026 passed `.\.venv\Scripts\python.exe -m pytest`, including the explicit compact full-flow and deterministic compaction coverage that exercises `$export --compact`, large raw payload omission, short-diff retention, oversized JSON-output compaction, and shared checkpoint behavior.
- On April 3, 2026, Daniel revalidated the post-Stage-2 live Windows app happy path and confirmed that full export, full incremental export, full compact export, and compact incremental export all still worked from the current repo state across multiple invocation orders, including mixed full-to-compact and compact-to-full sequences. This reconfirmation was happy-path-only; no new failure-path or ambiguity evidence was added in that pass.
- On April 3, 2026, a deeper Windows 11 ARM audit then reran the current `main` repo entrypoint on the live app thread plus isolated copied app-style Codex homes derived from that live thread. That audit re-confirmed first export, incremental export, no-new-content behavior, ambiguity fail-closed behavior, targeted `\\?\` current-thread recovery, workspace-mismatch rejection, denied rollout access handling, German checkpoint-failure localization, unsafe installed-skill-directory rejection, and a fresh green temporary Windows `.venv` run of `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- The same April 3, 2026 audit also reproduced a new blocking app-surface issue on the current repo state: a real Windows app-style compact export still preserved bulky raw `shell_command` file-read output such as the full `pyproject.toml` body, so the compact render profile did not satisfy the deterministic omission contract on that live Windows Desktop-style surface.
- That audit also established that the globally installed skill under `C:\Users\Daniel\.codex\skills\export` was stale relative to the current repo revision, which means installed-skill manual runs on this machine can no longer be treated as evidence for the current `main` repo state until the install is refreshed.
- The same audit additionally reproduced a long-path Windows write failure on the repo entrypoint at an estimated final export-path length of about `276` characters, and observed that successful targeted recovery from a persisted `\\?\` path spelling still surfaces that raw extended-length form in the user-facing success message.
- The localized failure-path replay used copied real Windows app thread `019cdd30-b865-76f3-9612-6f801fe45575`, source `vscode`, Codex `0.112.0-alpha.3`, model `gpt-5.4`, approval `never`, sandbox `danger-full-access`, and rollout copy `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\app-language\rollouts\app-language-rollout.jsonl`.
- That localized failure-path replay first created `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\app-language\app-lang-project\codex_exports\20260327-144752-Hey-GPT-Ich-hoffe-dass-wir-auch-auf-Deutsch-hier-eine-ideale-1.md` plus sidecar `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\app-language\app-lang-project\codex_exports\019cdd30-b865-76f3-9612-6f801fe45575-checkpoint.json`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- The restricted-access and ambiguity close-out used copied real Windows app thread `019d0bd3-71ff-7823-8295-203d79cd8338`, source `vscode`, Codex `0.115.0-alpha.27`, model `gpt-5.4`, approval `on-request`, sandbox `workspace-write` without network access.
- After denying read access to `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\app-restricted\rollouts\app-restricted-rollout.jsonl`, the exporter returned the explicit persisted-session-history failure and created no export or checkpoint artifacts.
- After seeding two same-workspace `vscode` rows in the isolated `state_5.sqlite` with Windows extended-length `\\?\` workspace spelling, the untargeted run failed clearly with the ambiguous-session message, and the targeted rerun with `CODEX_THREAD_ID=019d0bd3-71ff-7823-8295-203d79cd8338` exported `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\app-ambiguity\app-ambiguous-project\codex_exports\20260327-144752-Please-sync-the-GitHub-repo-with-the-local-repo-The-GitHub-r-1.md` successfully.
- Ran automated Windows gates in the repo on the same day: `.\.venv\Scripts\python.exe -m pytest`, `.\.venv\Scripts\python.exe -m mypy skills/export tests`, `.\.venv\Scripts\python.exe -m ruff check .`, and `.\.venv\Scripts\python.exe -m ruff format --check .`.

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
- compact export behavior: fail

## Notes

- This file preserves the historical March 18-27 Windows app evidence, but the April 3, 2026 post-refactor audit re-opened Windows app validation on the current repo state because compact-mode behavior failed on a real Windows app-style session.
- The March 27 close-out intentionally used isolated temporary Codex state derived from real Windows app persisted-session data because those failure-path conditions had not reproduced reliably in ordinary live use.
- The April 3 happy-path reconfirmation was still useful evidence, but it did not add new failure-path, no-new-content, or ambiguity evidence, so the March 27 controlled close-out remains the authoritative close-out for those checklist items.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- The compact checklist item is not currently closed for the current repo state because the reproduced Windows app-style `shell_command` compact export still leaked bulky raw file-read output instead of replacing it with the approved deterministic omission marker.
- The stale installed-skill finding means future Windows app installed-skill checks on this machine must prove install parity with the repo before they count as validation evidence for the current revision.
- See `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md` for the full April 3, 2026 audit and its relationship to the separate March 28 session-discovery proposal.
