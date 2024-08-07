from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_keyboard_builder(template, messages: list | tuple, call_backs: list[str], sizes: list | None = None):
    builder = InlineKeyboardBuilder()
    for message, call_back in zip(messages, call_backs):
        builder.add(
            InlineKeyboardButton(
                text=message,
                callback_data=template(choice=call_back).pack()
            )
        )
    builder.adjust(*sizes)
    return builder.as_markup()
