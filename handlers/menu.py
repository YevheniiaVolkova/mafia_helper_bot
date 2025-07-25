from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import get_user_by_id
from config import config
import logging

router = Router()
logger = logging.getLogger(__name__)
BOT_USERNAME = config.BOT_USERNAME

# 👤 Показати профіль з кнопками
async def show_profile_with_buttons(message: Message, is_admin: bool):
    user = await get_user_by_id(message.from_user.id)
    if not user:
        return await message.answer("❌ Не вдалося завантажити профіль.")

    text = (
        f"👤 <b>Профіль:</b>\n"
        f"Нік: @{user['username'] or 'Без ніка'}\n"
        f"Баланс: {user['balance']} 💰\n"
        f"Зірки: {user['stars']} ⭐\n"
        f"Ігор сьогодні: {user['daily_games']}\n"
        f"Перемог: {user['wins']} ✅\n"
        f"Поразок: {user['losses']} ❌"
    )

    # Базові кнопки
    buttons = [
        [InlineKeyboardButton(text="👛 Придбати бабідони", callback_data="buy_babidons")],
        [InlineKeyboardButton(text="💸 Витратити бабідони", callback_data="spend_babidons")]
    ]

    # Якщо адмін — додаємо додаткові
    if is_admin:
        buttons.append([InlineKeyboardButton(text="👥 Перегляд усіх профілів", callback_data="view_all_profiles")])
        buttons.append([InlineKeyboardButton(text="⭐ Баланс чату у зірках", callback_data="chat_stars_balance")])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text, reply_markup=kb)

# 📲 /menu — доступна всім (у групі або в приваті)
@router.message(Command("menu"))
async def handle_menu(message: Message, bot: Bot):
    user_id = message.from_user.id
    is_admin = False

    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await bot.get_chat_member(message.chat.id, user_id)
            is_admin = member.status in ["administrator", "creator"]
        except Exception as e:
            logger.warning(f"Не вдалося визначити статус користувача: {e}")
    else:
        # У приватному чаті — вважай що всі мають доступ
        is_admin = True

    await show_profile_with_buttons(message, is_admin=is_admin)
