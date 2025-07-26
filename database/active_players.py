import sqlite3
from database.db import get_connection
import logging

logger = logging.getLogger(__name__)

# Зберегти одного активного гравця (асинхронна функція, якщо потрібно - але тут синхронна)
async def save_active_player(username: str, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO active_players (username, user_id)
        VALUES (?, ?)
    """, (username, user_id))
    conn.commit()
    conn.close()

# Синхронна функція для збереження списку активних гравців
def save_active_players(players: list[tuple[str, int]]):
    """
    players — список кортежів (username, user_id)
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM active_players")

    cursor.executemany("INSERT INTO active_players (username, user_id) VALUES (?, ?)", players)

    conn.commit()
    conn.close()

    logger.info(f"Збережено {len(players)} активних гравців у таблицю active_players")

# Отримати user_id за username
async def get_user_id_by_username(username: str) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM active_players WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# ⬅️ ДОДАНО: Отримати всіх активних гравців
async def get_all_active_players() -> list[tuple[str, int]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, user_id FROM active_players")
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in rows]
