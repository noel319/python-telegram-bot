from aiogram import Dispatcher
from routes.handlers import (cmd_start, process_name, process_age_invalid, process_age,
                             cancel_handler, handle_photo, list_users_command, cmd_weather, 
                             process_weather_city, ask_question)
from routes.handlers import Form, WeatherState, ReminderState

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(process_name, state=Form.name)
    dp.register_message_handler(process_age_invalid, lambda message: not message.text.isdigit(), state=Form.age)
    dp.register_message_handler(process_age, lambda message: message.text.isdigit(), state=Form.age)
    dp.register_message_handler(cancel_handler, commands='cancel', state='*')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(handle_photo, content_types=['photo'])
    dp.register_message_handler(list_users_command, commands='users')
    dp.register_message_handler(cmd_weather, commands='weather')
    dp.register_message_handler(process_weather_city, state=WeatherState.city)
    dp.register_message_handler(ask_question, commands='ask')
