import time
from pathlib import Path


def backup_schema(conn, schema_path: Path):
    schema_sql = schema_path.read_text()
    now = int(time.time())
    conn.execute(
        "INSERT INTO schema_backups (schema_sql, created_at) VALUES (?, ?)",
        (schema_sql, now),
    )
