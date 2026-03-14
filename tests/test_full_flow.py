from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from codexporter.cli import main
from conftest import SessionFixture, build_session_fixture

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "skills" / "export" / "scripts" / "export_skill.py"
)


def test_cli_main_success_prints_export_message_and_returns_zero(
    session_fixture: SessionFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(
        [
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
        ]
    )

    captured = capsys.readouterr()
    export_paths = sorted(session_fixture.export_dir.glob("*.md"))

    assert exit_code == 0
    assert len(export_paths) == 1
    assert (
        captured.out.strip()
        == f"Exported the current session to {export_paths[0]}. File: {export_paths[0].name}."
    )


def test_export_skill_script_runs_across_two_project_contexts(tmp_path: Path) -> None:
    first_fixture = build_session_fixture(tmp_path / "workspace-a", project_name="project-alpha")
    second_fixture = build_session_fixture(tmp_path / "workspace-b", project_name="project-beta")

    first_run = _run_script(first_fixture)
    second_run = _run_script(second_fixture)

    assert first_run.returncode == 0
    assert second_run.returncode == 0
    first_exports = sorted(first_fixture.export_dir.glob("*.md"))
    second_exports = sorted(second_fixture.export_dir.glob("*.md"))

    assert len(first_exports) == 1
    assert len(second_exports) == 1
    assert first_run.stdout.strip() == (
        f"Exported the current session to {first_exports[0]}. File: {first_exports[0].name}."
    )
    assert second_run.stdout.strip() == (
        f"Exported the current session to {second_exports[0]}. File: {second_exports[0].name}."
    )
    assert first_fixture.export_dir != second_fixture.export_dir


def _run_script(session_fixture: SessionFixture) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
