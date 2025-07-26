import sqlite3
from database.db import get_connection
import logging

logger = logging.getLogger(__name__)

# 🧠 Отримати користувача за ID
async def get_user_by_id(user_id: int) -> dict | None:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# 👤 Створити або оновити користувача
async def get_or_create_user(user_id: int, username: str = ""):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        # Оновити username, якщо він змінився і не пустий
        if username and user[1] != username:
            cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            logger.info(f"Оновлено username для user_id={user_id} на {username}")
    else:
        cursor.execute("""
            INSERT INTO users 
            (user_id, username, balance, stars, daily_games, wins, losses) 
            VALUES (?, ?, 0, 0, 0, 0, 0)
        """, (user_id, username))
        logger.info(f"Створено нового користувача user_id={user_id} username={username}")

    conn.commit()
    conn.close()

# 📋 Отримати всіх користувачів
async def get_all_users() -> list[dict]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ⭐ Отримати суму всіх зірок у чаті
async def get_chat_stars_balance() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(stars) FROM users")
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0

# 💰 Оновити баланс бабідонів користувача
async def update_user_balance(user_id: int, amount: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

# ⭐ Оновити кількість зірок Telegram
async def update_user_stars(user_id: int, stars: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET stars = stars + ? WHERE user_id = ?", (stars, user_id))
    conn.commit()
    conn.close()

# ✅ Додати перемогу
async def increment_user_wins(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET wins = wins + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# ❌ Додати поразку
async def increment_user_losses(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET losses = losses + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# 🎮 Збільшити кількість ігор за день
async def increment_daily_games(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET daily_games = daily_games + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# 🎯 Оновити результат гри
async def update_game_result_by_id(user_id: int, win: bool):
    conn = get_connection()
    cursor = conn.cursor()
    if win:
        cursor.execute("""
            UPDATE users 
            SET wins = wins + 1, balance = balance + 10, daily_games = daily_games + 1
            WHERE user_id = ?
        """, (user_id,))
        logger.info(f"Оновлено перемогу для user_id={user_id}: +1 win, +10 balance, +1 daily_games")
    else:
        cursor.execute("""
            UPDATE users
            SET losses = losses + 1, daily_games = daily_games + 1
            WHERE user_id = ?
        """, (user_id,))
        logger.info(f"Оновлено поразку для user_id={user_id}: +1 loss, +1 daily_games")
    conn.commit()
    conn.close()

# Отримати користувача за username
async def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
