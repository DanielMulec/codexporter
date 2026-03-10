# User Stories

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Source: extracted from the initial product triage

## Purpose

This document contains the initial user stories for the Codex export skill project.

It exists separately from the triage document so that:

- product prioritization stays isolated in `01_product_triage.md`
- user-facing behavior can expand without bloating the triage document
- later acceptance criteria can be mapped here more directly

## Core Export

- As a Codex user, I want to invoke an export skill from the current session so that I can preserve the chat history in markdown.
- As a Codex user, I want the export to include the meaningful workflow trail so that I can see what the agent actually did, not just the final answer.
- As a Codex user, I want the export to be readable and well-structured so that I can use it for documentation, handoff, or review.

## Repeated Export

- As a Codex user, I want repeated exports in the same session to continue from the last export point so that I do not get noisy duplication.
- As a Codex user, I want it to be clear whether an export is a full export or an incremental export so that I understand what changed since the previous checkpoint.

## Git-Aware Export

- As a Codex user working in a git repository, I want the export to include git context so that I can correlate the conversation with actual repository changes.
- As a Codex user, I want missing git data to degrade gracefully so that the export still works in non-git contexts.

## Optional AI-Derived Report

- As a Codex user, I want an optional report generated from the export so that I can quickly understand what happened in the session.
- As a Codex user, I want control over the report purpose so that the post-processing matches my workflow.
- As a Codex user, I want the original raw export preserved even when an AI-derived report is generated so that I retain an auditable source record.

## Cross-Platform Behavior

- As a Codex user, I want the skill to work consistently across the supported operating systems for Codex so that I can rely on it in different environments.
- As a Codex user in a restricted environment, I want the skill to tell me clearly what it can and cannot access so that I understand the result and the limitations.
