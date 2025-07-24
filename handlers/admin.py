from aiogram import Router, F, Bot
from aiogram.filters import Command, Text, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils.access import is_chat_admin
from utils.access import is_admin
from database.db import get_db
from config import BOT_USERNAME
from aiogram.utils.deep_linking import create_start_link
from keyboards.menu_kb import get_admin_menu_kb


import logging

from database import get_all_events, get_event, add_event, update_event, delete_event, ban_user, unban_user, is_banned,
    get_user_stats, update_user_balance, update_user_stats,
    set_setting, get_setting

router = Router()

chat_admins = set()

# Логування
logger = logging.getLogger(__name__)

# FSM стани для додавання / редагування івентів
class EventForm(StatesGroup):
    waiting_for_id = State()
    waiting_for_title = State()
    waiting_for_description = State()
    editing_field = State()  # для редагування окремих полів

# --- Команди ---

@router.message(Command("get_admins"), F.chat.type.in_({"group", "supergroup"}))
async def get_admins_handler(message: Message, bot: Bot):
    global chat_admins
    admins = await bot.get_chat_administrators(message.chat.id)
    chat_admins = {a.user.id for a in admins}
    names = [f"@{a.user.username}" if a.user.username else a.user.first_name for a in admins]
    sent = await message.answer("✅ Адміни:\n" + "\n".join(names))
    await sent.delete(delay=30)
    await message.delete(delay=30)
    logger.info(f"Admins updated: {chat_admins}")

@router.message(Command("admin"), F.chat.type.in_({"group", "supergroup"}))
async def admin_group(message: Message, bot: Bot):
    bot_user = await bot.get_me()
    link = f"https://t.me/{bot_user.username}?start=adminpanel"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Налаштування", url=link)]
    ])
    sent = await message.answer("Натисніть для налаштувань:", reply_markup=kb)
    await sent.delete(delay=30)
    await message.delete(delay=30)

@router.message(Text(startswith="/start adminpanel"))
async def admin_panel(message: Message):
    if message.from_user.id not in chat_admins:
        await message.answer("⛔️ У вас немає доступу")
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Івенти", callback_data="open_events")],
        [InlineKeyboardButton(text="⚙️ Інші функції", callback_data="other_admin")],
    ])
    await message.answer("🔧 Адмін-панель:", reply_markup=kb)

# --- Івенти ---

@router.callback_query(F.data == "open_events")
async def open_events_cb(cb: CallbackQuery):
    if cb.from_user.id not in chat_admins:
        await cb.answer("⛔️ Немає доступу", show_alert=True)
        return

    events = get_all_events()
    if not events:
        await cb.message.answer("⚠️ Список івентів порожній.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=ev["title"], callback_data=f"evview:{ev['id']}")]
        for ev in events
    ] + [[InlineKeyboardButton(text="➕ Додати новий івент", callback_data="evadd")]])
    await cb.message.answer("Оберіть івент:", reply_markup=kb)
    await cb.answer()

@router.callback_query(F.data.startswith("evview:"))
async def ev_view(cb: CallbackQuery):
    ev_id = cb.data.split(":", 1)[1]
    ev = get_event(ev_id)
    if not ev:
        await cb.answer("Івент не знайдено", show_alert=True)
        return

    text = f"🎲 <b>{ev['title']}</b>\n\n{ev['description']}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редагувати", callback_data=f"evedit:{ev_id}")],
        [InlineKeyboardButton(text="❌ Видалити", callback_data=f"evdel:{ev_id}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="open_events")]
    ])
    await cb.message.answer(text, parse_mode="HTML", reply_markup=kb)
    await cb.answer()

@router.callback_query(F.data == "evadd")
async def ev_add_start(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id not in chat_admins:
        await cb.answer("⛔️ Немає доступу", show_alert=True)
        return
    await state.set_state(EventForm.waiting_for_id)
    await cb.message.answer("📝 Введіть унікальний ID для нового івенту:")
    await cb.answer()

@router.message(EventForm.waiting_for_id)
async def ev_add_id(message: Message, state: FSMContext):
    ev_id = message.text.strip()
    if get_event(ev_id):
        await message.answer("⚠️ Івент з таким ID вже існує. Введіть інший ID.")
        return
    await state.update_data(ev_id=ev_id)
    await state.set_state(EventForm.waiting_for_title)
    await message.answer("Введіть назву івенту:")

@router.message(EventForm.waiting_for_title)
async def ev_add_title(message: Message, state: FSMContext):
    title = message.text.strip()
    await state.update_data(title=title)
    await state.set_state(EventForm.waiting_for_description)
    await message.answer("Введіть опис івенту:")

@router.message(EventForm.waiting_for_description)
async def ev_add_description(message: Message, state: FSMContext):
    description = message.text.strip()
    data = await state.get_data()
    ev_id = data["ev_id"]
    title = data["title"]
    add_event(ev_id, title, description)
    await message.answer("✅ Івент додано!")
    logger.info(f"Event added: {ev_id} - {title}")
    await state.clear()
    
@router.callback_query(F.data.startswith("evedit:"))
async def ev_edit_start(cb: CallbackQuery, state: FSMContext):
    ev_id = cb.data.split(":", 1)[1]
    ev = get_event(ev_id)
    if not ev:
        await cb.answer("Івент не знайдено", show_alert=True)
        return
    if cb.from_user.id not in chat_admins:
        await cb.answer("⛔️ Немає доступу", show_alert=True)
        return
    await state.update_data(ev_id=ev_id)
    await state.set_state(EventForm.waiting_for_title)
    await cb.message.answer(f"✏️ Редагуємо івент '{ev['title']}'. Введіть нову назву або надішліть /skip для пропуску.")
    await cb.answer()

@router.message(EventForm.waiting_for_title)
async def ev_edit_title(message: Message, state: FSMContext):
    if message.text == "/skip":
        data = await state.get_data()
        ev_id = data["ev_id"]
        ev = get_event(ev_id)
        await state.update_data(title=ev["title"])
    else:
        await state.update_data(title=message.text.strip())
    await state.set_state(EventForm.waiting_for_description)
    await message.answer("Введіть новий опис або /skip для пропуску:")

@router.message(EventForm.waiting_for_description)
async def ev_edit_description(message: Message, state: FSMContext):
    data = await state.get_data()
    ev_id = data["ev_id"]
    title = data.get("title")
    if message.text == "/skip":
        ev = get_event(ev_id)
        description = ev["description"]
    else:
        description = message.text.strip()

    update_event(ev_id, title, description)
    await message.answer("✅ Івент оновлено!")
    logger.info(f"Event updated: {ev_id} - {title}")
    await state.clear()

@router.callback_query(F.data.startswith("evdel:"))
async def ev_delete(cb: CallbackQuery):
    ev_id = cb.data.split(":", 1)[1]
    if cb.from_user.id not in chat_admins:
        await cb.answer("⛔️ Немає доступу", show_alert=True)
        return
    delete_event(ev_id)
    await cb.message.answer("🗑 Івент видалено.")
    await open_events_cb(cb)
    await cb.answer()

# Можна додати колбек для "other_admin" для інших функцій, поки що просто відповідає
@router.callback_query(F.data == "other_admin")
async def other_admin_cb(cb: CallbackQuery):
    await cb.answer("Поки що інших функцій немає.", show_alert=True)

# Бан користувача
@router.message(Command("ban"))
async def cmd_ban(message: Message):
    if message.from_user.id not in chat_admins:
        await message.answer("⛔️ Немає доступу")
        return
    if not message.reply_to_message:
        await message.answer("Щоб забанити користувача, надішліть команду у відповідь на його повідомлення.")
        return
    user_id = message.reply_to_message.from_user.id
    ban_user(user_id)
    await message.answer(f"🚫 Користувач {user_id} заблокований.")

# Розбан користувача
@router.message(Command("unban"))
async def cmd_unban(message: Message):
    if message.from_user.id not in chat_admins:
        await message.answer("⛔️ Немає доступу")
        return
    if not message.reply_to_message:
        await message.answer("Щоб розбанити користувача, надішліть команду у відповідь на його повідомлення.")
        return
    user_id = message.reply_to_message.from_user.id
    unban_user(user_id)
    await message.answer(f"✅ Користувач {user_id} розблокований.")

# Перевірка статусу бану
@router.message(Command("checkban"))
async def cmd_checkban(message: Message):
    user_id = message.from_user.id
    banned = is_banned(user_id)
    await message.answer(f"Ви {'заблоковані' if banned else 'не заблоковані'}.")

# Перегляд статистики користувача
@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user_id = message.from_user.id
    stats = get_user_stats(user_id)
    text = (f"Ваш баланс: {stats['balance']} ум\n"
            f"Перемог: {stats['wins']}\n"
            f"Поразок: {stats['losses']}")
    await message.answer(text)

# Оновлення балансу (для демонстрації)
@router.message(Command("addbalance"))
async def cmd_addbalance(message: Message):
    if message.from_user.id not in chat_admins:
        await message.answer("⛔️ Немає доступу")
        return
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Використання: /addbalance <user_id> <сума>")
        return
    try:
        user_id = int(args[1])
        amount = int(args[2])
    except:
        await message.answer("Невірні параметри.")
        return
    update_user_balance(user_id, amount)
    await message.answer(f"Баланс користувача {user_id} змінено на {amount} ум.")

# Приклад налаштувань
@router.message(Command("setparam"))
async def cmd_setparam(message: Message):
    if message.from_user.id not in chat_admins:
        await message.answer("⛔️ Немає доступу")
        return
    args = message.text.split(maxsplit=2)
    if len(args) != 3:
        await message.answer("Використання: /setparam <ключ> <значення>")
        return
    key, value = args[1], args[2]
    set_setting(key, value)
    await message.answer(f"Параметр '{key}' встановлено в '{value}'.")

@router.message(Command("getparam"))
async def cmd_getparam(message: Message):
    if message.from_user.id not in chat_admins:
        await message.answer("⛔️ Немає доступу")
        return
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Використання: /getparam <ключ>")
        return
    key = args[1]
    value = get_setting(key)
    await message.answer(f"Параметр '{key}': '{value}'" if value else f"Параметр '{key}' не встановлено.")

@router.message(F.text == "/menu")
async def send_admin_menu_link(message: Message, bot):
    if message.chat.type not in ("supergroup", "group"):
        return await message.answer("❗ Команда доступна лише в групі.")

    # Перевірка, що це адмін
    if not await is_chat_admin(bot, message.from_user.id, message.chat.id):
        return await message.answer("🚫 Ви не адміністратор групи.")

    # Створюємо унікальне стартове посилання з payload'ом
    deep_link = await create_start_link(bot, payload=f"adminmenu:{message.chat.id}", encode=True)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⚙️ Перейти до керування", url=deep_link)]
    ])

    await message.answer("🔧 Відкрийте меню керування у приватному чаті з ботом:", reply_markup=kb)


@router.message(CommandStart(deep_link=True))
async def handle_start_with_payload(message: Message):
    if not message.text.startswith("/start adminmenu:"):
        return

    payload = message.text.split("adminmenu:")[1]
    group_chat_id = int(payload)

    # Можна перевірити в базі, чи цей користувач має статус "admin"
    # Але зараз просто відкриємо меню
    from keyboards.menu_kb import admin_main_menu_kb
    await message.answer("🔧 Панель керування:", reply_markup=admin_main_menu_kb())

    @router.message(Command("menu"))
async def send_admin_menu_link(message: Message):
    # Перевірка, чи це група
    if message.chat.type not in ["group", "supergroup"]:
        return await message.answer("Ця команда працює лише в групі.")

    # Перевірка, чи це адмін
    if not await is_admin(message.bot, message.chat.id, message.from_user.id):
        return await message.answer("❌ Лише адміністратори мають доступ до меню.")

    # Генерація посилання в приват
    deep_link = f"https://t.me/{BOT_USERNAME}?start=adminmenu"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Відкрити меню керування", url=deep_link)]
    ])
    await message.answer("Відкрийте меню керування у приватному чаті:", reply_markup=keyboard)

@router.message(CommandStart(deep_link="adminmenu"))
async def open_admin_menu(message: Message):
    await message.answer(
        "👑 Адмінське меню:\n\nОберіть, що ви хочете налаштувати:",
        reply_markup=get_admin_menu_kb()
    )

@router.callback_query(F.data == "admin_events")
async def open_events_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("🔧 Налаштування івентів (в розробці)")

@router.callback_query(F.data == "admin_users")
async def open_users_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("👥 Керування користувачами (в розробці)")

@router.callback_query(F.data == "admin_settings")
async def open_settings_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("⚙️ Загальні налаштування (в розробці)")

@router.callback_query(F.data == "admin_stats")
async def open_stats_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("📊 Статистика по іграх (в розробці)")
