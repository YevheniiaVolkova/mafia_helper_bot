from dataclasses import dataclass
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()  # шлях до теки з config.py

@dataclass
class Config:
    BOT_TOKEN: str
    BOT_USERNAME: str
    DATABASE_PATH: str

config = Config(
    BOT_TOKEN=os.getenv("BOT_TOKEN"),
    BOT_USERNAME=os.getenv("BOT_USERNAME", "BabidzhonBot"),  # без @
    DATABASE_PATH=os.getenv("DATABASE_PATH", str(BASE_DIR / "database" / "mafia.db"))
)
