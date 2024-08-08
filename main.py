# main.py

import asyncio
from bot import bot, dp
from src.handlers import register_handlers
from src.utils.scheduler import start_scheduler, response_scheduler
from src.middleware.response_tracker import setup_middleware

async def main():
    register_handlers(dp)
    setup_middleware(dp, scheduler=response_scheduler)
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
