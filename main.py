import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from database.db import init_db
from handlers import profile, events, admin, roles, settings, start, callbacks, profile_callbacks, game_end
from aiogram.client.default import DefaultBotProperties


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Підключаємо кожен роутер окремо
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(events.router)
dp.include_router(admin.router)
dp.include_router(roles.router)
dp.include_router(settings.router)
dp.include_router(callbacks.router)
dp.include_router(profile_callbacks.router)
dp.include_router(game_end.router)


if __name__ == "__main__":
    init_db()
    dp.run_polling(bot)



#python main.py