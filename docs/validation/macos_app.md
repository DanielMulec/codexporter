# macOS Codex App Validation

- Date: March 13, 2026
- Validation status: partial
- Host OS: macOS
- Codex surface: Codex Desktop app context
- Rollout source field: `vscode`
- Codex version: `0.115.0-alpha.11`
- Model: `gpt-5.4`
- Sandbox mode: `danger-full-access`
- Approval mode: `never`

## Evidence

- Ran `./.venv/bin/python skills/export/scripts/export_skill.py --project-root /Users/danielmulec/Projekte/codexporter --codex-home /Users/danielmulec/.codex` from the active project root.
- Observed first export creation at `codex_exports/20260313-221601-review-whether-21-coverage-matrix-md-is-complete-enough-as-t-1.md`.
- Observed second incremental export creation at `codex_exports/20260313-221620-review-whether-21-coverage-matrix-md-is-complete-enough-as-t-2.md`.
- Observed no-new-content behavior by calling `export_current_session(...)` twice inside one shell process; the first call created `codex_exports/20260313-221644-review-whether-21-coverage-matrix-md-is-complete-enough-as-t-3.md` and the second call returned `There is no new content to export since the last successful export.` without creating another markdown file.
- Inspected the live checkpoint sidecar at `codex_exports/019ce8a6-83c4-7ca3-8b8a-aef4a1bbd26b-checkpoint.json` after the first and second real exports.
- Inspected the rendered markdown artifacts and confirmed the visible-chat-first structure, metadata header, tool sections, and export metadata footer.
- Ran automated gates in the repo on the same day:
  - `./.venv/bin/ruff check .`
  - `./.venv/bin/ruff format --check .`
  - `./.venv/bin/mypy skills/export tests`
  - `./.venv/bin/pytest`

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

## Notes

- This validation record covers the macOS Codex app runtime behavior in the current desktop-app session context. It does not yet validate GitHub skill installation flow end to end.
- English user-facing success and no-new-content messages were observed directly. Non-English failure or omission behavior still needs separate real-use validation.
