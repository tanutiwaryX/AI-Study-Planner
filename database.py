import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("study_planner.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            topic TEXT NOT NULL, sentiment TEXT NOT NULL, polarity REAL NOT NULL,
            word_count INTEGER NOT NULL, summary TEXT NOT NULL)""")

def save_analysis(topic, sentiment, polarity, word_count, summary):
    with get_connection() as conn:
        conn.execute("INSERT INTO analyses(topic,sentiment,polarity,word_count,summary) VALUES(?,?,?,?,?)",
                     (topic,sentiment,float(polarity),int(word_count),summary))

def get_history():
    with get_connection() as conn:
        return conn.execute("SELECT id,created_at,topic,sentiment,polarity,word_count,summary FROM analyses ORDER BY id DESC").fetchall()

def clear_history():
    with get_connection() as conn:
        conn.execute("DELETE FROM analyses")
