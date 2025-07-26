import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import config
from database.db import init_db
from handlers import main_router  # імпортуємо один головний роутер

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

if __name__ == "__main__":
    init_db()
    dp.include_router(main_router)  # Один єдиний виклик
    dp.run_polling(bot)


#python main.py