# middleware/response_tracker.py

from aiogram import BaseMiddleware, types, Bot
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from src.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

class ResponseTrackerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self.scheduler = scheduler

    async def __call__(self, handler, event, data):
        if isinstance(event, types.Message) and event.text:
            state: FSMContext = data['state']
            state_data = await state.get_data()

            if 'waiting_for_response' in state_data:
                self.scheduler.remove_job(state_data['job_id'])
                await state.update_data(waiting_for_response=False, job_id=None)

        await handler(event, data)

    async def schedule_reminder(self, chat_id: int, user_name: str, delay: int = 15):
        trigger_time = datetime.now() + timedelta(minutes=delay)
        job_id = f"reminder_{chat_id}"
        self.scheduler.add_job(
            self.send_reminder,
            DateTrigger(run_date=trigger_time),
            args=[chat_id, user_name],
            id=job_id,
            replace_existing=True
        )
        return job_id

    async def send_reminder(self, chat_id: int, user_name: str):
        await bot.send_message(chat_id, f"You forgot to answer, {user_name}!")

# Middleware setup
def setup_middleware(dp, scheduler):
    dp.message.middleware(ResponseTrackerMiddleware(scheduler))
