from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_action_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📊 Переглянути статистику", callback_data="view_stats")],
        [InlineKeyboardButton(text="🪙 Придбати бабідони", callback_data="buy_babidons")],
        [InlineKeyboardButton(text="💸 Витратити бабідони", callback_data="spend_babidons")]
    ]

    if is_admin:
        buttons.append([InlineKeyboardButton(text="📋 Усі профілі", callback_data="view_all_profiles")])
        buttons.append([InlineKeyboardButton(text="⭐ Баланс чату у зірках", callback_data="chat_stars_balance")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
