import sqlite3
from config import config


def get_connection():
    return sqlite3.connect(config.DATABASE_PATH)


def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                is_banned BOOLEAN DEFAULT 0,
                role TEXT DEFAULT 'user',
                balance INTEGER DEFAULT 0,
                stars INTEGER DEFAULT 0,
                daily_games INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        conn.commit()


# EVENTS CRUD

def get_all_events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_event(ev_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (ev_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_event(ev_id, title, description):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (id, name, description) VALUES (?, ?, ?)",
        (ev_id, title, description)
    )
    conn.commit()
    conn.close()

def update_event(ev_id, title, description):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE events SET name = ?, description = ? WHERE id = ?",
        (title, description, ev_id)
    )
    conn.commit()
    conn.close()

def delete_event(ev_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (ev_id,))
    conn.commit()
    conn.close()


# USERS MANAGEMENT

def ban_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_banned = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_banned(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row["is_banned"]) if row else False


# USER STATS AND BALANCE

def get_user_stats(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance, wins, losses FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    else:
        return {"balance": 0, "wins": 0, "losses": 0}

def update_user_balance(user_id, amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        new_balance = row["balance"] + amount
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    conn.close()

def update_user_stats(user_id, wins=0, losses=0):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT wins, losses FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        new_wins = row["wins"] + wins
        new_losses = row["losses"] + losses
        cursor.execute("UPDATE users SET wins = ?, losses = ? WHERE user_id = ?", (new_wins, new_losses, user_id))
    else:
        cursor.execute("INSERT INTO users (user_id, wins, losses) VALUES (?, ?, ?)", (user_id, wins, losses))
    conn.commit()
    conn.close()


# SETTINGS

def set_setting(key, value):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_setting(key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row["value"] if row else None
