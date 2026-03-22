# macOS Codex App Validation

- Validation dates: March 13-14, 2026
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
- On March 14, 2026, invoked the globally installed skill under the renamed `$export` boundary in the active macOS Codex app thread and observed incremental export creation at `codex_exports/20260314-171923-I-ran-the-installed-skill-normally-It-returned-2.md`.
- Confirmed that the installed skill boundary at `~/.codex/skills/export/` wrote the artifact into the active project's `codex_exports/` directory rather than into the installed skill directory.
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
- The March 14 evidence closes the direct macOS app evidence gap for the renamed installed-skill invocation path and for writing to the active project root from the installed skill boundary.
- English user-facing success and no-new-content messages were observed directly. Non-English failure or omission behavior still needs separate real-use validation.
- On March 22, 2026, the macOS-host automated suite added supplemental coverage for German omission or failure messaging and same-workspace current-thread targeting behavior. That evidence strengthens the repo baseline, but it does not convert the remaining macOS app checklist gaps into direct app-runtime validation.
