from __future__ import annotations

import sqlite3

import pytest

from codexporter.errors import SessionDiscoveryError
from codexporter.service import export_current_session
from codexporter.session_store import discover_current_thread
from conftest import SessionFixture, insert_thread_record

ALTERNATE_SESSION_ID = "019aaa00-bbbb-7ccc-8ddd-eeeeffff0002"
MISMATCHED_SESSION_ID = "019aaa00-bbbb-7ccc-8ddd-eeeeffff0003"


def test_export_prefers_runtime_thread_id_over_newer_same_workspace_match(
    session_fixture: SessionFixture,
    monkeypatch: pytest.MonkeyPatch,
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
    result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    assert result.sidecar_path.name == f"{session_fixture.session_id}-checkpoint.json"
    assert result.export_path is not None
    assert "Exported the current session" in result.message


def test_discover_current_thread_accepts_windows_extended_path_for_targeted_session(
    session_fixture: SessionFixture,
) -> None:
    windows_cwd = r"\\?\C:\projekte\AI\sonstiges\SKILLS"
    with sqlite3.connect(session_fixture.state_db_path) as connection:
        connection.execute("DELETE FROM threads")
        insert_thread_record(
            connection,
            session_id=session_fixture.session_id,
            rollout_path=session_fixture.rollout_path,
            cwd=windows_cwd,
            created_at=1773428400,
            updated_at=1773428700,
            title="Windows Session",
        )
        connection.commit()

    thread = discover_current_thread(
        r"C:\projekte\AI\sonstiges\SKILLS",
        session_fixture.codex_home,
        session_id=session_fixture.session_id,
    )

    assert thread.session_id == session_fixture.session_id


def test_export_fails_when_targeted_session_points_to_different_workspace(
    session_fixture: SessionFixture,
) -> None:
    other_project_root = session_fixture.project_root.parent / "project-beta"
    other_project_root.mkdir()
    with sqlite3.connect(session_fixture.state_db_path) as connection:
        insert_thread_record(
            connection,
            session_id=MISMATCHED_SESSION_ID,
            rollout_path=session_fixture.rollout_path,
            cwd=other_project_root,
            created_at=1773428402,
            updated_at=1773429800,
            title="Other Workspace Session",
        )
        connection.commit()

    with pytest.raises(SessionDiscoveryError, match="belongs to"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.first_export_time,
            session_id=MISMATCHED_SESSION_ID,
        )

    assert not session_fixture.export_dir.exists()


def test_export_fails_closed_when_multiple_sessions_match_same_workspace(
    session_fixture: SessionFixture,
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

    with pytest.raises(SessionDiscoveryError, match="more than one Codex session"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.first_export_time,
        )

    assert not session_fixture.export_dir.exists()
