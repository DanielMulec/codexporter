from __future__ import annotations

import json

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | dict[str, "JsonValue"] | list["JsonValue"]
type JsonObject = dict[str, JsonValue]


def load_json_value(text: str) -> JsonValue:
    # The stdlib stub returns Any here, so contain that escape hatch in one
    # boundary helper and validate the decoded shape immediately at call sites.
    return json.loads(text)  # type: ignore[misc,no-any-return]


def load_json_object(text: str) -> JsonObject:
    value = load_json_value(text)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object.")
    return {str(key): item for key, item in value.items()}
