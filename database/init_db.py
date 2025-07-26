import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mafia.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Створення таблиці users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0,
        stars INTEGER DEFAULT 0,
        daily_games INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Базу даних ініціалізовано: таблиця users готова.")

if __name__ == "__main__":
    init_db()
