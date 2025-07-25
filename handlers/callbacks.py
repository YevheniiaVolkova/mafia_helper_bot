from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold, as_list
from database.users import get_all_users, get_user_by_id
from aiogram.fsm.context import FSMContext

router = Router()

# 👛 Придбати бабідони
@router.callback_query(lambda c: c.data == "buy_currency")
async def handle_buy_currency(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("🛒 Щоб придбати бабідони — зверніться до адміністратора або натисніть на кнопку купівлі в майбутньому.")

# 💸 Витратити бабідони
@router.callback_query(lambda c: c.data == "spend_currency")
async def handle_spend_currency(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("💸 Тут зʼявляться варіанти витрати бабідонів. Функціонал незабаром буде доступний.")

# 👥 Перегляд усіх профілів
@router.callback_query(lambda c: c.data == "admin_view_profiles")
async def handle_admin_view_profiles(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_users()

    if not users:
        return await callback.message.answer("📭 У базі немає користувачів.")

    text_blocks = []
    for user in users:
        text_blocks.append(
            f"👤 @{user['username']} | 💰 {user['balance']} | ⭐ {user['stars']} | 🎮 {user['daily_games']} | ✅ {user['wins']} | ❌ {user['losses']}"
        )

    await callback.message.answer("\n".join(text_blocks))

# ⭐ Баланс чату у зірках
@router.callback_query(lambda c: c.data == "admin_chat_stars")
async def handle_admin_chat_stars(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_users()
    total_stars = sum(user['stars'] for user in users if user['stars'] is not None)
    await callback.message.answer(f"⭐ Загальний баланс чату у зірках: <b>{total_stars}</b>")
