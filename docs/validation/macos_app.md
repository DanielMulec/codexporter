# macOS Codex App Validation

- Validation dates: March 13-14 and March 27, 2026
- Validation status: validated
- Host OS: macOS
- Codex surface: Codex Desktop app context
- Rollout source field: `vscode`
- Codex version: `0.115.0-alpha.11`
- Models observed: `gpt-5.4`
- Approval modes observed: `never` (March 13-14 live app-context validation), `on-request` (March 27 controlled close-out source row)
- Sandbox modes observed: `danger-full-access` (March 13-14 live app-context validation), `workspace-write` without network access (March 27 controlled close-out source row)

## Evidence

- Ran `./.venv/bin/python skills/export/scripts/export_skill.py --project-root /Users/danielmulec/Projekte/codexporter --codex-home /Users/danielmulec/.codex` from the active project root.
- Observed first export creation at `codex_exports/20260313-221601-review-whether-21-coverage-matrix-md-is-complete-enough-as-t-1.md`.
- Observed second incremental export creation at `codex_exports/20260313-221620-review-whether-21-coverage-matrix-md-is-complete-enough-as-t-2.md`.
- Observed no-new-content behavior by calling `export_current_session(...)` twice inside one shell process; the first call created `codex_exports/20260313-221644-review-whether-21-coverage-matrix-md-is-complete-enough-as-t-3.md` and the second call returned `There is no new content to export since the last successful export.` without creating another markdown file.
- Inspected the live checkpoint sidecar at `codex_exports/019ce8a6-83c4-7ca3-8b8a-aef4a1bbd26b-checkpoint.json` after the first and second real exports.
- Inspected the rendered markdown artifacts and confirmed the visible-chat-first structure, metadata header, tool sections, and export metadata footer.
- On March 14, 2026, invoked the globally installed skill under the renamed `$export` boundary in the active macOS Codex app thread and observed incremental export creation at `codex_exports/20260314-171923-I-ran-the-installed-skill-normally-It-returned-2.md`.
- Confirmed that the installed skill boundary at `~/.codex/skills/export/` wrote the artifact into the active project's `codex_exports/` directory rather than into the installed skill directory.
- On March 27, 2026, ran `./.venv/bin/python skills/export/scripts/export_skill.py` on macOS against isolated temporary Codex homes under `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl`, populated with copied real macOS app thread `019cf207-561a-72e0-8add-8dbd3ec4efc2`, source `vscode`, Codex `0.115.0-alpha.11`, model `gpt-5.4`, approval `on-request`, and sandbox `workspace-write` without network access.
- That controlled app close-out first created `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/app-lang-project/codex_exports/20260327-090217-Ich-will-beim-export-skill-deutsche-UX-testen-Bitte-generier-1.md` plus sidecar `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/app-lang-project/codex_exports/019cf207-561a-72e0-8add-8dbd3ec4efc2-checkpoint.json`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- After removing read permission from `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/rollouts/app-restricted-rollout.jsonl`, the exporter returned the explicit persisted-session-history failure and created no export or checkpoint artifacts.
- After seeding two same-workspace `vscode` rows in the isolated `state_5.sqlite`, the untargeted run failed clearly with the ambiguous-session message, and the targeted rerun with `CODEX_THREAD_ID=forced-app-ambiguous-a` exported `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/app-ambiguous-project/codex_exports/20260327-090217-Ich-will-beim-export-skill-deutsche-UX-testen-Bitte-generier-1.md` plus sidecar `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/app-ambiguous-project/codex_exports/019cf207-561a-72e0-8add-8dbd3ec4efc2-checkpoint.json`.
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
- language-sensitive failure messaging: pass
- restricted-environment honesty: pass
- current-thread targeting under shared-workspace ambiguity or path variation: pass

## Notes

- This record now closes the remaining macOS app checklist items for non-English failure behavior, restricted-environment honesty, and same-workspace current-thread safety.
- The March 27 close-out intentionally used isolated temporary Codex state derived from real macOS app persisted-session data because those failure-path conditions had not reproduced reliably in ordinary live use.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- This validation record covers the macOS app platform checklist. It still does not turn GitHub-origin installation flow into a separate validated requirement.
