from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import config  # <-- Ось так правильно
from database.db import init_db
from handlers import profile, events, admin, roles, settings, game_stats
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(
    profile.router,
    events.router,
    admin.router,
    roles.router,
    settings.router,
    #game_stats.router,
)

if __name__ == "__main__":
    init_db()
    dp.run_polling(bot)




#       python main.py