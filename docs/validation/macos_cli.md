# macOS Codex CLI Validation

- Validation dates: March 18 and March 27, 2026
- Validation status: validated
- Host OS: macOS
- Codex surface: Codex CLI in Ghostty
- Codex versions observed: `0.115.x` (March 18 live run; exact patch not recorded), `0.116.0` (March 27 restricted-access and ambiguity close-out), `0.80.0` (March 27 German failure-path replay)
- Models observed: `gpt-5.4`, `gpt-5.2-codex`
- Approval modes observed: March 18 live run not retained; March 27 controlled close-out used `on-request`
- Sandbox modes observed: March 18 live run not retained; March 27 controlled close-out used `workspace-write` with network access

## Evidence

- Daniel directly validated the skill in macOS Codex CLI running in Ghostty on March 18, 2026.
- Daniel reported on March 22, 2026 that he had also already installed this skill successfully through `skill-installer` on his macOS device and used the resulting globally installed `export` skill in real use; the exact installer transcript and installed path were not retained in the repository notes.
- The March 18 live run covered first export, default destination, success message with path, repeated incremental behavior, no-new-content behavior, filename sequencing, and rendered markdown quality.
- On March 27, 2026, ran `./.venv/bin/python skills/export/scripts/export_skill.py` on macOS against isolated temporary Codex homes under `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl`, populated with copied real macOS CLI thread rows and copied rollout artifacts so the rare failure-path conditions could be forced without mutating live `~/.codex` state.
- The localized failure-path replay used copied real macOS CLI thread `019ba91a-6d80-7373-9ece-3ecab3e4736d`, source `cli`, CLI `0.80.0`, model `gpt-5.2-codex`, approval `on-request`, sandbox `workspace-write` with network access, and rollout copy `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/rollouts/cli-language-rollout.jsonl`.
- That localized failure-path replay first created `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/cli-lang-project/codex_exports/20260327-090216-Hello-Codex-Do-you-have-web-search-access-and-internet-acces-1.md` plus sidecar `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/cli-lang-project/codex_exports/019ba91a-6d80-7373-9ece-3ecab3e4736d-checkpoint.json`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- The restricted-access and ambiguity close-out used copied real macOS CLI thread `019d25c7-6b90-7092-a2c9-1273d3f43cb7`, source `cli`, CLI `0.116.0`, model `gpt-5.4`, approval `on-request`, sandbox `workspace-write` with network access.
- After removing read permission from `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/rollouts/cli-restricted-rollout.jsonl`, the exporter returned the explicit persisted-session-history failure and created no export or checkpoint artifacts.
- After seeding two same-workspace thread rows in the isolated `state_5.sqlite`, the untargeted run failed clearly with the ambiguous-session message, and the targeted rerun with `CODEX_THREAD_ID=forced-cli-ambiguous-a` exported `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/cli-ambiguous-project/codex_exports/20260327-090217-Hey-GPT-I-lost-complete-train-of-where-the-project-currently-1.md` plus sidecar `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-validation-iunfq0pl/cli-ambiguous-project/codex_exports/019d25c7-6b90-7092-a2c9-1273d3f43cb7-checkpoint.json`.

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

## Notes

- The March 27 close-out intentionally used isolated temporary Codex state derived from real macOS CLI persisted-session records because the missing failure-path and ambiguity cases had not reproduced on demand in normal live use.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- With the March 18 live success-path evidence plus the March 27 controlled failure-path and ambiguity evidence, the macOS CLI checklist is fully observed.
