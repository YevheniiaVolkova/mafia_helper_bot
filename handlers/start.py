# handlers/start.py

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.menu_kb import admin_main_menu_kb

router = Router()

chat_admins = [123456789]  # заміни на своїх адміністраторів

@router.message(CommandStart(deep_link=True))
async def handle_start_with_payload(message: Message):
    payload = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

    if payload.startswith("adminmenu:"):
        group_chat_id = int(payload.split("adminmenu:")[1])
        await message.answer("🔧 Панель керування:", reply_markup=admin_main_menu_kb())

    elif payload == "adminpanel":
        if message.from_user.id not in chat_admins:
            await message.answer("⛔️ У вас немає доступу")
            return
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎲 Івенти", callback_data="open_events")],
            [InlineKeyboardButton(text="⚙️ Інші функції", callback_data="other_admin")]
        ])
        await message.answer("🔧 Адмін-панель:", reply_markup=kb)

    else:
        await message.answer("👋 Вітаємо! Ви у боті-помічнику.")
