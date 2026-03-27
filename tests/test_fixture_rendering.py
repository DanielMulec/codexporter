from __future__ import annotations

import json
from pathlib import Path

from conftest import FIXTURE_ROOT, render_markdown_template, render_rollout_jsonl_template


def test_windows_path_rollout_template_renders_valid_jsonl_and_plain_markdown() -> None:
    project_root = Path(r"C:\Users\Daniel\Projekte\codexporter")

    rendered_rollout = render_rollout_jsonl_template(
        FIXTURE_ROOT / "rollout_initial.jsonl",
        project_root,
    )
    records = [json.loads(line) for line in rendered_rollout.splitlines()]

    turn_context = next(record for record in records if record["type"] == "turn_context")
    tool_call = next(
        record
        for record in records
        if record["type"] == "response_item" and record["payload"]["type"] == "function_call"
    )
    tool_arguments = json.loads(tool_call["payload"]["arguments"])

    assert turn_context["payload"]["cwd"] == str(project_root)
    assert tool_arguments["workdir"] == str(project_root)

    rendered_markdown = render_markdown_template(
        FIXTURE_ROOT / "expected" / "initial_export.md",
        project_root,
    )
    assert f"- Current working directory: {project_root}" in rendered_markdown
    markdown_arguments = rendered_markdown.split("```json\n", 1)[1].split("\n```", 1)[0]
    assert json.loads(markdown_arguments)["workdir"] == str(project_root)
