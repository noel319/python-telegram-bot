# handlers/start.py

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Choice 1", callback_data="choice_1")],
        [InlineKeyboardButton(text="Choice 2", callback_data="choice_2")]
    ])
    await message.answer("Welcome to our bot! Please choose an option:", reply_markup=keyboard)
