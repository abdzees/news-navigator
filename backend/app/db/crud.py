"""
CRUD utilities for the SQLite database (synchronous placeholders).

Replace with async implementations or integrate SQLModel/SQLAlchemy for production.
"""
import sqlite3
from typing import List, Dict, Any
from .database import DB_PATH


def list_articles() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, title, description, url, source FROM articles ORDER BY id DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_article(article_id: int) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, title, description, url, source FROM articles WHERE id = ?", (article_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def insert_feedback(user_id: str, article_id: int, reward: float, metadata: str = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user_id, article_id, reward, metadata) VALUES (?, ?, ?, ?)",
              (user_id, article_id, reward, metadata))
    conn.commit()
    conn.close()
