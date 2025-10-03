"""
Database connection utilities.

Using SQLite for simplicity. For async usage consider databases or SQLModel/SQLAlchemy
with aiosqlite/asyncpg backends.
"""
import sqlite3
from pathlib import Path

# Resolve DB to backend/data/news.db (workspace/backend/data/news.db)
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "news.db"


def init_db():
    """Initialize a simple SQLite DB with minimal tables (synchronous placeholder)."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT,
            source TEXT
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            article_id INTEGER,
            category TEXT,
            reward REAL,
            metadata TEXT,
            timestamp TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()
