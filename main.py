from bot import dp
from aiogram import executor

if __name__ == '__main__':
    from src.models.user import setup_db
    setup_db()
    executor.start_polling(dp, skip_updates=True)
