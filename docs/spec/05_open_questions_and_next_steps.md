# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 10, 2026

## Key Open Questions

- What is the exact definition of the "current session" across Codex CLI and Codex app?
- What exact session fields are stable enough to be part of the supported export contract?
- Should v1 output be one markdown file or a small bundle of markdown files?
- Where should checkpoint state live?
- What should happen when the current environment blocks access to the relevant session history?
- Is optional AI classification a v1 feature or a later phase?
- Which skill invocation names should be supported?

## Recommended Next Spec Steps

1. Define supported environments precisely, based on actual Codex platform support.
2. Define the export data contract: what is included, excluded, optional, and unsupported.
3. Define the output artifact structure and naming rules.
4. Define incremental export and checkpoint behavior.
5. Define degraded-mode behavior under sandbox or restricted access.
6. Decide whether AI-derived reporting is in v1 or v1.1.
7. Write acceptance criteria and test scenarios only after the above decisions are fixed.
