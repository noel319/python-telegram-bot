from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.middleware.reminder_middleware import ReminderMiddleware
import logging

# Initialize bot and dispatcher
bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

# Add handlers to dispatcher using the utility function
from src.utils.set_bot_commands import register_handlers
register_handlers(dp)

# Error handler
@dp.errors_handler()
async def error_handler(update, exception):
    if isinstance(exception, Exception):
        logging.error(f"An error occurred: {exception}")
        try:
            await bot.send_message(update.message.chat.id, "An error occurred, try again later.")
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    return True

if __name__ == '__main__':
    # Setup database
    from models.db import setup_db
    setup_db()

    # Setup scheduler
    scheduler.start()

    # Add middleware
    dp.middleware.setup(ReminderMiddleware())

    # Start polling
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
