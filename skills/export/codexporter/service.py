from __future__ import annotations

import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from codexporter.checkpoint import (
    build_checkpoint,
    checkpoint_to_json,
    load_checkpoint,
    sidecar_path_for_session,
    validate_checkpoint,
)
from codexporter.errors import ExporterError, ProjectRootError, RolloutAccessError
from codexporter.messages import (
    no_exportable_content_message,
    no_new_content_message,
    success_message,
    unsafe_project_root_message,
    write_failure_message,
)
from codexporter.models import ExportEntry, ExportMode, ExportResult, Language
from codexporter.renderer import render_markdown
from codexporter.rollout_parser import parse_rollout
from codexporter.session_store import discover_current_thread, resolve_codex_home

SKILL_ROOT = Path(__file__).resolve().parents[1]


def export_current_session(
    project_root: Path,
    codex_home: Path | None = None,
    now: datetime | None = None,
    session_id: str | None = None,
) -> ExportResult:
    invocation_root = project_root.expanduser().resolve()
    _ensure_safe_project_root(invocation_root)

    current_session_id = _resolve_session_id(session_id)
    thread = discover_current_thread(
        invocation_root,
        resolve_codex_home(codex_home),
        session_id=current_session_id,
    )
    _ensure_safe_project_root(thread.cwd)

    parsed = parse_rollout(thread)
    export_dir = thread.cwd / "codex_exports"
    sidecar_path = sidecar_path_for_session(export_dir, parsed.session.session_id)
    checkpoint = load_checkpoint(sidecar_path, parsed.session.language)

    export_entries: tuple[ExportEntry, ...]
    export_mode: ExportMode
    if checkpoint is None:
        export_entries = parsed.entries
        export_mode = "full"
    else:
        validate_checkpoint(checkpoint, parsed, sidecar_path)
        export_entries = tuple(
            entry
            for entry in parsed.entries
            if entry.source_index > checkpoint.last_exported_record_index
        )
        export_mode = "incremental"

    if not export_entries:
        if checkpoint is None:
            raise RolloutAccessError(no_exportable_content_message(parsed.session.language))
        return ExportResult(
            message=no_new_content_message(parsed.session.language),
            project_root=thread.cwd,
            export_path=None,
            sidecar_path=sidecar_path,
            export_sequence=checkpoint.export_sequence,
            export_mode=export_mode,
            no_new_content=True,
        )

    exported_at = now or datetime.now().astimezone()
    sequence = (checkpoint.export_sequence + 1) if checkpoint is not None else 1
    export_path = export_dir / _build_export_filename(
        exported_at, parsed.session.session_name, parsed.session.session_id, sequence
    )
    if export_path.exists():
        raise ExporterError(write_failure_message(export_dir, parsed.session.language))

    checkpoint_state = build_checkpoint(
        previous=checkpoint,
        session=parsed.session,
        last_entry=export_entries[-1],
        export_path=export_path,
        exported_at=exported_at,
    )
    markdown = render_markdown(
        session=parsed.session,
        entries=export_entries,
        export_sequence=sequence,
        export_mode=export_mode,
        exported_at=exported_at,
        sidecar_path=sidecar_path,
    )
    _write_export_pair(
        export_dir=export_dir,
        export_path=export_path,
        markdown=markdown,
        sidecar_path=sidecar_path,
        sidecar_payload=checkpoint_to_json(checkpoint_state),
        language=parsed.session.language,
    )
    return ExportResult(
        message=success_message(export_path, export_mode == "incremental", parsed.session.language),
        project_root=thread.cwd,
        export_path=export_path,
        sidecar_path=sidecar_path,
        export_sequence=sequence,
        export_mode=export_mode,
        no_new_content=False,
    )


def _resolve_session_id(explicit_session_id: str | None) -> str | None:
    if explicit_session_id is not None and explicit_session_id.strip():
        return explicit_session_id.strip()
    env_session_id = os.environ.get("CODEX_THREAD_ID")
    if env_session_id is not None and env_session_id.strip():
        return env_session_id.strip()
    return None


def _ensure_safe_project_root(project_root: Path) -> None:
    if project_root == SKILL_ROOT or project_root.is_relative_to(SKILL_ROOT):
        raise ProjectRootError(unsafe_project_root_message(project_root))


def _build_export_filename(
    exported_at: datetime,
    session_name: str | None,
    session_id: str,
    sequence: int,
) -> str:
    slug = _slugify(session_name or session_id)
    timestamp = exported_at.strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{slug}-{sequence}.md"


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    compact = re.sub(r"[^A-Za-z0-9]+", "-", normalized).strip("-")
    compact = re.sub(r"-{2,}", "-", compact)
    if not compact:
        return "session"
    return compact[:60]


def _write_export_pair(
    export_dir: Path,
    export_path: Path,
    markdown: str,
    sidecar_path: Path,
    sidecar_payload: str,
    language: Language,
) -> None:
    export_dir.mkdir(parents=True, exist_ok=True)
    export_temp = export_dir / f".{export_path.name}.{uuid4().hex}.tmp"
    sidecar_temp = export_dir / f".{sidecar_path.name}.{uuid4().hex}.tmp"
    try:
        export_temp.write_text(markdown, encoding="utf-8")
        sidecar_temp.write_text(sidecar_payload, encoding="utf-8")
        export_temp.replace(export_path)
        sidecar_temp.replace(sidecar_path)
    except OSError as exc:
        for temporary_path in (export_temp, sidecar_temp):
            if temporary_path.exists():
                temporary_path.unlink(missing_ok=True)
        if export_path.exists():
            export_path.unlink(missing_ok=True)
        raise ExporterError(write_failure_message(export_dir, language)) from exc
