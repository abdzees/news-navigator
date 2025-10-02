"""
Epsilon-greedy bandit over discrete arms (article categories).

This implementation keeps lightweight persistent state in the project's SQLite
DB (table `bandit_state`) so estimated values survive process restarts. The
persistence is optional and controlled by the `persist` flag.
"""
import random
import sqlite3
from typing import Dict, List, Any, Optional

from app.db.database import DB_PATH


class BanditAgent:
    """Simple epsilon-greedy agent where arms are category strings.

    Methods
    - select_arm() -> str
    - update(arm: str, reward: float)

    State is kept in two in-memory dicts (counts and values) and persisted to
    the DB if persist=True.
    """

    def __init__(self, arms: List[str], epsilon: float = 0.1, persist: bool = True):
        self.arms = list(arms)
        self.epsilon = float(epsilon)
        self.persist = bool(persist)

        # in-memory estimates
        self.counts: Dict[str, int] = {a: 0 for a in self.arms}
        self.values: Dict[str, float] = {a: 0.0 for a in self.arms}

        if self.persist:
            self._ensure_table()
            self._load_state()

    # ------------------ persistence helpers ------------------
    def _ensure_table(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS bandit_state (
                arm TEXT PRIMARY KEY,
                count INTEGER,
                value REAL
            )
            """
        )
        conn.commit()
        conn.close()

    def _load_state(self):
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute("SELECT arm, count, value FROM bandit_state")
        rows = c.fetchall()
        conn.close()
        for arm, count, value in rows:
            if arm in self.arms:
                self.counts[arm] = int(count)
                self.values[arm] = float(value)

    def _save_arm(self, arm: str):
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        # upsert (works on modern SQLite versions)
        c.execute(
            """
            INSERT INTO bandit_state (arm, count, value)
            VALUES (?, ?, ?)
            ON CONFLICT(arm) DO UPDATE SET count=excluded.count, value=excluded.value
            """,
            (arm, self.counts.get(arm, 0), self.values.get(arm, 0.0)),
        )
        conn.commit()
        conn.close()

    # ------------------ bandit methods ------------------
    def select_arm(self) -> str:
        """Select an arm (category) using epsilon-greedy exploration.

        Returns a category string from the set of arms.
        """
        if not self.arms:
            raise ValueError("No arms available for bandit selection")
        if random.random() < self.epsilon:
            return random.choice(self.arms)
        # exploitation: pick arm with highest estimated value
        best = max(self.arms, key=lambda a: self.values.get(a, 0.0))
        return best

    def update(self, arm: str, reward: float):
        """Update internal estimates for the given arm with observed reward."""
        if arm not in self.arms:
            # ignore unknown arms
            return
        self.counts[arm] = self.counts.get(arm, 0) + 1
        n = self.counts[arm]
        value = self.values.get(arm, 0.0)
        # incremental mean update
        new_value = value + (float(reward) - value) / n
        self.values[arm] = new_value
        if self.persist:
            self._save_arm(arm)


# Convenience singleton for the application. Call get_bandit_agent() to reuse.
_default_agent: Optional[BanditAgent] = None


def get_bandit_agent(arms: Optional[List[str]] = None, epsilon: float = 0.1, persist: bool = True) -> BanditAgent:
    """Return a module-level BanditAgent singleton.

    If an agent already exists this returns it (ignoring new arms). To create a
    separate agent, instantiate BanditAgent directly.
    """
    global _default_agent
    if _default_agent is None:
        if arms is None:
            arms = ["technology", "business", "politics", "sports", "science", "health", "entertainment"]
        _default_agent = BanditAgent(arms=arms, epsilon=epsilon, persist=persist)
    return _default_agent
