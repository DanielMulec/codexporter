from __future__ import annotations

from pathlib import Path

from codexporter.json_utils import load_json_object
from conftest import (
    FIXTURE_ROOT,
    json_object_field,
    json_text_field,
    load_json_lines,
    render_markdown_template,
    render_rollout_jsonl_template,
)


def test_windows_path_rollout_template_renders_valid_jsonl_and_plain_markdown() -> None:
    project_root = Path(r"C:\Users\Daniel\Projekte\codexporter")

    rendered_rollout = render_rollout_jsonl_template(
        FIXTURE_ROOT / "rollout_initial.jsonl",
        project_root,
    )
    records = load_json_lines(rendered_rollout)

    turn_context = next(
        record for record in records if json_text_field(record, "type") == "turn_context"
    )
    tool_call = next(
        record
        for record in records
        if json_text_field(record, "type") == "response_item"
        and json_text_field(json_object_field(record, "payload"), "type") == "function_call"
    )
    tool_arguments = load_json_object(
        json_text_field(json_object_field(tool_call, "payload"), "arguments")
    )

    assert json_text_field(json_object_field(turn_context, "payload"), "cwd") == str(project_root)
    assert json_text_field(tool_arguments, "workdir") == str(project_root)

    rendered_markdown = render_markdown_template(
        FIXTURE_ROOT / "expected" / "initial_export.md",
        project_root,
    )
    assert f"- Current working directory: {project_root}" in rendered_markdown
    markdown_arguments = rendered_markdown.split("```json\n", 1)[1].split("\n```", 1)[0]
    assert json_text_field(load_json_object(markdown_arguments), "workdir") == str(project_root)
