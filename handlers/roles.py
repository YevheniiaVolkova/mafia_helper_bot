from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.db import get_db

router = Router()

# Приклад: команда, яка показує роль користувача
@router.message(Command("myrole"))
async def show_my_role(message: Message):
    user_id = message.from_user.id
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    role = row["role"] if row else "user"
    await message.answer(f"Ваша роль: {role}")

# Приклад: команда, якою адміністратор може змінити роль іншого користувача
@router.message(Command("setrole"))
async def set_role(message: Message):
    # Очікуємо формат: /setrole <user_id> <role>
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Використання: /setrole <user_id> <роль>")
        return
    user_id, role = args[1], args[2]

    # Тут можна додати перевірку, що виконує цей код лише адміністратор (поки що без перевірки)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, user_id))
    conn.commit()
    await message.answer(f"Роль користувача {user_id} змінена на {role}")

# Ти можеш додати сюди ще більше хендлерів для управління ролями
