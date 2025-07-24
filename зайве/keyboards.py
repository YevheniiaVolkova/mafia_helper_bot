from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_settings_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Налаштування івентів", url="https://t.me/Mafia_Babidzhon_Bot")]
    ])
    return kb
