# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 10, 2026

## Key Open Questions

- What exact optional fields beyond the current v1 contract are worth including without adding noise?
- How much optional environment metadata should appear in the default markdown output versus a later expanded mode?
- What exact sidecar schema should represent checkpoint state?
- What exact user-facing wording should be standardized for degraded-mode failures and omissions?
- What validation is required before Windows Codex CLI can be upgraded from best-effort to a primary supported environment?

## Recommended Next Spec Steps

1. Turn the current v1 decisions into acceptance criteria while preserving the additive-stage and additive-artifact extension model.
2. Define the checkpoint sidecar schema.
3. Define the markdown section order and formatting rules for the primary export artifact.
4. Define test scenarios for successful export, incremental export, non-git export, and degraded-mode behavior.
5. Validate the support matrix against real environments, especially Windows Codex CLI.
