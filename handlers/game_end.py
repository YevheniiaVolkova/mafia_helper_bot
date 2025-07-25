from aiogram import Router, types, Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from database.users import update_game_result_by_id

router = Router()

@router.message()
async def handle_game_end_message(message: Message, bot: Bot):
    if not message.text or not message.text.startswith("Гру закінчено!"):
        return

    entities = message.entities or []
    text = message.text

    winners_ids = []
    losers_ids = []

    # Знаходимо індекси початку секцій "Переможці:" і "Решта учасників:"
    winners_start = text.find("Переможці:")
    others_start = text.find("Решта учасників:")

    if winners_start == -1 or others_start == -1:
        await message.answer("⚠️ Не вдалося знайти розділи 'Переможці' або 'Решта учасників'.")
        return

    # Витягуємо user_id з text_mention (згадок з користувачами)
    for entity in entities:
        if entity.type == "text_mention" and entity.user:
            offset = entity.offset
            if winners_start < offset < others_start:
                winners_ids.append(entity.user.id)
            elif offset > others_start:
                losers_ids.append(entity.user.id)

    # Оновлюємо статистику у базі
    for uid in winners_ids:
        await update_game_result_by_id(uid, win=True)
        await notify_winner(bot, uid)

    for uid in losers_ids:
        await update_game_result_by_id(uid, win=False)

    await message.answer("✅ Результати гри збережено. Перемог: +1 / Поразок: +1")


# 📨 Надіслати повідомлення переможцю в приват
async def notify_winner(bot: Bot, user_id: int):
    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "🏆 Ви перемогли в грі!\n"
                "💰 Вам нараховано +10 бабідонів.\n"
                "📈 Ваша статистика оновлена."
            )
        )
    except TelegramForbiddenError:
        print(f"❗️ Бот заблокований користувачем {user_id}, не вдалося надіслати повідомлення.")
