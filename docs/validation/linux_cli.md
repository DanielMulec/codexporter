# Linux Codex CLI Validation

- Validation dates: March 18, March 27, and April 3, 2026
- Validation status: validated
- Host OS: Linux
- Codex surface: Codex CLI in Kitty
- Codex versions observed: `0.115.x` (March 18 live run; exact patch not recorded), `0.117.0` (March 27 restricted-access and ambiguity close-out), `0.77.0` (March 27 German failure-path replay), `0.118.0` (April 3 post-refactor live rerun and controlled close-out refresh)
- Models observed: `gpt-5.4`, `gpt-5.2`
- Approval modes observed: March 18 live run not retained; March 27 controlled close-out observed `on-request` and `never`; April 3 rerun observed `never`
- Sandbox modes observed: March 18 live run not retained; March 27 controlled close-out observed `workspace-write` with network access and `danger-full-access`; April 3 rerun observed `danger-full-access`

## Evidence

- Daniel directly validated the skill in Linux Codex CLI running in Kitty on March 18, 2026.
- Daniel reported on March 22, 2026 that he had also already installed this skill successfully through `skill-installer` on his Linux device and used the resulting globally installed `export` skill in real use; the exact installer transcript and installed path were not retained in the repository notes.
- The March 18 live run covered first export, default destination, success message with path, repeated incremental behavior, no-new-content behavior, filename sequencing, and rendered markdown quality.
- On March 27, 2026, ran `./.venv/bin/python skills/export/scripts/export_skill.py` on Linux against isolated temporary Codex homes under `/tmp/codexporter-linux-validation-4jEM58`, populated with copied real Linux CLI thread rows and copied rollout artifacts so the rare failure-path conditions could be forced without mutating live `~/.codex` state.
- The fresh Linux-host automated gate rerun recorded on March 27, 2026 passed `pytest`, which includes the explicit compact full-flow and deterministic compaction coverage that exercises `$export --compact`, large raw payload omission, short-diff retention, oversized JSON-output compaction, and shared checkpoint behavior.
- On April 3, 2026, recreated `.venv` on the Linux host under Python `3.14.3` and reran `./.venv/bin/python -m pytest`, `./.venv/bin/python -m mypy skills/export tests`, `./.venv/bin/python -m ruff check .`, and `./.venv/bin/python -m ruff format --check .`; all four gates passed from the current repo state.
- On April 3, 2026, ran `./.venv/bin/python skills/export/scripts/export_skill.py --project-root /home/dmulec/projekte/codexporter --codex-home /home/dmulec/.codex` against live Linux CLI thread `019d54d3-1ead-7c12-b9e2-8d3c9716ebd0`, source `cli`, Codex `0.118.0`, model `gpt-5.4`, approval `never`, sandbox `danger-full-access`, and observed first export creation at `/home/dmulec/projekte/codexporter/codex_exports/20260403-213745-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-1.md`.
- In that same live Linux workspace, the persisted state DB held three thread rows for `/home/dmulec/projekte/codexporter`; `env -u CODEX_THREAD_ID ./.venv/bin/python skills/export/scripts/export_skill.py --project-root /home/dmulec/projekte/codexporter --codex-home /home/dmulec/.codex` failed clearly with the ambiguous-session message instead of guessing, and the targeted follow-up `./.venv/bin/python skills/export/scripts/export_skill.py --project-root /home/dmulec/projekte/codexporter --codex-home /home/dmulec/.codex --compact` created compact incremental export `/home/dmulec/projekte/codexporter/codex_exports/20260403-213756-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-2.md` while advancing the same live checkpoint to sequence `2`.
- On April 3, 2026, reran the production entrypoint on Linux against isolated temporary Codex homes under `/tmp/codexporter-linux-validation-yxEzjU`, populated with the current live Linux CLI thread row `019d54d3-1ead-7c12-b9e2-8d3c9716ebd0` and copied rollout history so the post-refactor edge cases could be forced without mutating live `~/.codex` state.
- In `/tmp/codexporter-linux-validation-yxEzjU/sequence`, a compact-first run created `/tmp/codexporter-linux-validation-yxEzjU/sequence/sequence-project/codex_exports/20260403-213924-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-1.md` with `Render profile: compact` plus repeated deterministic omission markers such as `Raw file contents omitted in compact mode.` and `Large raw tool output omitted in compact mode.`; after appending one synthetic visible turn to the copied rollout, a full rerun created incremental export `/tmp/codexporter-linux-validation-yxEzjU/sequence/sequence-project/codex_exports/20260403-213956-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-2.md`, and a third rerun with no further rollout change returned `There is no new content to export since the last successful export.` without creating a `-3` artifact.
- In `/tmp/codexporter-linux-validation-yxEzjU/german`, a copied rollout with one appended German visible user turn first created `/tmp/codexporter-linux-validation-yxEzjU/german/german-project/codex_exports/20260403-214016-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-1.md`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- In `/tmp/codexporter-linux-validation-yxEzjU/restricted`, removing read permission from `/tmp/codexporter-linux-validation-yxEzjU/restricted/rollouts/restricted-rollout.jsonl` produced the explicit persisted-session-history failure and created no export or checkpoint artifacts.
- In `/tmp/codexporter-linux-validation-yxEzjU/ambiguous`, seeding two same-workspace thread rows in the isolated `state_5.sqlite` reproduced the untargeted ambiguous-session failure under `env -u CODEX_THREAD_ID`; the targeted rerun with `CODEX_THREAD_ID=019d54d3-1ead-7c12-b9e2-8d3c9716ebd0` then exported `/tmp/codexporter-linux-validation-yxEzjU/ambiguous/ambiguous-project/codex_exports/20260403-214038-We-just-did-a-refactor-in-order-to-get-out-all-of-the-implic-1.md` plus sidecar `/tmp/codexporter-linux-validation-yxEzjU/ambiguous/ambiguous-project/codex_exports/019d54d3-1ead-7c12-b9e2-8d3c9716ebd0-checkpoint.json`.
- In `/tmp/codexporter-linux-validation-yxEzjU/mismatch`, explicitly targeting session `linux-mismatch-thread` from `/tmp/codexporter-linux-validation-yxEzjU/mismatch/mismatch-project` failed clearly because the copied thread row belonged to `/tmp/codexporter-linux-validation-yxEzjU/mismatch/other-project`, and running the production entrypoint with `--project-root /home/dmulec/projekte/codexporter/skills/export` failed with the unsafe-project-root message without creating `skills/export/codex_exports`.

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
- The April 3 rerun refreshed the Linux CLI checklist directly on the current post-refactor repo state instead of relying only on the March 27 close-out: it re-observed live full export, live ambiguity fail-closed behavior, live compact incremental behavior, compact-first/full-second shared checkpoint behavior, no-new-content behavior, German checkpoint-failure localization, denied rollout access, explicit workspace-mismatch fail-closed behavior, and unsafe-project-root rejection.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- The live validation shell already exported a `CODEX_THREAD_ID` for the active conversation, so the untargeted close-out commands used `env -u CODEX_THREAD_ID` to keep the isolated replay controlled by the copied temp state rather than the live thread.
- With the March 18 live success-path evidence, the March 27 historical close-out, and the April 3 fresh live plus controlled reruns, the Linux CLI checklist is fully observed on the current repo state.
- The compact checklist item is now backed by the April 3, 2026 live compact incremental rerun, the compact-first/full-second shared-checkpoint replay under `/tmp/codexporter-linux-validation-yxEzjU/sequence`, and the fresh Linux-host automated full-flow and compaction tests.
