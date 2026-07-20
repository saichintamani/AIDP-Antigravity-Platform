import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "telemetry.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reproductions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            leakage_rate REAL NOT NULL,
            reviewer_stance TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_reproduction(model_name: str, leakage_rate: float, reviewer_stance: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reproductions (model_name, leakage_rate, reviewer_stance) VALUES (?, ?, ?)",
        (model_name, leakage_rate, reviewer_stance)
    )
    conn.commit()
    conn.close()

def get_aggregated_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT model_name, COUNT(*), AVG(leakage_rate)
        FROM reproductions
        GROUP BY model_name
    ''')
    rows = c.fetchall()
    conn.close()
    
    return [
        {"model": row[0], "evaluations": row[1], "mean_leakage": row[2]}
        for row in rows
    ]
