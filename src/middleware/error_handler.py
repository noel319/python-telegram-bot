# middleware/error_handler.py

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Update
from loguru import logger

class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except TelegramAPIError as e:
            logger.error(f"TelegramAPIError: {e}")
            if isinstance(event, Update):
                if event.message:
                    await event.message.answer("An error occurred, try again later")
                elif event.callback_query:
                    await event.callback_query.message.answer("An error occurred, try again later")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if isinstance(event, Update):
                if event.message:
                    await event.message.answer("An error occurred, try again later")
                elif event.callback_query:
                    await event.callback_query.message.answer("An error occurred, try again later")
            raise e  # Re-raise the exception to ensure it's logged

# Middleware setup
def setup_error_handling(dp):
    dp.update.middleware(ErrorHandlerMiddleware())
