# handlers/help.py

from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer("Available commands: /start, /help, /echo, /photo /weather /chat /users /")
