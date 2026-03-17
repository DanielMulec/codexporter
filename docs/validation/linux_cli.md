# Linux Codex CLI Validation

- Validation record date: March 18, 2026
- Validation status: partial
- Host OS: Linux
- Codex surface: Codex CLI in Kitty
- Codex version: `0.115.x` (reported by Daniel as the same series as the macOS CLI/App validation; exact patch not recorded)
- Model: `gpt-5.4`
- Sandbox mode: not recorded
- Approval mode: not recorded

## Evidence

- Daniel directly validated the skill in Linux Codex CLI running in Kitty.
- First export succeeded.
- The export destination was the `codex_exports/` subfolder under the active project root.
- The success message included the export file name and path.
- Repeated export behavior was incremental.
- Repeated export with no new content did not create a new file and informed the user directly.
- Export filename sequencing behaved correctly across repeated exports.
- Rendered markdown output matched expectations.
- Validation included both more-restricted and less-restricted runtime configurations, but the exact Codex `approval mode` and `sandbox mode` labels were not captured at test time.
- No failure or blocked-access case was encountered during these runs, so language-sensitive failure messaging and restricted-environment honesty were not observed directly.

## Checklist Results

- first export: pass
- default export destination: pass
- success message with file location: pass
- incremental export: pass
- no-new-content behavior: pass
- filename sequencing: pass
- markdown rendering: pass
- language-sensitive failure messaging: not run
- restricted-environment honesty: not run

## Notes

- This record intentionally stays concise because the observed behavior was clean and uneventful.
