import time
import uuid
from pathlib import Path
from typing import Dict, Any

from .db import connect


SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def initialize(conn=None):
    needs_close = False
    if conn is None:
        conn = connect()
        needs_close = True
    schema_sql = SCHEMA_PATH.read_text()
    conn.executescript(schema_sql)
    if needs_close:
        conn.close()


def create_session(conn) -> str:
    session_id = str(uuid.uuid4())
    now = int(time.time())
    conn.execute(
        "INSERT INTO sessions (id, started_at, ended_at) VALUES (?, ?, ?)",
        (session_id, now, None),
    )
    return session_id


def end_session(conn, session_id: str):
    now = int(time.time())
    conn.execute(
        "UPDATE sessions SET ended_at=? WHERE id=?",
        (now, session_id),
    )


def log_interaction(conn, session_id: str, actor: str, content: str):
    now = int(time.time())
    conn.execute(
        "INSERT INTO interactions (session_id, actor, content, created_at) VALUES (?, ?, ?, ?)",
        (session_id, actor, content, now),
    )


def read_archon_attrs(conn) -> Dict[str, Any]:
    cur = conn.execute("SELECT key, value FROM archon_attributes")
    return {k: v for k, v in cur.fetchall()}


def read_ui_state(conn) -> Dict[str, Any]:
    cur = conn.execute("SELECT key, value FROM ui_state")
    return {k: v for k, v in cur.fetchall()}


def set_ui_state(conn, key: str, value: str):
    now = int(time.time())
    conn.execute(
        "INSERT INTO ui_state (key, value, updated_at) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (key, value, now),
    )


def set_attribute(conn, table: str, key: str, value: float):
    now = int(time.time())
    conn.execute(
        f"INSERT INTO {table} (key, value, updated_at) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (key, value, now),
    )
