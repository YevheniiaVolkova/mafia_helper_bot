from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    await message.answer("⚙️ Тут будуть налаштування бота (поки що в розробці).")
