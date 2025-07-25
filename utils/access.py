from aiogram import Bot
from aiogram.types import ChatMember

async def is_chat_admin(bot: Bot, user_id: int, chat_id: int) -> bool:
    """
    Перевіряє, чи є користувач адміністратором у вказаному чаті.
    """
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Додаткова функція для перевірки прав користувача у чаті.
    Можна розширити для різних ролей (admin/moderator/user).
    Зараз просто перевіряє, чи є адміністратором.
    """
    return await is_chat_admin(bot, user_id, chat_id)

async def get_user_status(bot: Bot, user_id: int, chat_id: int) -> str:
    """
    Отримує статус користувача в чаті (creator, administrator, member, restricted, left, kicked).
    """
    member: ChatMember = await bot.get_chat_member(chat_id, user_id)
    return member.status
