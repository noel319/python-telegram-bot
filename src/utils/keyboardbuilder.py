from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def keyboard_builder(messages: list, sizes: list | None = None):
    builder = ReplyKeyboardBuilder()
    for message in messages:
        builder.add(
            KeyboardButton(text=message)
        )
    builder.adjust(*sizes)
    return builder.as_markup(resize_keyboard=True)

