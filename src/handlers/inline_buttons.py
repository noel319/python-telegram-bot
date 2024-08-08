# handlers/inline_buttons.py

from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Choice 1", callback_data="choice_1")],
        [InlineKeyboardButton(text="Choice 2", callback_data="choice_2")]
    ])
    await message.answer("Welcome to our bot! Please choose an option:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data in ["choice_1", "choice_2"])
async def process_callback(callback_query: types.CallbackQuery):
    choice = callback_query.data
    if choice == "choice_1":
        await callback_query.message.answer("You have selected Choice 1")
    elif choice == "choice_2":
        await callback_query.message.answer("You have selected Choice 2")
    await callback_query.answer()  # Acknowledge the callback query
