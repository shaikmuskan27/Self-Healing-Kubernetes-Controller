import sqlite3
import os
from datetime import datetime
import json

DB_PATH = os.getenv("DB_PATH", "incidents.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            app_name TEXT NOT NULL,
            diagnostic TEXT NOT NULL,
            proposed_fix TEXT NOT NULL,
            pr_url TEXT,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_incident(app_name, diagnostic, proposed_fix, pr_url, status="Resolved"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat() + "Z"
    cursor.execute('''
        INSERT INTO incidents (timestamp, app_name, diagnostic, proposed_fix, pr_url, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, app_name, diagnostic, proposed_fix, pr_url, status))
    conn.commit()
    conn.close()

def get_incidents():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM incidents ORDER BY timestamp DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
