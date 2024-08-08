# scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from src.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

async def send_reminder():
    chat_ids = get_all_user_ids()  # Function to get all user IDs from the database
    for chat_id in chat_ids:
        await bot.send_message(chat_id, "Don’t forget to check your notifications!")

def get_all_user_ids():
    import sqlite3
    from contextlib import closing
    DB_NAME = "db/bot_users.db"
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with connection as conn:
            return [row[0] for row in conn.execute('SELECT user_id FROM users').fetchall()]

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, CronTrigger(hour=9, minute=0))
    scheduler.start()

def response_scheduler():
    scheduler =AsyncIOScheduler()
    scheduler.start()