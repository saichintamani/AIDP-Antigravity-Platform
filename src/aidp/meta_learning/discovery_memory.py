import sqlite3
import uuid
from typing import Any


class DiscoveryMemory:
    """
    Relational persistence layer for completed campaigns and discoveries.
    Allows the system to query past experiences (E1) to avoid repeating mistakes.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                goal TEXT,
                domain TEXT,
                eig_score REAL,
                cost_usd REAL,
                status TEXT
            )
        """)
        self.conn.commit()

    def log_campaign(
        self, goal: str, domain: str, eig_score: float, cost_usd: float, status: str
    ) -> str:
        camp_id = f"camp_{uuid.uuid4().hex[:8]}"
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO campaigns (id, goal, domain, eig_score, cost_usd, status) VALUES (?, ?, ?, ?, ?, ?)",
            (camp_id, goal, domain, eig_score, cost_usd, status),
        )
        self.conn.commit()
        return camp_id

    def retrieve_failed_campaigns(self, domain: str, max_results: int = 5) -> list[dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, goal, eig_score FROM campaigns WHERE domain = ? AND status = 'failed' ORDER BY cost_usd DESC LIMIT ?",
            (domain, max_results),
        )
        rows = cursor.fetchall()
        return [{"id": r[0], "goal": r[1], "eig_score": r[2]} for r in rows]
