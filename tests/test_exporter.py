from __future__ import annotations

import json

import pytest

from codexporter.checkpoint import load_checkpoint
from codexporter.errors import CheckpointError
from codexporter.service import export_current_session
from conftest import SessionFixture


def test_first_export_creates_markdown_and_checkpoint(session_fixture: SessionFixture) -> None:
    result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    assert result.export_path is not None
    assert result.export_path.name == "20260313-210000-Spec-Export-Planning-1.md"
    assert (
        result.export_path.read_text(encoding="utf-8") == session_fixture.expected_initial_markdown
    )
    assert result.sidecar_path == session_fixture.sidecar_path
    assert result.sidecar_path.exists()
    assert result.message == (
        f"Exported the current session to {result.export_path}. File: {result.export_path.name}."
    )

    checkpoint = load_checkpoint(result.sidecar_path, "en")
    assert checkpoint is not None
    assert checkpoint.export_sequence == 1
    assert checkpoint.last_exported_record_index == 10
    assert checkpoint.last_exported_event_timestamp == "2026-03-13T19:00:11Z"
    assert checkpoint.last_exported_turn_id == "turn-1"
    assert checkpoint.exported_artifacts == [str(result.export_path)]


def test_second_export_is_incremental_and_keeps_prior_artifact_unchanged(
    session_fixture: SessionFixture,
) -> None:
    first_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    assert first_result.export_path is not None
    first_export_snapshot = first_result.export_path.read_text(encoding="utf-8")

    session_fixture.apply_extended_rollout()
    second_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.second_export_time,
    )

    assert second_result.export_path is not None
    assert second_result.export_path.name == "20260313-210500-Spec-Export-Planning-2.md"
    assert (
        second_result.export_path.read_text(encoding="utf-8")
        == session_fixture.expected_incremental_markdown
    )
    assert first_result.export_path.read_text(encoding="utf-8") == first_export_snapshot
    expected_message = (
        f"Created incremental export {second_result.export_path.name} "
        f"at {second_result.export_path}."
    )
    assert second_result.message == expected_message

    checkpoint = load_checkpoint(second_result.sidecar_path, "en")
    assert checkpoint is not None
    assert checkpoint.export_sequence == 2
    assert checkpoint.last_exported_record_index == 18
    assert checkpoint.last_exported_event_timestamp == "2026-03-13T19:05:06Z"
    assert checkpoint.last_exported_turn_id == "turn-2"
    assert checkpoint.exported_artifacts == [
        str(first_result.export_path),
        str(second_result.export_path),
    ]


def test_no_new_content_creates_no_new_markdown_file(session_fixture: SessionFixture) -> None:
    export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    session_fixture.apply_extended_rollout()
    export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.second_export_time,
    )

    no_change_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.second_export_time,
    )

    markdown_files = sorted(session_fixture.export_dir.glob("*.md"))
    assert no_change_result.export_path is None
    assert no_change_result.no_new_content is True
    assert (
        no_change_result.message
        == "There is no new content to export since the last successful export."
    )
    assert [path.name for path in markdown_files] == [
        "20260313-210000-Spec-Export-Planning-1.md",
        "20260313-210500-Spec-Export-Planning-2.md",
    ]


def test_corrupted_checkpoint_fails_safely(session_fixture: SessionFixture) -> None:
    first_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    assert first_result.export_path is not None
    session_fixture.sidecar_path.write_text("{not-valid-json", encoding="utf-8")
    session_fixture.apply_extended_rollout()

    with pytest.raises(CheckpointError, match="checkpoint sidecar"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.second_export_time,
        )

    markdown_files = sorted(session_fixture.export_dir.glob("*.md"))
    assert [path.name for path in markdown_files] == ["20260313-210000-Spec-Export-Planning-1.md"]
    assert (
        first_result.export_path.read_text(encoding="utf-8")
        == session_fixture.expected_initial_markdown
    )


def test_checkpoint_cursor_mismatch_fails_without_new_artifact(
    session_fixture: SessionFixture,
) -> None:
    first_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    assert first_result.export_path is not None
    sidecar_payload = json.loads(session_fixture.sidecar_path.read_text(encoding="utf-8"))
    sidecar_payload["last_exported_event_timestamp"] = "2026-03-13T19:00:10Z"
    session_fixture.sidecar_path.write_text(
        json.dumps(sidecar_payload, indent=2) + "\n", encoding="utf-8"
    )
    session_fixture.apply_extended_rollout()

    with pytest.raises(CheckpointError, match="no longer matches"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.second_export_time,
        )

    markdown_files = sorted(session_fixture.export_dir.glob("*.md"))
    assert [path.name for path in markdown_files] == ["20260313-210000-Spec-Export-Planning-1.md"]
    assert (
        first_result.export_path.read_text(encoding="utf-8")
        == session_fixture.expected_initial_markdown
    )
