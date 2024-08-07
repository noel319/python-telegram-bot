# bot.py

from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
