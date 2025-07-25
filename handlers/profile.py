from aiogram import Router, types, Bot
from aiogram.filters import Command
from keyboards.menu_kb import profile_action_kb
from database.users import get_or_create_user, get_user_by_id

router = Router()

@router.message(Command("profile"))
async def show_profile(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or "Без ніка"

    # ⏺️ Створити або оновити користувача
    await get_or_create_user(user_id=user_id, username=username)

    # 🔎 Отримати його профіль
    user = await get_user_by_id(user_id)
    if not user:
        await message.answer("⚠️ Не вдалося отримати ваш профіль.")
        return

    # 🛡 Перевірка чи адмін
    is_admin = False
    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await bot.get_chat_member(message.chat.id, user_id)
            if member.status in ["administrator", "creator"]:
                is_admin = True
        except Exception:
            pass
    else:
        is_admin = True  # У приваті автоматично

    # 📊 Вивід профілю
    text = (
        f"<b>👤 Профіль:</b>\n"
        f"Нік: @{user['username'] or 'Без ніка'}\n"
        f"💰 Бабідони: {user['balance']}\n"
        f"🌟 Зірки: {user['stars']}\n"
        f"🎮 Ігор сьогодні: {user['daily_games']}\n"
        f"🏆 Перемог: {user['wins']}\n"
        f"💀 Поразок: {user['losses']}"
    )
    await message.answer(text, reply_markup=profile_action_kb(is_admin=is_admin))
