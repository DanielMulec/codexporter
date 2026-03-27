from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

EntryKind = Literal["assistant", "commentary", "event", "tool_call", "tool_output", "user"]
ExportMode = Literal["full", "incremental"]
Language = Literal["de", "en"]
RenderProfile = Literal["full", "compact"]


@dataclass(frozen=True)
class ThreadRecord:
    session_id: str
    rollout_path: Path
    created_at: datetime | None
    updated_at: datetime | None
    cwd: Path
    title: str | None
    source: str | None
    model_provider: str | None
    cli_version: str | None
    approval_mode: str | None
    sandbox_policy: str | None


@dataclass(frozen=True)
class ExportEntry:
    source_index: int
    kind: EntryKind
    timestamp: datetime | None
    turn_id: str | None
    text: str | None = None
    tool_name: str | None = None
    arguments: str | None = None
    output: str | None = None
    event_type: str | None = None
    call_id: str | None = None


@dataclass(frozen=True)
class SessionInfo:
    session_id: str
    session_name: str | None
    session_started_at: datetime | None
    cwd: Path
    source: str | None
    originator: str | None
    model: str | None
    model_provider: str | None
    cli_version: str | None
    timezone_name: str | None
    approval_policy: str | None
    sandbox_policy: str | None
    language: Language


@dataclass(frozen=True)
class ParsedRollout:
    session: SessionInfo
    entries: tuple[ExportEntry, ...]
    entry_index: dict[int, ExportEntry]


@dataclass(frozen=True)
class CheckpointState:
    schema_version: int
    session_id: str
    session_name: str | None
    export_sequence: int
    last_exported_record_index: int
    last_exported_event_timestamp: str | None
    last_exported_turn_id: str | None
    exported_artifacts: list[str]
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "session_id": self.session_id,
            "session_name": self.session_name,
            "export_sequence": self.export_sequence,
            "last_exported_record_index": self.last_exported_record_index,
            "last_exported_event_timestamp": self.last_exported_event_timestamp,
            "last_exported_turn_id": self.last_exported_turn_id,
            "exported_artifacts": self.exported_artifacts,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass(frozen=True)
class ExportResult:
    message: str
    project_root: Path
    export_path: Path | None
    sidecar_path: Path
    export_sequence: int
    export_mode: ExportMode
    render_profile: RenderProfile
    no_new_content: bool
