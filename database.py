import sqlite3
import logging

DB_PATH = "mafia_helper.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    # Можна додати таблиці для користувачів, балансів тощо
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

def get_connection():
    return sqlite3.connect(DB_PATH)

# CRUD для івентів:

def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description FROM events")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "description": r[2]} for r in rows]

def get_event(event_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description FROM events WHERE id = ?", (event_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "title": row[1], "description": row[2]}
    return None

def add_event(ev_id, title, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (id, title, description) VALUES (?, ?, ?)",
                   (ev_id, title, description))
    conn.commit()
    conn.close()

def update_event(ev_id, title, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET title = ?, description = ? WHERE id = ?",
                   (title, description, ev_id))
    conn.commit()
    conn.close()

def delete_event(ev_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (ev_id,))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Таблиця івентів
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    # Таблиця користувачів
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            banned INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            role TEXT DEFAULT 'user'
        )
    """)

    # Таблиця налаштувань (key-value)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()
    logging.info("Database initialized.")

# --- Функції для користувачів ---

def ban_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    cursor.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET banned = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_banned(user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT banned FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None and row[0] == 1

def get_user_stats(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance, wins, losses FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"balance": row[0], "wins": row[1], "losses": row[2]}
    else:
        return {"balance": 0, "wins": 0, "losses": 0}

def update_user_balance(user_id: int, delta: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (delta, user_id))
    conn.commit()
    conn.close()

def update_user_stats(user_id: int, win_increment=0, loss_increment=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    cursor.execute(
        "UPDATE users SET wins = wins + ?, losses = losses + ? WHERE user_id = ?",
        (win_increment, loss_increment, user_id)
    )
    conn.commit()
    conn.close()

# --- Функції для налаштувань ---

def set_setting(key: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_setting(key: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
