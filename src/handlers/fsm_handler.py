# handlers/fsm_handler.py

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from src.utils.fsm import UserData

router = Router()

@router.message(Command("chat"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Hi! What's your name?")
    await state.set_state(UserData.waiting_for_name)

@router.message(UserData.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("How old are you?")
    await state.set_state(UserData.waiting_for_age)

@router.message(UserData.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    await message.answer(f"Your name is {user_data['name']} and you are {user_data['age']} years old.")
    await state.clear()
