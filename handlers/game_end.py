import logging
import re
from aiogram import Router
from aiogram.types import Message

from database.db import (
    update_user_balance,
    update_user_stats,
    get_user_by_id,
    update_role_stats  # <--- додали!
)
from database.active_players import get_all_active_players

router = Router()
logger = logging.getLogger(__name__)

@router.message()
async def handle_game_end(message: Message):
    if not message.text or "Переможці:" not in message.text:
        return

    logger.info("📩 Обробка кінця гри")

    lines = message.text.splitlines()
    winners = []

    for line in lines:
        match = re.match(r"• \[(.+?)\]\(tg://user\?id=(\d+)\)\s+—\s+@?(\w+)?", line)
        if match:
            role = match.group(1)
            user_id = int(match.group(2))
            username = match.group(3)
            winners.append((user_id, username, role))
            logger.info(f"🏆 Переможець: {username} ({user_id}) — роль {role}")

    # Отримати список усіх активних гравців (початок першого дня)
    all_players = await get_all_active_players()
    all_ids = {uid for _, uid in all_players}

    winner_ids = {uid for uid, _, _ in winners}
    loser_ids = all_ids - winner_ids

    # 1. Переможцям +10 бабідонів, +1 перемога, оновлення статистики по ролі
    for user_id, username, role in winners:
        update_user_balance(user_id, 10)
        update_user_stats(user_id, wins=1)
        await update_role_stats(user_id, role=role, won=True)

    # 2. Програвшим +1 поразка, оновлення статистики
    for _, user_id in all_players:
        if user_id not in winner_ids:
            update_user_stats(user_id, losses=1)
            await update_role_stats(user_id, role=None, won=False)  # якщо роль невідома

    logger.info(f"✅ Гру завершено. Переможців: {len(winners)}. Програвших: {len(loser_ids)}")
   