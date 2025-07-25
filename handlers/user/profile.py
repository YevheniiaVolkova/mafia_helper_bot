from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.db import get_user_by_id

router = Router()

@router.message(Command("profile"))
async def profile_handler(message: Message):
    user = get_user_by_id(message.from_user.id)

    if not user:
        await message.answer("🔒 Ви ще не зареєстровані в системі.")
        return

    text = (
        f"👤 <b>Профіль користувача</b>\n"
        f"🆔 ID: <code>{user['user_id']}</code>\n"
        f"👥 Username: @{user['username'] or 'Немає'}\n"
        f"💼 Роль: {user['role']}\n"
        f"💰 Баланс: {user['balance']} ₼\n"
        f"⭐ Зірки Telegram: {user['stars']}\n"
        f"🎮 Ігор сьогодні: {user['daily_games']}\n"
        f"✅ Перемог: {user['wins']}\n"
        f"❌ Поразок: {user['losses']}\n"
    )

    await message.answer(text, parse_mode="HTML")
