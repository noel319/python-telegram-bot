# handlers/echo.py

from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("echo"))
async def echo_message(message: types.Message):
    if message.text:
        await message.answer(message.text[len("/echo "):])
