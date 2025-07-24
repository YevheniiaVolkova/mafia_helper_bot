import sqlite3
from config import DATABASE_PATH

DB_NAME = "mafia_helper.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def get_db():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        # Таблиця користувачів
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            role TEXT DEFAULT 'user',
            balance INTEGER DEFAULT 0,
            stars INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
        """)

        # Таблиця івентів
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            is_active INTEGER DEFAULT 0
        )
        """)

        # Таблиця налаштувань
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            key TEXT,
            value TEXT
        )
        """)

        conn.commit()
