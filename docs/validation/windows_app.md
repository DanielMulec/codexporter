# Windows Codex App Validation

- Validation dates: March 18-20, 2026
- Validation status: partial
- Host OS: Windows
- Codex surface: Codex Desktop app context
- Rollout source field: `vscode`
- Codex version: `0.115.0-alpha.27`
- Model: `gpt-5.4`
- Sandbox mode: `danger-full-access`
- Approval mode: `never`

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
- Ran automated Windows quality gates in the repo checkout on March 19, 2026:
  - `.venv\Scripts\python.exe -m mypy skills/export tests`
  - `.venv\Scripts\python.exe -m ruff check .`
  - `.venv\Scripts\python.exe -m ruff format --check .`
- Also ran `.venv\Scripts\python.exe -m pytest` on Windows. That run is important validation evidence even though it is not yet green:
  - the suite first failed before collection because `tests/conftest.py` constructs `ZoneInfo("Europe/Vienna")` and the Windows virtual environment did not have `tzdata`
  - after installing `tzdata` into the Windows virtual environment, `pytest` collected 23 tests but still failed because the current fixture/template layer injects raw Windows paths into JSONL fixture content without escaping backslashes, causing `json.decoder.JSONDecodeError: Invalid \escape`

## Checklist Results

- first export: pass
- default export destination: pass
- success message with file location: pass
- incremental export: pass
- no-new-content behavior: pass
- filename sequencing: pass
- markdown rendering: pass
- language-sensitive failure messaging: partial
- restricted-environment honesty: not run
- current-thread targeting under shared-workspace ambiguity or path variation: pass

## Notes

- This record covers Windows Codex Desktop app behavior for the current happy path and for the specific current-thread/path-variation case that previously broke the skill on Windows.
- The March 20, 2026 rerun confirmed the same-thread installed-skill happy path again in the live Windows Codex Desktop app conversation for this repository, including a direct first export followed by a direct incremental export.
- English success and no-new-content messaging were observed directly. Non-English failure messaging was not re-run on Windows after the fix, so that checklist item remains partial rather than full.
- Windows CLI now has its own direct validation record in `docs/validation/windows_cli.md`; this document should not be stretched to cover that surface.
- The March 19, 2026 Windows `pytest` failure recorded a real shared-harness portability defect at that time.
- As of March 22, 2026, the repo harness has been updated so the shared baseline no longer depends on named timezone data and the rollout fixtures render Windows-style paths safely, but a fresh Windows rerun still needs to be recorded before the automated Windows gap can be considered closed.
