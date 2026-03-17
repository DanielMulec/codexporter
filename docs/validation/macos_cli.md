# macOS Codex CLI Validation

- Validation record date: March 18, 2026
- Validation status: partial
- Host OS: macOS
- Codex surface: Codex CLI in Ghostty
- Codex version: `0.115.x` (exact patch not recorded)
- Model: `gpt-5.4`
- Sandbox mode: not recorded
- Approval mode: not recorded

## Evidence

- Daniel directly validated the skill in macOS Codex CLI running in Ghostty.
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
- The exact CLI patch/build number was not retained; only the `0.115` series alignment with the corresponding macOS validation was confirmed.
