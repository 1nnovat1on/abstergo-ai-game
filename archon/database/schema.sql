-- schema.sql

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    started_at INTEGER,
    ended_at INTEGER
);

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    actor TEXT,
    content TEXT,
    created_at INTEGER
);

CREATE TABLE IF NOT EXISTS archon_attributes (
    key TEXT PRIMARY KEY,
    value REAL,
    updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS user_attributes (
    key TEXT PRIMARY KEY,
    value REAL,
    updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS ui_state (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS schema_backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schema_sql TEXT,
    created_at INTEGER
);
