import json
from typing import Any, Dict

from archon.cognition.llm import call_archon
from archon.database import queries
from archon.ui.render import render_status


def run_reflection(conn, session_id: str, system_prompt: Dict[str, Any], snapshot: Dict[str, Any]):
    try:
        response = call_archon(system_prompt, snapshot)
    except Exception as exc:  # JSON or process failure
        render_status(f"LLM call failed: {exc}")
        queries.log_interaction(conn, session_id, "archon", "LLM invocation failed")
        return None

    try:
        formatted = json.dumps(response)
        queries.log_interaction(conn, session_id, "archon", formatted)
    except Exception:
        render_status("Could not log LLM response")

    return response
