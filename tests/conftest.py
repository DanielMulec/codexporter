from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pytest

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "session_alpha"
PLACEHOLDER = "__PROJECT_ROOT__"
SESSION_ID = "019aaa00-bbbb-7ccc-8ddd-eeeeffff0001"
SESSION_TITLE = "Spec Export Planning"
TIMEZONE = UTC


@dataclass
class SessionFixture:
    project_root: Path
    codex_home: Path
    rollout_path: Path
    session_id: str
    expected_initial_markdown: str
    expected_incremental_markdown: str

    def apply_initial_rollout(self, replacements: Mapping[str, str] | None = None) -> None:
        _write_rollout_template(
            FIXTURE_ROOT / "rollout_initial.jsonl",
            self.rollout_path,
            self.project_root,
            replacements,
        )

    def apply_extended_rollout(self, replacements: Mapping[str, str] | None = None) -> None:
        _write_rollout_template(
            FIXTURE_ROOT / "rollout_incremental.jsonl",
            self.rollout_path,
            self.project_root,
            replacements,
        )

    @property
    def export_dir(self) -> Path:
        return self.project_root / "codex_exports"

    @property
    def sidecar_path(self) -> Path:
        return self.export_dir / f"{self.session_id}-checkpoint.json"

    @property
    def state_db_path(self) -> Path:
        return self.codex_home / "state_5.sqlite"

    @property
    def first_export_time(self) -> datetime:
        return datetime(2026, 3, 13, 20, 0, 0, tzinfo=TIMEZONE)

    @property
    def second_export_time(self) -> datetime:
        return datetime(2026, 3, 13, 20, 5, 0, tzinfo=TIMEZONE)


@pytest.fixture()
def session_fixture(tmp_path: Path) -> SessionFixture:
    return build_session_fixture(tmp_path)


@pytest.fixture(autouse=True)
def clear_codex_thread_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)


def build_session_fixture(base_dir: Path, project_name: str = "project-alpha") -> SessionFixture:
    base_dir.mkdir(parents=True, exist_ok=True)
    project_root = base_dir / project_name
    project_root.mkdir()
    codex_home = base_dir / ".codex"
    rollout_path = codex_home / "sessions" / "2026" / "03" / "13" / "rollout.jsonl"
    rollout_path.parent.mkdir(parents=True)
    _create_state_db(codex_home / "state_5.sqlite", rollout_path, project_root)

    expected_initial_markdown = render_markdown_template(
        FIXTURE_ROOT / "expected" / "initial_export.md", project_root
    )
    expected_incremental_markdown = render_markdown_template(
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
        insert_thread_record(
            connection,
            session_id=SESSION_ID,
            rollout_path=rollout_path,
            cwd=project_root,
            created_at=1773428400,
            updated_at=1773428700,
            title=SESSION_TITLE,
        )
        connection.commit()
    finally:
        connection.close()


def insert_thread_record(
    connection: sqlite3.Connection,
    *,
    session_id: str,
    rollout_path: Path,
    cwd: Path | str,
    created_at: int,
    updated_at: int,
    title: str | None,
    source: str = "vscode",
    model_provider: str = "openai",
    sandbox_policy: str = '{"type":"danger-full-access"}',
    approval_mode: str = "never",
    cli_version: str = "0.115.0-alpha.11",
) -> None:
    connection.execute(
        """
        INSERT INTO threads (
            id, rollout_path, created_at, updated_at, source, model_provider, cwd, title,
            sandbox_policy, approval_mode, cli_version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            str(rollout_path),
            created_at,
            updated_at,
            source,
            model_provider,
            str(cwd),
            title,
            sandbox_policy,
            approval_mode,
            cli_version,
        ),
    )


def render_markdown_template(
    template_path: Path,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> str:
    rendered = _render_markdown_template_content(
        template_path.read_text(encoding="utf-8"),
        project_root,
        replacements,
    )
    return rendered.rstrip("\n") + "\n"


def render_rollout_jsonl_template(
    template_path: Path,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> str:
    rendered_lines: list[str] = []
    for line in template_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        rendered_record = _replace_nested_string_values(record, project_root, replacements)
        rendered_lines.append(
            json.dumps(rendered_record, ensure_ascii=False, separators=(",", ":"))
        )
    return "\n".join(rendered_lines).rstrip("\n") + "\n"


def _write_rollout_template(
    template_path: Path,
    destination: Path,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> None:
    destination.write_text(
        render_rollout_jsonl_template(template_path, project_root, replacements), encoding="utf-8"
    )


def _replace_nested_string_values(
    value: object,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> object:
    if isinstance(value, str):
        return _replace_string_values(value, project_root, replacements)
    if isinstance(value, list):
        return [_replace_nested_string_values(item, project_root, replacements) for item in value]
    if isinstance(value, dict):
        return {
            key: _replace_nested_string_values(item, project_root, replacements)
            for key, item in value.items()
        }
    return value


def _replace_string_values(
    value: str,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> str:
    nested_json = _reencode_nested_json_string(value, project_root, replacements)
    if nested_json is not None:
        return nested_json

    return _replace_plain_string_values(value, project_root, replacements)


def _replace_plain_string_values(
    value: str,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> str:
    rendered = value.replace(PLACEHOLDER, str(project_root))
    if replacements is not None:
        for original, replacement in replacements.items():
            rendered = rendered.replace(original, replacement)
    return rendered


def _reencode_nested_json_string(
    value: str,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> str | None:
    stripped = value.strip()
    if not stripped.startswith(("{", "[")):
        return None

    try:
        nested_payload = json.loads(value)
    except json.JSONDecodeError:
        return None

    rendered_payload = _replace_nested_string_values(nested_payload, project_root, replacements)
    return json.dumps(rendered_payload, ensure_ascii=False, separators=(",", ":"))


def _render_markdown_template_content(
    markdown: str,
    project_root: Path,
    replacements: Mapping[str, str] | None = None,
) -> str:
    lines = markdown.splitlines()
    rendered_lines: list[str] = []
    in_json_fence = False
    fence_lines: list[str] = []

    for line in lines:
        if not in_json_fence:
            if line == "```json":
                rendered_lines.append(line)
                in_json_fence = True
                fence_lines = []
            else:
                rendered_lines.append(
                    _replace_plain_string_values(line, project_root, replacements)
                )
            continue

        if line == "```":
            try:
                parsed_payload = json.loads("\n".join(fence_lines))
            except json.JSONDecodeError:
                rendered_lines.extend(
                    _replace_plain_string_values(block_line, project_root, replacements)
                    for block_line in fence_lines
                )
            else:
                rendered_payload = _replace_nested_string_values(
                    parsed_payload, project_root, replacements
                )
                rendered_lines.extend(
                    json.dumps(rendered_payload, indent=2, sort_keys=True).splitlines()
                )
            rendered_lines.append(line)
            in_json_fence = False
            fence_lines = []
            continue

        fence_lines.append(line)

    if in_json_fence:
        rendered_lines.extend(
            _replace_plain_string_values(block_line, project_root, replacements)
            for block_line in fence_lines
        )

    return "\n".join(rendered_lines)
