from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import config
from aiogram.utils.deep_linking import create_start_link
from keyboards.menu_kb import admin_main_menu_kb
from database import (
    get_all_events, get_event, add_event, update_event, delete_event,
    ban_user, unban_user, is_banned, get_user_stats, update_user_balance,
    set_setting, get_setting
)
import logging
from aiogram.exceptions import TelegramBadRequest

router = Router()
chat_admins = set()
logger = logging.getLogger(__name__)
BOT_USERNAME = config.BOT_USERNAME

class EventForm(StatesGroup):
    add_waiting_for_id = State()
    add_waiting_for_title = State()
    add_waiting_for_description = State()
    edit_waiting_for_title = State()
    edit_waiting_for_description = State()

@router.message(Command("get_admins"), F.chat.type.in_({"group", "supergroup"}))
async def get_admins_handler(message: Message, bot: Bot):
    global chat_admins
    admins = await bot.get_chat_administrators(message.chat.id)
    chat_admins = {a.user.id for a in admins}
    names = [f"@{a.user.username}" if a.user.username else a.user.first_name for a in admins]
    sent = await message.answer("✅ Адміни:\n" + "\n".join(names))
    await sent.delete(delay=60)
    await message.delete(delay=60)
    logger.info(f"Admins updated: {chat_admins}")

@router.message(Command("admin"), F.chat.type.in_({"group", "supergroup"}))
async def admin_group(message: Message, bot: Bot):
    bot_user = await bot.get_me()
    link = f"https://t.me/{bot_user.username}?start=adminpanel"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Налаштування", url=link)]
    ])
    await message.answer("Натисніть для налаштувань:", reply_markup=kb)
    

@router.message(CommandStart(deep_link=True))
async def handle_start_with_payload(message: Message):
    payload = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

    if payload == "adminpanel":
        if message.from_user.id not in chat_admins:
            await message.answer("⛔️ У вас немає доступу")
            return
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Івенти", callback_data="open_events")],
            [InlineKeyboardButton(text="⚙️ Інші функції", callback_data="other_admin")],
            [InlineKeyboardButton(text="💰 Власна валюта", callback_data="admin_currency")],
            [InlineKeyboardButton(text="📈 Статистика", callback_data="admin_stats")],
        ])
        await message.answer("🔧 Адмін-панель:", reply_markup=kb)

    elif payload.startswith("adminmenu:"):
        group_chat_id = int(payload.split("adminmenu:")[1])
        await message.answer("🔧 Панель керування:", reply_markup=admin_main_menu_kb())

    else:
        await message.answer("👋 Вітаємо! Ви у боті-помічнику.")

# --- Івенти (те саме, що ти вже маєш) ---
# Ти можеш залишити у своєму файлі або додати сюди, як тобі зручно

@router.callback_query(F.data == "other_admin")
async def other_admin_cb(cb: CallbackQuery):
    await cb.answer("Поки що інших функцій немає.", show_alert=True)

@router.callback_query(F.data == "admin_currency")
async def handle_admin_currency(cb: CallbackQuery):
    if cb.from_user.id not in chat_admins:
        await cb.answer("⛔️ Немає доступу", show_alert=True)
        return
    await cb.message.answer("💰 Тут можна керувати власною валютою (поки що заглушка).")
    await cb.answer()

@router.callback_query(F.data == "admin_stats")
async def handle_admin_stats(cb: CallbackQuery):
    if cb.from_user.id not in chat_admins:
        await cb.answer("⛔️ Немає доступу", show_alert=True)
        return
    await cb.message.answer("📈 Статистика поки що в розробці.")
    await cb.answer()

# Команда /menu у групі, щоб показати посилання на адмін меню
@router.message(F.text == "/menu")
async def send_admin_menu_link(message: Message, bot: Bot):
    if message.chat.type not in ("supergroup", "group"):
        return await message.answer("❗ Команда доступна лише в групі.")
    # Перевірка, що користувач - адмін
    if message.from_user.id not in chat_admins:
        return await message.answer("🚫 Ви не адміністратор групи.")
    deep_link = await create_start_link(bot, payload=f"adminmenu:{message.chat.id}", encode=True)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Перейти до керування", url=deep_link)]
    ])
    await message.answer("🔧 Відкрийте меню керування у приватному чаті з ботом:", reply_markup=kb)
