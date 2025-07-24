import sqlite3

def get_db():
    return sqlite3.connect("data.db")

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                user_id TEXT PRIMARY KEY,
                nickname TEXT,
                games_today INTEGER DEFAULT 0,
                wins_today INTEGER DEFAULT 0,
                currency INTEGER DEFAULT 0,
                stars INTEGER DEFAULT 0,
                silence INTEGER DEFAULT 0,
                reveal INTEGER DEFAULT 0
            );
        """)
