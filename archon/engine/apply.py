import json
from pathlib import Path
from typing import Any, Dict

from archon.database import queries


PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system_prompt.json"


def apply_changes(conn, session_id: str, payload: Dict[str, Any]):
    if not payload:
        return
    proposed_ui = payload.get("ui_state", {})
    for key, value in proposed_ui.items():
        queries.set_ui_state(conn, key, json.dumps(value))

    proposed_archon_attrs = payload.get("archon_attributes", {})
    for key, value in proposed_archon_attrs.items():
        queries.set_attribute(conn, "archon_attributes", key, float(value))

    prompt_update = payload.get("system_prompt")
    if prompt_update:
        PROMPT_PATH.write_text(json.dumps(prompt_update, indent=2))
