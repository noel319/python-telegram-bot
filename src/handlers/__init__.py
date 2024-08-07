# handlers/__init__.py

from aiogram import Dispatcher
from .start import router as start_router
from .help import router as help_router

def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(help_router)
