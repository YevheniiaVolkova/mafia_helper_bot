from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any
from database import is_banned

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if is_banned(user_id):
            await event.answer("⛔️ Ви заблоковані і не можете користуватись ботом.")
            return  # Не передаємо далі
        return await handler(event, data)
