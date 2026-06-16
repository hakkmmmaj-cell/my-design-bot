import sqlite3
from config import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        joined_at TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        url TEXT,
        type TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username, date):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
              (user_id, username, date))
    conn.commit()
    conn.close()


def add_download(user_id, url, type_, date):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO downloads (user_id, url, type, date) VALUES (?, ?, ?, ?)",
              (user_id, url, type_, date))
    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    downloads = c.execute("SELECT COUNT(*) FROM downloads").fetchone()[0]

    conn.close()
    return users, downloads
