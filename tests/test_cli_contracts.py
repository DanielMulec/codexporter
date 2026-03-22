from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from codexporter.cli import main
from codexporter.service import export_current_session
from conftest import SessionFixture, build_session_fixture, insert_thread_record

ALTERNATE_SESSION_ID = "019aaa00-bbbb-7ccc-8ddd-eeeeffff0002"
GERMAN_REPLACEMENTS = {
    "Please outline the implementation plan for the exporter.": (
        "Kannst du das bitte jetzt exportieren, danke?"
    ),
    "Please export the newly added tests as well.": (
        "Kannst du das bitte jetzt erneut exportieren, danke?"
    ),
}


def test_cli_main_localizes_no_new_content_for_german_thread(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    session_fixture = build_session_fixture(tmp_path)
    session_fixture.apply_initial_rollout(replacements=GERMAN_REPLACEMENTS)
    export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    exit_code = main(
        [
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert (
        captured.out.strip()
        == "Es gibt seit dem letzten erfolgreichen Export noch keinen neuen Inhalt zu exportieren."
    )


def test_cli_main_localizes_checkpoint_failure_for_german_thread(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    session_fixture = build_session_fixture(tmp_path)
    session_fixture.apply_initial_rollout(replacements=GERMAN_REPLACEMENTS)
    export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    session_fixture.sidecar_path.write_text("{}", encoding="utf-8")

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
    assert "Checkpoint-Datei" in captured.out.strip()


def test_cli_main_fails_closed_when_same_workspace_is_ambiguous(
    session_fixture: SessionFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with sqlite3.connect(session_fixture.state_db_path) as connection:
        insert_thread_record(
            connection,
            session_id=ALTERNATE_SESSION_ID,
            rollout_path=session_fixture.rollout_path,
            cwd=session_fixture.project_root,
            created_at=1773428401,
            updated_at=1773429700,
            title="Ambiguous Same-Workspace Session",
        )
        connection.commit()

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
    assert "more than one Codex session" in captured.out.strip()
    assert not session_fixture.export_dir.exists()


def test_cli_main_prefers_runtime_thread_id_over_same_workspace_heuristics(
    session_fixture: SessionFixture,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with sqlite3.connect(session_fixture.state_db_path) as connection:
        insert_thread_record(
            connection,
            session_id=ALTERNATE_SESSION_ID,
            rollout_path=session_fixture.rollout_path,
            cwd=session_fixture.project_root,
            created_at=1773428401,
            updated_at=1773429700,
            title="Newer Same-Workspace Session",
        )
        connection.commit()

    monkeypatch.setenv("CODEX_THREAD_ID", session_fixture.session_id)
    exit_code = main(
        [
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Exported the current session" in captured.out.strip()
    assert session_fixture.sidecar_path.exists()
    assert not session_fixture.export_dir.joinpath(
        f"{ALTERNATE_SESSION_ID}-checkpoint.json"
    ).exists()
