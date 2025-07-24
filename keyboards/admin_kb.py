from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def update_admins_kb():
    keyboard = [
        [InlineKeyboardButton(text="🔄 Оновити адмінів", callback_data="update_admins")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


