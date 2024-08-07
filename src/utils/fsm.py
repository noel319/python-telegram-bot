# utils/fsm.py

from aiogram.fsm.state import State, StatesGroup

class UserData(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
