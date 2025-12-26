import time


def update_complexity(conn):
    now = int(time.time())
    cur = conn.cursor()
    cur.execute("SELECT value, updated_at FROM archon_attributes WHERE key='complexity_level'")
    row = cur.fetchone()

    if not row:
        cur.execute(
            "INSERT INTO archon_attributes VALUES (?, ?, ?)",
            ("complexity_level", 0.03, now)
        )
        return 0.03

    value, last = row
    if now - last > 86400:
        value += 0.03
        cur.execute(
            "UPDATE archon_attributes SET value=?, updated_at=? WHERE key='complexity_level'",
            (value, now)
        )
    return value
