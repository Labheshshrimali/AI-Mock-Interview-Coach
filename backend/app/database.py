import sqlite3
import json
from datetime import datetime

DB_NAME = "interview_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            question TEXT,
            transcript TEXT,
            scores_json TEXT,
            metrics_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_session(question, transcript, scores, metrics):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interview_sessions (timestamp, question, transcript, scores_json, metrics_json)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        question,
        transcript,
        json.dumps(scores),
        json.dumps(metrics)
    ))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM interview_sessions ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
