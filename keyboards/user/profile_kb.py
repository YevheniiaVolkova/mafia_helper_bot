# mafia_helper_bot/keyboards/user/profile_kb.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_profile_keyboard():
    buttons = [
        [InlineKeyboardButton(text="💰 Поповнити", callback_data="top_up_balance")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="user_stats")],
        [InlineKeyboardButton(text="🔄 Обміняти зірки", callback_data="exchange_stars")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
