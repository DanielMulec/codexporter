# Supported Environments

## Status

- Phase: analysis and discussion
- Date: March 10, 2026

## Purpose

This document defines the current support targets for v1 based on:

- the desired product reach for this project
- the current public Codex platform support picture

## Current Session Definition

For this project, the `current session` means the live chat thread the user is currently in when `$export` is invoked in Codex CLI or the Codex app.

This applies to:

- the currently active Codex CLI thread
- the currently active Codex app thread

It does not mean:

- all sessions in the workspace
- the last session on disk
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
- Validation must happen separately from this analysis-phase document.
- For this project, Windows Codex CLI is a required v1 product target.
- Validation for Windows support may be established through real-user testing by Daniel and trusted Windows users in addition to repo-driven validation scenarios.

## Documentation Rule

Whenever environment support is described elsewhere in the spec, it should use the same distinction:

- primary v1 targets
- validated support status

## Source Basis

Checked on March 10, 2026 against:

- [OpenAI Codex CLI Getting Started](https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
