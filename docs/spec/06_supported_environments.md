# Supported Environments

## Status

- Phase: implementation and validation
- Date: March 27, 2026

## Purpose

This document defines the current support targets for v1 based on:

- the desired product reach for this project
- the current public Codex platform support picture

## Current Session Definition

For this project, the `current session` means the live chat thread the user is currently in when `$export` is invoked in Codex CLI or the Codex app.

When a precise runtime thread or session identifier is available at invocation time, that identifier is authoritative over workspace-based discovery.

Workspace-path-based discovery is only an allowed fallback when no precise current-thread identifier is available and the result is unambiguous.

This applies to:

- the currently active Codex CLI thread
- the currently active Codex app thread

It does not mean:

- all sessions in the workspace
- the last session on disk
- the newest session that happens to share the same workspace path
- a project-wide merged history

## V1 Environment Targets

### Primary v1 targets

- macOS Codex CLI
- Linux Codex CLI
- macOS Codex app
- Windows Codex CLI
- Windows Codex app

## Support Notes

- The specification should distinguish between:
  - target support
  - validated support
- Validation must happen separately from this support-target document.
- For this project, Windows Codex CLI is a required v1 product target.
- As of March 27, 2026, current OpenAI Codex documentation is inconsistent about native Windows CLI support: the dedicated CLI setup page still describes Windows support as experimental and recommends WSL, while the Codex quickstart currently lists the CLI as supported on macOS, Windows, and Linux.
- This repository treats Windows Codex CLI as both an in-scope v1 target and a validated repository surface based on direct repo-controlled evidence recorded in `docs/spec/22_platform_validation.md` and `docs/validation/windows_cli.md`.
- Because the upstream support picture is still inconsistent, native Windows Codex CLI should still be treated as a higher external-platform-risk surface than macOS or Linux CLI even though this repository's own v1 validation checklist is closed.
- Validation for Windows support may be established through real-user testing by Daniel and trusted Windows users in addition to repo-driven validation scenarios.
- Platform validation is not complete unless it includes current-thread targeting correctness, not just happy-path export success.
- Where practical, platform validation should include same-workspace multi-thread conditions and platform-specific path-representation differences.

## Documentation Rule

Whenever environment support is described elsewhere in the spec, it should use the same distinction:

- primary v1 targets
- validated support status

## Source Basis

Checked on March 27, 2026 against:

- [Codex CLI setup](https://developers.openai.com/codex/cli/#cli-setup)
- [Codex quickstart setup](https://developers.openai.com/codex/quickstart/#setup)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
