from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🎲 Івенти"), KeyboardButton("👤 Користувачі")],
            [KeyboardButton("💰 Власна валюта"), KeyboardButton("📈 Статистика")],
            [KeyboardButton("⚙️ Налаштування")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Обери дію з меню..."
    )

def get_admin_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Івенти", callback_data="admin_events")],
        [InlineKeyboardButton(text="👥 Користувачі", callback_data="admin_users")],
        [InlineKeyboardButton(text="💰 Власна валюта", callback_data="admin_currency")],
        [InlineKeyboardButton(text="📈 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="admin_settings")]
    ])
