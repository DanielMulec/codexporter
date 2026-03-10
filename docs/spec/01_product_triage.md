# Product Triage

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope level: initial product triage, not implementation spec

## Purpose

This document captures the first structured triage for the Codex export skill project.

It translates the current discussion into:

- goals
- non-goals
- assumptions
- initial must / should / could prioritization
- initial user stories

This is intentionally a decision-shaping document. It does not yet define the full technical architecture, file formats, or test plan in detail.

## Problem Statement

Codex users currently lack a reliable, reusable way to export the meaningful history of the current chat session into a durable markdown artifact.

The desired product is a Codex skill that can export the current session into markdown and, optionally, produce a derived report that helps the user understand what happened in the session, what changed, and what work was performed.

## Goals

- Create a Codex skill that exports the current session into one or more markdown files.
- Support Codex CLI and Codex app in the environments where Codex currently supports skills and local session data access.
- Preserve the meaningful workflow record of the session, not just the final assistant answer.
- Make repeated export within the same session practical and understandable for users.
- Keep the export readable by humans and useful for handoff, learning, documentation, and audit purposes.
- Design the product to be cross-platform where Codex itself is available and where the skill can access the required local data.
- Leave room for optional post-export AI summarization or classification without making it mandatory for the core export flow.

## Non-Goals

These items are explicitly out of scope for the initial version unless later promoted:

- Exporting hidden chain-of-thought or private model reasoning.
- Depending on undocumented internal platform behavior as if it were guaranteed stable.
- Guaranteeing automatic temporary sandbox escalation and automatic restoration across all environments.
- Guaranteeing Linux support for the Codex desktop app if the platform itself does not provide it.
- Building a full project knowledge management system, analytics system, or long-term archive browser in v1.
- Exporting every possible internal system event if those events are not stable, accessible, or useful to end users.

## Product Assumptions

- Codex persists enough local session data to enable a useful export flow.
- The skill can rely on visible session artifacts more safely than on internal or hidden reasoning data.
- A raw export and a derived report are separate product concerns and should not be conflated.
- Repeated exports in the same session are common enough to justify checkpoint behavior.
- Markdown is the primary output format for v1.
- Users value transparency into tool activity, file work, and git state alongside the conversation itself.

## Platform Assumptions and Constraints

- Current platform support must be defined based on actual Codex product support, not aspirational support.
- Codex CLI and Codex app may expose different runtime capabilities and storage layouts.
- Sandboxing and approval behavior may limit file access, especially outside the workspace.
- A skill should not assume it can always self-upgrade its privileges without user interaction or platform support.
- Git context may or may not exist for a given session.
- Export behavior must remain useful even when some optional data sources are unavailable.

## Must / Should / Could

### Must

- Export the current session into markdown.
- Work in Codex CLI and Codex app where the required capabilities are actually available.
- Include the core visible workflow trail:
  - user messages
  - assistant final answers
  - assistant progress or commentary updates when available
  - tool calls and tool outputs when available
- Support repeated export within the same session without blindly duplicating already-exported content.
- Produce output that is readable without extra tooling.
- Fail clearly when data cannot be accessed.

### Should

- Separate raw export from optional summarized or classified report output.
- Include git context when available, such as status and diff snapshots.
- Support both direct invocation by skill name and natural-language invocation if the platform permits it reliably.
- Support configurable export modes such as:
  - full worklog
  - handoff summary
  - learning log
  - spec or documentation summary
- Use a checkpoint model for repeated exports within the same chat instance.

### Could

- Produce a multi-file export bundle instead of a single markdown file.
- Add optional AI-generated reporting or classification after the raw export is complete.
- Let users choose the report style or classifier goal.
- Add project-level rollups that combine multiple session exports later.
- Add machine-readable sidecar files in a later version if markdown alone becomes limiting.

## Initial User Stories

### Core Export

- As a Codex user, I want to invoke an export skill from the current session so that I can preserve the chat history in markdown.
- As a Codex user, I want the export to include the meaningful workflow trail so that I can see what the agent actually did, not just the final answer.
- As a Codex user, I want the export to be readable and well-structured so that I can use it for documentation, handoff, or review.

### Repeated Export

- As a Codex user, I want repeated exports in the same session to continue from the last export point so that I do not get noisy duplication.
- As a Codex user, I want it to be clear whether an export is a full export or an incremental export so that I understand what changed since the previous checkpoint.

### Git-Aware Export

- As a Codex user working in a git repository, I want the export to include git context so that I can correlate the conversation with actual repository changes.
- As a Codex user, I want missing git data to degrade gracefully so that the export still works in non-git contexts.

### Optional AI-Derived Report

- As a Codex user, I want an optional report generated from the export so that I can quickly understand what happened in the session.
- As a Codex user, I want control over the report purpose so that the post-processing matches my workflow.
- As a Codex user, I want the original raw export preserved even when an AI-derived report is generated so that I retain an auditable source record.

### Cross-Platform Behavior

- As a Codex user, I want the skill to work consistently across the supported operating systems for Codex so that I can rely on it in different environments.
- As a Codex user in a restricted environment, I want the skill to tell me clearly what it can and cannot access so that I understand the result and the limitations.

## Initial UX Principles

- The raw export is the source record.
- Optional AI summarization must never replace the source record.
- Repeated export behavior must be predictable.
- Degraded-mode behavior must be explicit, not silent.
- The user should not need to understand internal Codex storage details to use the skill successfully.

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

## Source Notes

This triage is based on:

- the March 10, 2026 project discussion
- current Codex platform constraints checked on March 10, 2026
- local verification that Codex persists session data on disk in the current environment
