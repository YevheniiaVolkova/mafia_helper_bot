import os
from dotenv import load_dotenv

# Завантажує змінні середовища з .env файлу
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "mafia_helper_bot.db")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")  # Без @

config = Config()
