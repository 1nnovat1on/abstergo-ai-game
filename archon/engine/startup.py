import json
import os
import time
from pathlib import Path

from archon.cognition.reflection import run_reflection
from archon.database import queries
from archon.database.backup import backup_schema
from archon.database.db import connect
from archon.engine.complexity import update_complexity
from archon.engine.apply import apply_changes
from archon.ui.render import render_status, render_thoughts
from archon.ui.layout import build_snapshot_view
from archon.sound.synth import tone


PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "system_prompt.json"


def get_disk_usage():
    stats = os.statvfs(".")
    used = (stats.f_blocks - stats.f_bfree) * stats.f_frsize
    total = stats.f_blocks * stats.f_frsize
    return {
        "used": used,
        "total": total,
        "percent": (used / total * 100) if total else 0,
    }


def bootstrap():
    conn = connect()
    queries.initialize(conn)
    backup_schema(conn, PROMPT_PATH.parents[1] / "database" / "schema.sql")

    session_id = queries.create_session(conn)
    render_status("Session initialized")

    complexity = update_complexity(conn)
    effective_complexity = complexity ** 2

    system_prompt = json.loads(PROMPT_PATH.read_text())

    snapshot = {
        "complexity": complexity,
        "effective_complexity": effective_complexity,
        "storage_bytes": get_disk_usage(),
        "archon_attributes": queries.read_archon_attrs(conn),
        "ui_state": queries.read_ui_state(conn),
    }

    render_status("Calling DeepSeek-R1 via Ollama...")
    thoughts = run_reflection(conn, session_id, system_prompt, snapshot)
    if thoughts:
        render_thoughts(json.dumps(thoughts, indent=2))
        apply_changes(conn, session_id, thoughts.get("proposed_changes", {}))
    else:
        render_thoughts("{}")

    tone(freq=144, dur=120)

    def status_supplier():
        disk = get_disk_usage()
        snapshot_state = build_snapshot_view(complexity, effective_complexity, disk)
        return snapshot_state

    from archon.engine.loop import idle_loop

    idle_loop(status_supplier)
