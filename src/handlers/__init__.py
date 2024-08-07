# handlers/__init__.py

from aiogram import Dispatcher
from .start import router as start_router
from .help import router as help_router
from .echo import router as echo_router
from .inline_buttons import router as inline_buttons_router
from .fsm_handler import router as fsm_handler_router
from .img_handler import router as img_handler_router
from .users import router as users_router

def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(echo_router)
    dp.include_router(inline_buttons_router)
    dp.include_router(fsm_handler_router)
    dp.include_router(img_handler_router)
    dp.include_router(users_router)
