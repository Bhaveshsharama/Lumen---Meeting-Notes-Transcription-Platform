"""
One-time migration: make meetings.owner_id nullable in SQLite.
SQLite does not support ALTER COLUMN, so we use the recreate-table approach.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fireflies.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = OFF")

cursor.executescript("""
BEGIN;

-- 1. Create new table with nullable owner_id
CREATE TABLE IF NOT EXISTS meetings_new (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id       INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title          VARCHAR NOT NULL,
    description    TEXT,
    meeting_date   DATETIME NOT NULL,
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    media_url      TEXT,
    media_type     VARCHAR DEFAULT 'audio',
    tags           JSON,
    status         VARCHAR NOT NULL DEFAULT 'ready',
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_meeting_media_type CHECK (media_type IN ('audio', 'video')),
    CONSTRAINT ck_meeting_status     CHECK (status IN ('processing', 'ready', 'failed'))
);

-- 2. Copy existing data
INSERT INTO meetings_new SELECT * FROM meetings;

-- 3. Drop old table
DROP TABLE meetings;

-- 4. Rename new table
ALTER TABLE meetings_new RENAME TO meetings;

-- 5. Recreate index
CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings (meeting_date);

COMMIT;
""")

cursor.execute("PRAGMA foreign_keys = ON")
conn.close()
print("Migration complete: meetings.owner_id is now nullable.")
