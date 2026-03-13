from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "session_alpha"
PLACEHOLDER = "__PROJECT_ROOT__"
SESSION_ID = "019aaa00-bbbb-7ccc-8ddd-eeeeffff0001"
SESSION_TITLE = "Spec Export Planning"
TIMEZONE = ZoneInfo("Europe/Vienna")


@dataclass
class SessionFixture:
    project_root: Path
    codex_home: Path
    rollout_path: Path
    session_id: str
    expected_initial_markdown: str
    expected_incremental_markdown: str

    def apply_initial_rollout(self) -> None:
        _write_template(
            FIXTURE_ROOT / "rollout_initial.jsonl", self.rollout_path, self.project_root
        )

    def apply_extended_rollout(self) -> None:
        _write_template(
            FIXTURE_ROOT / "rollout_incremental.jsonl", self.rollout_path, self.project_root
        )

    @property
    def export_dir(self) -> Path:
        return self.project_root / "codex_exports"

    @property
    def sidecar_path(self) -> Path:
        return self.export_dir / f"{self.session_id}-checkpoint.json"

    @property
    def first_export_time(self) -> datetime:
        return datetime(2026, 3, 13, 21, 0, 0, tzinfo=TIMEZONE)

    @property
    def second_export_time(self) -> datetime:
        return datetime(2026, 3, 13, 21, 5, 0, tzinfo=TIMEZONE)


@pytest.fixture()
def session_fixture(tmp_path: Path) -> SessionFixture:
    project_root = tmp_path / "project-alpha"
    project_root.mkdir()
    codex_home = tmp_path / ".codex"
    rollout_path = codex_home / "sessions" / "2026" / "03" / "13" / "rollout.jsonl"
    rollout_path.parent.mkdir(parents=True)
    _create_state_db(codex_home / "state_5.sqlite", rollout_path, project_root)

    expected_initial_markdown = _read_template(
        FIXTURE_ROOT / "expected" / "initial_export.md", project_root
    )
    expected_incremental_markdown = _read_template(
        FIXTURE_ROOT / "expected" / "incremental_export.md", project_root
    )
    fixture = SessionFixture(
        project_root=project_root,
        codex_home=codex_home,
        rollout_path=rollout_path,
        session_id=SESSION_ID,
        expected_initial_markdown=expected_initial_markdown,
        expected_incremental_markdown=expected_incremental_markdown,
    )
    fixture.apply_initial_rollout()
    return fixture


def _create_state_db(state_db: Path, rollout_path: Path, project_root: Path) -> None:
    connection = sqlite3.connect(state_db)
    try:
        connection.execute(
            """
            CREATE TABLE threads (
                id TEXT PRIMARY KEY,
                rollout_path TEXT NOT NULL,
                created_at INTEGER,
                updated_at INTEGER,
                source TEXT,
                model_provider TEXT,
                cwd TEXT NOT NULL,
                title TEXT,
                sandbox_policy TEXT,
                approval_mode TEXT,
                cli_version TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO threads (
                id, rollout_path, created_at, updated_at, source, model_provider, cwd, title,
                sandbox_policy, approval_mode, cli_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                SESSION_ID,
                str(rollout_path),
                1773428400,
                1773428700,
                "vscode",
                "openai",
                str(project_root),
                SESSION_TITLE,
                '{"type":"danger-full-access"}',
                "never",
                "0.115.0-alpha.11",
            ),
        )
        connection.commit()
    finally:
        connection.close()


def _read_template(template_path: Path, project_root: Path) -> str:
    rendered = template_path.read_text(encoding="utf-8").replace(PLACEHOLDER, str(project_root))
    return rendered.rstrip("\n") + "\n"


def _write_template(template_path: Path, destination: Path, project_root: Path) -> None:
    destination.write_text(_read_template(template_path, project_root), encoding="utf-8")
