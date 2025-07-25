from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.menu_kb import admin_extra_kb, user_profile_kb
from database.users import get_or_create_user, get_user_by_id
from config import config
import logging

router = Router()
logger = logging.getLogger(__name__)
BOT_USERNAME = config.BOT_USERNAME


# 👤 Показати профіль користувача з кнопками
async def show_profile(message: Message, is_admin: bool):
    user = await get_user_by_id(message.from_user.id)
    if not user:
        return await message.answer("❌ Не вдалося завантажити профіль.")

    full_name = message.from_user.full_name or "(не вказано)"

    profile_text = (
        f"👤 <b>Профіль</b>:\n"
        f"Ім’я: {full_name}\n"
        f"Бабідони: {user['balance']} 💰\n"
        f"Зірки: {user['stars']} ⭐\n"
        f"Ігор сьогодні: {user['daily_games']}\n"
        f"Перемог: {user['wins']} ✅\n"
        f"Поразок: {user['losses']} ❌"
    )

    kb = admin_extra_kb() if is_admin else user_profile_kb()
    await message.answer(profile_text, reply_markup=kb)


# 🟢 /start (враховує deep-link)
@router.message(CommandStart(deep_link=True))
async def handle_start(message: Message, command: CommandStart):
    await get_or_create_user(message.from_user.id, message.from_user.username or "")
    args = command.args

    if args == "menu":
        # Відкрили бот через deep link "menu"
        is_admin = False  # тут можна додати перевірку адміна, якщо потрібно
        await show_profile(message, is_admin=is_admin)
        return

    await message.answer("👋 Вітаємо! Напишіть /menu щоб переглянути свій профіль.")


# 📲 /menu — доступна всім (і в групі, і в приватку)
@router.message(Command("menu"))
async def handle_menu(message: Message, bot: Bot):
    if message.chat.type not in ["private", "group", "supergroup"]:
        return

    await get_or_create_user(message.from_user.id, message.from_user.username or "")

    # Визначаємо, чи це адмін
    is_admin = False
    if message.chat.type in ["group", "supergroup"]:
        try:
            member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
            is_admin = member.status in ["administrator", "creator"]
        except Exception as e:
            logger.warning(f"Помилка перевірки адміна: {e}")

        # У групі просто надсилаємо кнопку для переходу в бот
        link = f"https://t.me/{BOT_USERNAME}?start=menu"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Перейти в бот для перегляду профілю", url=link)]
        ])
        await message.answer(
            "Щоб переглянути свій профіль, перейдіть у приватний чат з ботом:",
            reply_markup=kb
        )
        return

    elif message.chat.type == "private":
        # Якщо приватний чат — показуємо профіль одразу
        await show_profile(message, is_admin=is_admin)


# 🛠 /admin — лише для адміністраторів
@router.message(Command("admin"))
async def handle_admin(message: Message, bot: Bot):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.answer("❌ Ця команда доступна лише в групах.")

    try:
        member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            return await message.answer("🚫 Ви не адміністратор групи.")
    except Exception as e:
        logger.warning(f"Помилка перевірки адміна: {e}")
        return await message.answer("⚠️ Не вдалося перевірити ваш статус.")

    link = f"https://t.me/{BOT_USERNAME}?start=menu"
    await message.answer(
        f"🔧 Відкрийте адмін-меню в боті:\n👉 <a href=\"{link}\">Натисніть тут</a>",
        parse_mode="HTML"
    )
