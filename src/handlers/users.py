# handlers/users.py

from aiogram import types, Router
from aiogram.filters import Command
from src.utils.database import get_users

router = Router()

@router.message(Command("users"))
async def list_users(message: types.Message):
    users = get_users()
    if users:
        user_list = "\n".join([f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}" for user in users])
        await message.answer(f"Registered Users:\n{user_list}")
    else:
        await message.answer("No users found.")
