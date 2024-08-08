# main.py

import asyncio
from bot import bot, dp
from src.handlers import register_handlers
from src.utils.scheduler import start_scheduler, response_scheduler
from src.middleware.response_tracker import setup_middleware
from src.middleware.error_handler import setup_error_handling
from loguru import logger

logger.add("bot_errors.log", rotation="1 week")  # Log errors to a file, rotating weekly

async def main():
    logger.info("Starting bot...")
    register_handlers(dp)
    setup_middleware(dp, scheduler=response_scheduler)
    setup_error_handling(dp)
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot Stopped!")
