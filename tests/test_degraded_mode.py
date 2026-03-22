from __future__ import annotations

from pathlib import Path

import pytest

from codexporter.cli import main
from codexporter.errors import CheckpointError, ProjectRootError
from codexporter.service import export_current_session
from conftest import SessionFixture, build_session_fixture

GERMAN_REPLACEMENTS = {
    "Please outline the implementation plan for the exporter.": (
        "Kannst du das bitte jetzt exportieren, danke?"
    ),
    "Please export the newly added tests as well.": (
        "Kannst du das bitte jetzt erneut exportieren, danke?"
    ),
}


def test_cli_main_missing_session_prints_recovery_guidance_and_returns_one(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    project_root = tmp_path / "project-alpha"
    project_root.mkdir()

    exit_code = main(
        [
            "--project-root",
            str(project_root),
            "--codex-home",
            str(tmp_path / ".codex"),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert (
        captured.out.strip()
        == f"I couldn't find a live Codex session for this workspace at {project_root}. "
        "Run $export from the active project session and retry."
    )
    assert not (project_root / "codex_exports").exists()


def test_missing_rollout_fails_without_claiming_success(
    session_fixture: SessionFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    session_fixture.rollout_path.unlink()

    exit_code = main(
        [
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert (
        captured.out.strip()
        == f"I couldn't read the persisted session history at {session_fixture.rollout_path}. "
        "Make sure this Codex environment can access the live session data, then retry $export."
    )
    assert not session_fixture.export_dir.exists()


def test_missing_rollout_uses_english_fallback_when_thread_language_cannot_be_detected(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    session_fixture = build_session_fixture(tmp_path)
    session_fixture.apply_initial_rollout(replacements=GERMAN_REPLACEMENTS)
    session_fixture.rollout_path.unlink()

    exit_code = main(
        [
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert (
        captured.out.strip()
        == f"I couldn't read the persisted session history at {session_fixture.rollout_path}. "
        "Make sure this Codex environment can access the live session data, then retry $export."
    )


def test_no_new_content_message_is_localized_for_german_thread(tmp_path: Path) -> None:
    session_fixture = build_session_fixture(tmp_path)
    session_fixture.apply_initial_rollout(replacements=GERMAN_REPLACEMENTS)

    export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    no_change_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    assert no_change_result.message == (
        "Es gibt seit dem letzten erfolgreichen Export noch keinen neuen Inhalt zu exportieren."
    )


def test_unreadable_checkpoint_message_is_localized_for_german_thread(tmp_path: Path) -> None:
    session_fixture = build_session_fixture(tmp_path)
    session_fixture.apply_initial_rollout(replacements=GERMAN_REPLACEMENTS)

    export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    session_fixture.sidecar_path.write_text("{}", encoding="utf-8")

    with pytest.raises(CheckpointError, match="Checkpoint-Datei"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.second_export_time,
        )


def test_export_rejects_unsafe_project_root(
    session_fixture: SessionFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import codexporter.service as service

    monkeypatch.setattr(service, "SKILL_ROOT", session_fixture.project_root)

    with pytest.raises(ProjectRootError, match="safe active project root"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.first_export_time,
        )

    assert not session_fixture.export_dir.exists()
