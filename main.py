# main.py

import asyncio
from bot import bot, dp
from handlers import register_handlers

async def main():
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
