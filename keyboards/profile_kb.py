from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪙 Використати валюту", callback_data="use_currency")],
        [InlineKeyboardButton(text="💼 Заробити валюту", callback_data="earn_currency")]
    ])
