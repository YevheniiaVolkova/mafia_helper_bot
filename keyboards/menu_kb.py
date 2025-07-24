from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🎲 Івенти"), KeyboardButton("👤 Користувачі")],
            [KeyboardButton("⚙️ Налаштування"), KeyboardButton("📊 Статистика")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Обери дію з меню..."
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_menu_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Івенти", callback_data="admin_events")],
        [InlineKeyboardButton(text="👥 Користувачі", callback_data="admin_users")],
        [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="admin_settings")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")]
    ])
    return keyboard
