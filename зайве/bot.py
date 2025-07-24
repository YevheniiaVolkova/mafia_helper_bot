import asyncio
import json
from pathlib import Path
BASE_DIR = Path(__file__).parent

import logging
import re

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.enums import ChatType
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from asyncio import sleep

import config  # Має містити TOKEN, GROUP_CHAT_ID, ADMIN_IDS

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

# Файли стану
PLAYERS_STATUS = "players_status.json"
ROLES_FILE = "roles.json"
SELECTED_EVENT = "selected_event.json"
QUEEN_STATE = "queen_state.json"

# В пам'яті
chat_admins = set(config.ADMIN_IDS)
players_status = {}
selected_event = None


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_players_status():
    global players_status
    players_status = load_json(PLAYERS_STATUS, {})


def save_players_status():
    save_json(PLAYERS_STATUS, players_status)


def load_selected_event():
    global selected_event
    selected_event = load_json(SELECTED_EVENT, None)


def save_selected_event(event):
    global selected_event
    selected_event = event
    save_json(SELECTED_EVENT, event)


def load_queen_state():
    return load_json(QUEEN_STATE, {
        "initial_done": False,
        "confirmed_user_id": None,
        "last_immunity": None,
    })


def save_queen_state(state):
    save_json(QUEEN_STATE, state)


# --- Адмінські команди ---
@dp.message(Command("get_admins"), F.chat.type.in_({"group", "supergroup"}))
async def get_admins(message: Message):
    global chat_admins
    admins = await bot.get_chat_administrators(message.chat.id)
    chat_admins = {a.user.id for a in admins}
    names = [
        f"@{a.user.username}" if a.user.username else f"{a.user.first_name or ''}".strip()
        for a in admins
    ]
    sent = await message.answer("✅ Адміни:\n" + "\n".join(names))
    await sleep(30)
    try:
        await message.delete()
        await sent.delete()
    except:
        pass


@dp.message(Command("admin"), F.chat.type.in_({"group", "supergroup"}))
async def admin_group(message: Message):
    bot_user = await bot.get_me()
    link = f"https://t.me/{bot_user.username}?start=adminpanel"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Налаштування", url=link)]
    ])
    sent = await message.answer("Натисніть для налаштувань:", reply_markup=kb)
    await sleep(30)
    try:
        await message.delete()
        await sent.delete()
    except:
        pass


@dp.message(Command("start"))
async def start(message: Message):
    txt = message.text or ""
    arg = txt.split(maxsplit=1)[1] if " " in txt else None

    if arg == "adminpanel":
        if message.from_user.id in chat_admins:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🎲 Івенти", callback_data="open_events")],
                [InlineKeyboardButton(text="💰 Гроші", callback_data="money")],
                [InlineKeyboardButton(text="👤 Профіль", callback_data="profile")],
            ])
            await message.answer("🔧 Адмін-панель:", reply_markup=kb)
        else:
            await message.answer("⛔️ У вас немає доступу")
    elif arg == "confirmrole":
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Я — Повія")],
                [KeyboardButton(text="Я — Місто")],
                [KeyboardButton(text="Я — Мафія")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Оберіть роль:", reply_markup=kb)
    else:
        sent = await message.answer("Привіт! Виконайте /admin в групі.")
        await sleep(30)
        try:
            await message.delete()
            await sent.delete()
        except:
            pass


# --- Приватні повідомлення (вибір ролі + адмінка) ---
@dp.message(F.chat.type == ChatType.PRIVATE)
async def private_msg(message: Message):
    txt = message.text or ""

    # Вибір ролі
    if txt in ["Я — Повія", "Я — Місто", "Я — Мафія"]:
        roles = load_json(ROLES_FILE, {})
        role = "повія" if "Повія" in txt else ("мафія" if "Мафія" in txt else "місто")
        roles[str(message.from_user.id)] = {
            "role": role,
            "nickname": message.from_user.full_name
        }
        save_json(ROLES_FILE, roles)
        await message.answer(f"Ви вибрали: {role}", reply_markup=ReplyKeyboardRemove())
        return

    # Панель адміністратора у приваті
    if message.from_user.id in chat_admins:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Івенти", callback_data="open_events")],
            [InlineKeyboardButton(text="💰 Гроші", callback_data="money")],
            [InlineKeyboardButton(text="👤 Профіль", callback_data="profile")],
        ])
        await message.answer("🔧 Адмін-панель:", reply_markup=kb)
    else:
        await message.answer("⛔️ Немає доступу")


# --- Вибір івенту ---
@dp.callback_query(F.data == "open_events")
async def ev_open(cb: CallbackQuery):
    if cb.from_user.id not in chat_admins:
        return

    # Класичне завантаження з локального файлу
    events = load_json("events.json", [])

    logging.info(f"🔍 Завантажено івентів: {len(events)}")

    if not events:
        await cb.message.answer("⚠️ Список івентів порожній. Перевірте файл events.json.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=e["title"], callback_data=f"evprev:{i}")]
        for i, e in enumerate(events)
    ])
    await cb.message.answer("Оберіть івент:", reply_markup=kb)




@dp.callback_query(F.data.startswith("evprev:"))
async def ev_prev(cb: CallbackQuery):
    idx = int(cb.data.split(":", 1)[1])
    events = load_json("events.json", [])
    ev = events[idx]
    text = f"🎲 {ev['title']}\n{ev['description']}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Вибрати", callback_data=f"select:{idx}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="open_events")],
    ])
    await cb.message.answer(text, parse_mode="HTML", reply_markup=kb)


@dp.callback_query(F.data.startswith("select:"))
async def ev_sel(cb: CallbackQuery):
    idx = int(cb.data.split(":", 1)[1])
    events = load_json("events.json", [])
    ev = events[idx]
    save_selected_event(ev)
    await cb.message.answer(f"✅ Вибрано: {ev['title']}", parse_mode="HTML")


# --- Формування status зі списку живих гравців ---
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def build_players_status(message: Message):
    if "Живі гравці:" not in (message.text or ""):
        return
    roles = load_json(ROLES_FILE, {})
    section = message.text.split("Живі гравці:")[1].split("Хтось із них:")[0]
    nicks = [
        line.split(". ", 1)[1].strip()
        for line in section.splitlines() if ". " in line
    ]
    ps = {}
    for uid, info in roles.items():
        nick = info.get("nickname", "")
        ps[uid] = {
            "nickname": nick,
            "role": info["role"],
            "alive": nick in nicks
        }
    global players_status
    players_status = ps
    save_players_status()


# --- Івент "Королева ночі": старт і щоденний імунітет ---
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def on_group_live(message: Message):
    if "Живі гравці:" not in (message.text or ""):
        return
    load_selected_event()
    load_players_status()
    if not selected_event or selected_event.get("id") != "queen_of_night":
        return

    state = load_queen_state()

    # Перший день
    if not state["initial_done"]:
        bot_user = await bot.get_me()
        deep = f"https://t.me/{bot_user.username}?start=confirmrole"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👑 Підтвердити роль", url=deep)]
        ])
        await message.answer("👑 Повія — підтвердіть свою роль у приваті:", reply_markup=kb)
        state["initial_done"] = True
        save_queen_state(state)

    # Наступні дні
    else:
        pov_id = state.get("confirmed_user_id")
        if pov_id:
            kb = await build_immunity_keyboard(state.get("last_immunity"))
            await bot.send_message(
                pov_id,
                "🔸 Новий день — оберіть, кому даєте імунітет:",
                reply_markup=kb
            )


# --- Підтвердження ролі Повією ---
@dp.message(F.chat.type == ChatType.PRIVATE)
async def confirm_role(message: Message):
    text = message.text or ""
    if text.lower().startswith("я — повія"):
        state = load_queen_state()
        state["confirmed_user_id"] = message.from_user.id
        save_queen_state(state)


async def build_immunity_keyboard(last_id):
    load_players_status()
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for uid, info in players_status.items():
        if info["alive"] and uid != last_id:
            kb.inline_keyboard.append([
                InlineKeyboardButton(text=info["nickname"], callback_data=f"imm:{uid}")
            ])
    return kb


@dp.callback_query(F.data.startswith("imm:"))
async def give_immunity(cb: CallbackQuery):
    uid = cb.data.split(":", 1)[1]
    state = load_queen_state()
    if cb.from_user.id != state.get("confirmed_user_id"):
        await cb.answer("Тільки Повія може це зробити.", show_alert=True)
        return

    state["last_immunity"] = uid
    save_queen_state(state)

    nick = players_status.get(uid, {}).get("nickname", "")
    await bot.send_message(
        config.GROUP_CHAT_ID,
        f"🔔 Імунітет отримав: {nick}"
    )
    await cb.answer("Імунітет встановлено.")


# --- Детект смерті Повії та помста ---
@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def detect_poviy_kill(message: Message):
    load_selected_event()
    load_players_status()
    if not selected_event or selected_event.get("id") != "queen_of_night":
        return

    m = re.search(r"вбитий безцінний Повія (.+?)\.\.\.", message.text or "")
    if not m:
        return

    nick = m.group(1).strip()
    pov_id = None
    for uid, info in players_status.items():
        if info["nickname"] == nick and info["role"] == "повія":
            pov_id = int(uid)
            players_status[uid]["alive"] = False
            save_players_status()
            break

    if not pov_id:
        return

    mafia_alive = [
        (u, i["nickname"])
        for u, i in players_status.items()
        if i["role"] == "мафія" and i["alive"]
    ]
    if not mafia_alive:
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=n, callback_data=f"rev:{u}")]
        for u, n in mafia_alive
    ])
    await bot.send_message(
        pov_id,
        "👑 Ви мертві. Оберіть мафіозі для помсти:",
        reply_markup=kb
    )


@dp.callback_query(F.data.startswith("rev:"))
async def revenge(cb: CallbackQuery):
    mafia_uid = cb.data.split(":", 1)[1]
    load_players_status()
    pov_id = cb.from_user.id
    pov_nick = players_status[str(pov_id)]["nickname"]
    mafia_nick = players_status.get(mafia_uid, {}).get("nickname", "???")

    await bot.send_message(
        config.GROUP_CHAT_ID,
        f"👑 Повія {pov_nick} помстилася! Розкрито мафіозі: {mafia_nick}."
    )
    await cb.answer("Помста виконана.")


async def main():
    load_selected_event()
    load_players_status()
    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




#cd 'c:\женя\мафія\Бот\mafia_helper_bot'

#python bot.py

