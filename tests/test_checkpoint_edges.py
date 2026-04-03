from __future__ import annotations

import json
from pathlib import Path

import pytest

from codexporter.checkpoint import REQUIRED_FIELDS, SCHEMA_VERSION
from codexporter.errors import CheckpointError, ExporterError
from codexporter.json_utils import load_json_object
from codexporter.service import export_current_session
from conftest import SessionFixture, json_int_field, json_string_list_field, json_text_field


def test_sidecar_json_contains_required_v1_fields(session_fixture: SessionFixture) -> None:
    result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    payload = load_json_object(result.sidecar_path.read_text(encoding="utf-8"))

    assert set(payload) == REQUIRED_FIELDS
    assert json_int_field(payload, "schema_version") == SCHEMA_VERSION
    assert json_text_field(payload, "session_id") == session_fixture.session_id
    assert json_text_field(payload, "session_name") == "Spec Export Planning"
    assert json_int_field(payload, "export_sequence") == 1
    assert json_string_list_field(payload, "exported_artifacts") == [str(result.export_path)]


def test_incomplete_checkpoint_sidecar_fails_safely(session_fixture: SessionFixture) -> None:
    first_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    session_fixture.sidecar_path.write_text("{}", encoding="utf-8")
    session_fixture.apply_extended_rollout()

    with pytest.raises(CheckpointError, match="checkpoint sidecar"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.second_export_time,
        )

    markdown_files = sorted(session_fixture.export_dir.glob("*.md"))
    assert [path.name for path in markdown_files] == ["20260313-200000-Spec-Export-Planning-1.md"]
    assert (
        first_result.export_path is not None
        and first_result.export_path.read_text(encoding="utf-8")
        == session_fixture.expected_initial_markdown
    )


def test_boolean_checkpoint_numeric_fields_fail_safely(session_fixture: SessionFixture) -> None:
    first_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    sidecar_payload = load_json_object(session_fixture.sidecar_path.read_text(encoding="utf-8"))
    sidecar_payload["export_sequence"] = True
    sidecar_payload["last_exported_record_index"] = True
    session_fixture.sidecar_path.write_text(
        json.dumps(sidecar_payload, indent=2) + "\n", encoding="utf-8"
    )
    session_fixture.apply_extended_rollout()

    with pytest.raises(CheckpointError, match="checkpoint sidecar"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.second_export_time,
        )

    markdown_files = sorted(session_fixture.export_dir.glob("*.md"))
    assert [path.name for path in markdown_files] == ["20260313-200000-Spec-Export-Planning-1.md"]
    assert (
        first_result.export_path is not None
        and first_result.export_path.read_text(encoding="utf-8")
        == session_fixture.expected_initial_markdown
    )


def test_failed_write_keeps_existing_checkpoint_state(
    session_fixture: SessionFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )
    original_sidecar_payload = session_fixture.sidecar_path.read_text(encoding="utf-8")
    session_fixture.apply_extended_rollout()

    original_replace = Path.replace

    def failing_replace(self: Path, target: Path | str) -> Path:
        if Path(target) == session_fixture.sidecar_path:
            raise OSError("simulated replace failure")
        return original_replace(self, target)

    monkeypatch.setattr(Path, "replace", failing_replace)

    with pytest.raises(ExporterError, match="write the export artifacts safely"):
        export_current_session(
            project_root=session_fixture.project_root,
            codex_home=session_fixture.codex_home,
            now=session_fixture.second_export_time,
        )

    markdown_files = sorted(session_fixture.export_dir.glob("*.md"))
    assert [path.name for path in markdown_files] == ["20260313-200000-Spec-Export-Planning-1.md"]
    assert session_fixture.sidecar_path.read_text(encoding="utf-8") == original_sidecar_payload
    assert original_result.export_path is not None
