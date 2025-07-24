from aiogram import Router, types
from aiogram.filters import Command
from database import get_connection
from keyboards.profile_kb import profile_menu_kb

router = Router()

@router.message(Command("profile"))
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без ніка"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            cursor.execute("INSERT INTO players (user_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            games_played, balance, stars = 0, 0, 0
        else:
            games_played, balance, stars = row[3], row[4], row[5]

    text = f"""
<b>👤 Профіль:</b>
Нік: @{username}
Ігор зіграно: {games_played}
Баланс: {balance} 💰
Зірки Telegram: {stars} ⭐
"""
    await message.answer(text, reply_markup=profile_menu_kb())
