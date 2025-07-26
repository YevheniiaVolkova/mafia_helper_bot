import logging
from aiogram import Router
from aiogram.types import Message

router = Router()
logger = logging.getLogger(__name__)

@router.message()
async def handle_alive_players_message(message: Message):
    if not message.text or not message.text.startswith("Живі гравці:"):
        return

    logger.info(f"Отримано повідомлення з текстом: {message.text}")
    logger.info(f"Entities у повідомленні: {message.entities}")

    if not message.entities:
        logger.warning(f"⚠️ Повідомлення не містить entities: message_id={message.message_id}")
        return

    players = []
    for entity in message.entities:
        if entity.type == "text_mention":
            user = entity.user
            if user:
                username = user.username or user.full_name
                players.append((username, user.id))
                logger.info(f"Знайдено text_mention: username={username}, user_id={user.id}")
        elif entity.type == "mention":
            offset = entity.offset
            length = entity.length
            username = message.text[offset+1 : offset+length]  # без @
            players.append((username, None))  # user_id невідомий
            logger.info(f"Знайдено mention: username={username} (user_id невідомий)")

    if players:
        from database.active_players import save_active_players  # правильний імпорт

        players_with_id = [p for p in players if p[1] is not None]

        if players_with_id:
            save_active_players(players_with_id)
            logger.info(f"✅ Збережено {len(players_with_id)} активних гравців у БД з повідомлення: {message.message_id}")
        else:
            logger.warning(f"⚠️ Не знайдено активних гравців з user_id в повідомленні: {message.message_id}")
    else:
        logger.warning(f"⚠️ Не знайдено жодного активного гравця в повідомленні: {message.message_id}")
