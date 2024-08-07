from aiogram import Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()

class ReminderMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        state = Dispatcher.get_current().current_state()
        current_state = await state.get_state()

        if current_state == 'ReminderState:waiting_for_response':
            state_data = await state.get_data()
            reminder_job_id = state_data.get('reminder_job_id')

            if reminder_job_id:
                scheduler.remove_job(reminder_job_id)
                await message.answer("Thank you for responding!")
                await state.finish()

    async def on_post_process_message(self, message: types.Message, results: list, data: dict):
        state = Dispatcher.get_current().current_state()
        current_state = await state.get_state()

        if current_state == 'ReminderState:waiting_for_response':
            reminder_time = datetime.now() + timedelta(minutes=15)
            reminder_job = scheduler.add_job(
                send_reminder_message,
                'date',
                run_date=reminder_time,
                args=[message.chat.id]
            )
            await state.update_data(reminder_job_id=reminder_job.id)

async def send_reminder_message(chat_id):
    bot = Dispatcher.get_current().bot
    await bot.send_message(chat_id, "You forgot to answer.")
