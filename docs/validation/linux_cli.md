# Linux Codex CLI Validation

- Validation dates: March 18, March 27, and April 3, 2026
- Validation status: validated
- Host OS: Linux
- Codex surface: Codex CLI in Kitty
- Codex versions observed: `0.115.x` (March 18 live run; exact patch not recorded), `0.117.0` (March 27 restricted-access and ambiguity close-out), `0.77.0` (March 27 German failure-path replay)
- Models observed: `gpt-5.4`, `gpt-5.2`
- Approval modes observed: March 18 live run not retained; March 27 controlled close-out observed `on-request` and `never`
- Sandbox modes observed: March 18 live run not retained; March 27 controlled close-out observed `workspace-write` with network access and `danger-full-access`

## Evidence

- Daniel directly validated the skill in Linux Codex CLI running in Kitty on March 18, 2026.
- Daniel reported on March 22, 2026 that he had also already installed this skill successfully through `skill-installer` on his Linux device and used the resulting globally installed `export` skill in real use; the exact installer transcript and installed path were not retained in the repository notes.
- The March 18 live run covered first export, default destination, success message with path, repeated incremental behavior, no-new-content behavior, filename sequencing, and rendered markdown quality.
- On March 27, 2026, ran `./.venv/bin/python skills/export/scripts/export_skill.py` on Linux against isolated temporary Codex homes under `/tmp/codexporter-linux-validation-4jEM58`, populated with copied real Linux CLI thread rows and copied rollout artifacts so the rare failure-path conditions could be forced without mutating live `~/.codex` state.
- The fresh Linux-host automated gate rerun recorded on March 27, 2026 passed `pytest`, which includes the explicit compact full-flow and deterministic compaction coverage that exercises `$export --compact`, large raw payload omission, short-diff retention, oversized JSON-output compaction, and shared checkpoint behavior.
- On April 3, 2026, Daniel revalidated the post-Stage-2 live Linux CLI happy path and confirmed that both full and compact exports still worked from the current repo state. This reconfirmation was happy-path-only; no new failure-path or ambiguity evidence was added in that pass.
- The localized failure-path replay used copied real Linux CLI thread `019b84c4-118a-7330-ac1c-a5b8fdfdd39f`, source `cli`, CLI `0.77.0`, model `gpt-5.2`, approval `on-request`, sandbox `workspace-write` with network access, and rollout copy `/tmp/codexporter-linux-validation-4jEM58/rollouts/cli-language-rollout.jsonl`.
- That localized failure-path replay first created `/tmp/codexporter-linux-validation-4jEM58/cli-lang-project/codex_exports/20260327-110400-Shell-Fish-Distro-Fedora-43-KDE-Edition-Problem-wir-mussen-g-1.md` plus sidecar `/tmp/codexporter-linux-validation-4jEM58/cli-lang-project/codex_exports/019b84c4-118a-7330-ac1c-a5b8fdfdd39f-checkpoint.json`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- The restricted-access and ambiguity close-out used copied real Linux CLI thread `019d2e99-e915-7681-a850-7510249f694e`, source `cli`, CLI `0.117.0`, model `gpt-5.4`, approval `never`, sandbox `danger-full-access`.
- After removing read permission from `/tmp/codexporter-linux-validation-4jEM58/rollouts/cli-restricted-rollout.jsonl`, the exporter returned the explicit persisted-session-history failure and created no export or checkpoint artifacts.
- After seeding two same-workspace thread rows in the isolated `state_5.sqlite`, the untargeted run failed clearly with the ambiguous-session message, and the targeted rerun with `CODEX_THREAD_ID=019d2e99-e915-7681-a850-7510249f694e` exported `/tmp/codexporter-linux-validation-4jEM58/cli-ambiguous-project/codex_exports/20260327-110439-Hi-GPT-This-repo-isn-t-up-to-date-with-github-anymore-please-1.md` plus sidecar `/tmp/codexporter-linux-validation-4jEM58/cli-ambiguous-project/codex_exports/019d2e99-e915-7681-a850-7510249f694e-checkpoint.json`.

## Checklist Results

- first export: pass
- default export destination: pass
- success message with file location: pass
- incremental export: pass
- no-new-content behavior: pass
- filename sequencing: pass
- markdown rendering: pass
- language-sensitive failure messaging: pass
- restricted-environment honesty: pass
- current-thread targeting under shared-workspace ambiguity or path variation: pass
- compact export behavior: pass

## Notes

- The March 27 close-out intentionally used isolated temporary Codex state derived from real Linux CLI persisted-session records because the missing failure-path and ambiguity cases had not reproduced on demand in normal live use.
- The April 3 reconfirmation was happy-path-only. It did not add new failure-path, no-new-content, or ambiguity evidence, so the March 27 controlled close-out remains the authoritative close-out for those checklist items.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- The live validation shell already exported a `CODEX_THREAD_ID` for the active conversation, so the untargeted close-out commands used `env -u CODEX_THREAD_ID` to keep the isolated replay controlled by the copied temp state rather than the live thread.
- With the March 18 live success-path evidence plus the March 27 controlled failure-path and ambiguity evidence, the Linux CLI checklist is fully observed.
- The compact checklist item is now backed by Daniel's April 3, 2026 live Linux full and compact happy-path retest plus the fresh Linux-host automated full-flow and compaction tests.
