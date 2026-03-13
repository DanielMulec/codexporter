# Product Triage

This document is only for prioritization.

## Must

- Export the current session into markdown.
- Work in Codex CLI and Codex app where the required capabilities are actually available.
- Be installable once as a global Codex skill and usable across project contexts without per-project reinstallation.
- Include the core visible workflow trail:
  - user messages
  - assistant final answers
  - assistant progress or commentary updates when available
  - tool calls and tool outputs when available
- Support repeated export within the same session without blindly duplicating already-exported content.
- Produce output that is readable without extra tooling.
- Fail clearly when data cannot be accessed.

## Should

- Separate raw export from optional summarized or classified report output.
- Include git context when available, such as status and diff snapshots.
- Support both direct invocation by skill name and natural-language invocation if the platform permits it reliably.
- Support configurable export modes such as:
  - full worklog
  - handoff summary
  - learning log
  - spec or documentation summary
- Use a checkpoint model for repeated exports within the same chat instance.

## Could

- Produce a multi-file export bundle instead of a single markdown file.
- Add optional AI-generated reporting or classification after the raw export is complete.
- Let users choose the report style or classifier goal.
- Add project-level rollups that combine multiple session exports later.
- Add machine-readable sidecar files in a later version if markdown alone becomes limiting.
