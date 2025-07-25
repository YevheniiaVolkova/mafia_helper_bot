from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

# 📍 Звичайне меню користувача (reply клавіатура)
def user_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профіль")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Обери дію з меню..."
    )

# 📍 Головне меню адміністратора (reply клавіатура)
def admin_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎲 Івенти"), KeyboardButton(text="👤 Користувачі")],
            [KeyboardButton(text="💰 Власна валюта"), KeyboardButton(text="📈 Статистика")],
            [KeyboardButton(text="⚙️ Налаштування")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Обери дію з меню..."
    )

# 📍 Інлайн-меню для адмін-панелі (callback_data)
def get_admin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Івенти", callback_data="admin_events")],
        [InlineKeyboardButton(text="👥 Користувачі", callback_data="admin_users")],
        [InlineKeyboardButton(text="💰 Власна валюта", callback_data="admin_currency")],
        [InlineKeyboardButton(text="📈 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="admin_settings")]
    ])

# 📍 Інлайн-кнопки під профілем — для звичайного користувача
def user_profile_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👛 Придбати бабідони", callback_data="buy_babidons")],
        [InlineKeyboardButton(text="🛍 Витратити бабідони", callback_data="spend_babidons")],
        [InlineKeyboardButton(text="📊 Переглянути статистику", callback_data="view_stats")]
    ])

# 📍 Інлайн-кнопки під профілем — для адміністратора (розширені)
def admin_extra_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👛 Придбати бабідони", callback_data="buy_babidons")],
        [InlineKeyboardButton(text="🛍 Витратити бабідони", callback_data="spend_babidons")],
        [InlineKeyboardButton(text="📊 Переглянути статистику", callback_data="view_stats")],
        [InlineKeyboardButton(text="👥 Профілі всіх користувачів", callback_data="view_all_profiles")],
        [InlineKeyboardButton(text="⭐ Баланс чату у зірках", callback_data="chat_stars_balance")]
    ])

# 📍 Універсальна функція для клавіатури профілю — вибір кнопок залежно від ролі
def profile_action_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="👛 Придбати бабідони", callback_data="buy_babidons")],
        [InlineKeyboardButton(text="🛍 Витратити бабідони", callback_data="spend_babidons")],
        [InlineKeyboardButton(text="📊 Переглянути статистику", callback_data="view_stats")]
    ]

    if is_admin:
        buttons.append([InlineKeyboardButton(text="👥 Профілі всіх користувачів", callback_data="view_all_profiles")])
        buttons.append([InlineKeyboardButton(text="⭐ Баланс чату у зірках", callback_data="chat_stars_balance")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
