from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_list, as_marked_section, Bold, Text

from database.users import get_all_users, get_chat_stars_balance  # обидві функції мають бути в users.py

router = Router()

# 🪙 Придбати бабідони
@router.callback_query(lambda c: c.data == "buy_babidons")
async def handle_buy_babidons(callback: CallbackQuery):
    await callback.message.answer(
        "💸 Для придбання бабідонів — зверніться до адміністрації або скористайтесь магазином (у розробці)."
    )
    await callback.answer()

# 💸 Витратити бабідони
@router.callback_query(lambda c: c.data == "spend_babidons")
async def handle_spend_babidons(callback: CallbackQuery):
    await callback.message.answer(
        "🪙 Ви можете витратити бабідони на:\n• скіни\n• статуси\n• доступ до бонусних подій.\n\n🔧 Функціонал у розробці!"
    )
    await callback.answer()

# 📋 Перегляд усіх профілів (для адміна)
@router.callback_query(lambda c: c.data == "view_all_profiles")
async def handle_view_all_profiles(callback: CallbackQuery):
    users = await get_all_users()
    if not users:
        await callback.message.answer("📭 Немає зареєстрованих користувачів.")
    else:
        text = "<b>📋 Усі профілі користувачів:</b>\n"
        for user in users:
            text += (
                f"\n👤 @{user['username'] or 'Без_ніка'}\n"
                f"• Бабідони: {user['balance']} 💰\n"
                f"• Зірки: {user['stars']} ⭐\n"
                f"• Ігор: {user['daily_games']} | ✅ {user['wins']} / ❌ {user['losses']}\n"
            )
        await callback.message.answer(text)
    await callback.answer()

# ⭐ Баланс чату у зірках (сума всіх користувачів)
@router.callback_query(lambda c: c.data == "chat_stars_balance")
async def handle_chat_stars(callback: CallbackQuery):
    total_stars = await get_chat_stars_balance()
    await callback.message.answer(f"⭐ Загальний баланс зірок у чаті: <b>{total_stars} ⭐</b>")
    await callback.answer()
