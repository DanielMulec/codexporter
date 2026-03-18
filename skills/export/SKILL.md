---
name: export
description: Export the current Codex session to markdown when the user asks for $export, export this session or chat, save the current chat history, or create a session transcript. Use for first exports, repeated incremental exports, and no-new-content checks.
---

# Codex Exporter

Use this skill when the user wants a markdown export of the current Codex session.

## Workflow

1. Treat the active project workspace as the command working directory. Do not use the installed skill directory as the project root.
2. Run `scripts/export_skill.py` from this skill directory with the active workspace as the command `workdir`.
3. On Windows, prefer `py -3`. On macOS and Linux, prefer `python3`. Fall back to `python` only if the preferred launcher is unavailable.
4. Relay the script's final user-facing message directly. Do not claim success if the script fails.

## Notes

- Export artifacts are written into `codex_exports/` under the active project root.
- Repeated exports are incremental.
- If there is no new exportable content, the exporter reports that directly and does not create a new markdown file.
