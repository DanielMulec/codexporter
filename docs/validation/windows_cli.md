# Windows Codex CLI Validation

- Validation dates: March 20 and March 27, 2026
- Validation status: validated
- Host OS: Windows
- Codex surface: Codex CLI
- Codex versions observed: March 20 live happy-path metadata not retained; March 27 controlled close-out on `0.116.0`
- Models observed: `gpt-5.4`
- Approval modes observed: March 20 live run not retained; March 27 controlled close-out observed `never`
- Sandbox modes observed: March 20 live run not retained; March 27 controlled close-out observed `danger-full-access`

## Evidence

- Daniel directly validated the skill happy path in Windows Codex CLI on March 20, 2026.
- Daniel reported on March 22, 2026 that he had already installed this skill successfully through `skill-installer` on his Windows device and used the resulting globally installed `export` skill in real use; the exact installer transcript and installed path were not retained in the repository notes.
- The March 20 live run covered first export, default destination, success message with path, and repeated incremental behavior, but the exact runtime metadata and artifact names were not preserved then.
- On March 27, 2026, ran `.\.venv\Scripts\python.exe skills/export/scripts/export_skill.py` on Windows against isolated temporary Codex homes under `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w`, populated with copied real Windows CLI thread rows and copied rollout artifacts so the remaining Windows-only failure-path and ambiguity cases could be forced without mutating live `C:\Users\DanielMulecDatenpol\.codex` state.
- The fresh Windows-host automated gate rerun on March 31, 2026 passed `.\.venv\Scripts\python.exe -m pytest`, including the explicit compact full-flow and deterministic compaction coverage that exercises `$export --compact`, large raw payload omission, short-diff retention, oversized JSON-output compaction, and shared checkpoint behavior.
- The localized failure-path replay used copied real Windows CLI thread `019d2932-b04b-79f3-a6d8-f7dc253a9d91`, source `cli`, Codex `0.116.0`, model `gpt-5.4`, approval `never`, sandbox `danger-full-access`, and rollout copy `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-language\rollouts\cli-language-rollout.jsonl`.
- That localized failure-path replay first created `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-language\cli-lang-project\codex_exports\20260327-144750-Hey-GPT-We-have-one-more-feature-task-on-this-project-then-t-1.md` plus sidecar `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-language\cli-lang-project\codex_exports\019d2932-b04b-79f3-a6d8-f7dc253a9d91-checkpoint.json`; after intentionally corrupting the sidecar, the next run failed in German with the unreadable-checkpoint message.
- The sequencing and no-new-content close-out used copied real Windows CLI thread `019d29bf-b8d5-7743-9145-cbc8e620820b`, source `cli`, Codex `0.116.0`, model `gpt-5.4`, approval `never`, sandbox `danger-full-access`, and rollout copy `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-sequence\rollouts\cli-sequence-rollout.jsonl`.
- That sequencing replay first created `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-sequence\cli-sequence-project\codex_exports\20260327-144750-datenpol-euro-demo-https-codextaxes4-odoo19-at-5720d575634d5-1.md`; after appending one synthetic visible turn to the copied rollout, the next run created `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-sequence\cli-sequence-project\codex_exports\20260327-144751-datenpol-euro-demo-https-codextaxes4-odoo19-at-5720d575634d5-2.md`; a third run with no further rollout change returned the explicit no-new-content message without creating another markdown file.
- The first sequence artifact was inspected and confirmed to keep the visible-chat-first structure, tool sections, and export metadata footer.
- The restricted-access and ambiguity close-out used copied real Windows CLI thread `019d29bf-b8d5-7743-9145-cbc8e620820b` in additional isolated Codex homes.
- After denying read access to `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-restricted\rollouts\cli-restricted-rollout.jsonl`, the exporter returned the explicit persisted-session-history failure and created no export or checkpoint artifacts.
- After seeding two same-workspace thread rows in the isolated `state_5.sqlite` with Windows extended-length `\\?\` workspace spelling, the untargeted run failed clearly with the ambiguous-session message, and the targeted rerun with `CODEX_THREAD_ID=019d29bf-b8d5-7743-9145-cbc8e620820b` exported `C:\Users\DanielMulecDatenpol\AppData\Local\Temp\codexporter-windows-validation-1ojzvv2w\cli-ambiguity\cli-ambiguous-project\codex_exports\20260327-144751-datenpol-euro-demo-https-codextaxes4-odoo19-at-5720d575634d5-1.md` successfully.
- Ran automated Windows gates in the repo on the same day: `.\.venv\Scripts\python.exe -m pytest`, `.\.venv\Scripts\python.exe -m mypy skills/export tests`, `.\.venv\Scripts\python.exe -m ruff check .`, and `.\.venv\Scripts\python.exe -m ruff format --check .`.

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

- The March 27 close-out intentionally used isolated temporary Codex state derived from real Windows CLI persisted-session records because the missing failure-path and ambiguity cases had not reproduced on demand in normal live use.
- Pre-rollout access failures still fall back to English in v1 by design because the exporter cannot determine conversation language until it can read the rollout content.
- With the March 20 live success-path evidence, the March 27 controlled close-out evidence, and the fresh Windows `.venv` gate rerun, the Windows CLI checklist is fully observed.
- The compact checklist item is currently backed primarily by the fresh Windows-host automated full-flow and compaction tests rather than by a separately retained live `$export --compact` CLI transcript.
