# handlers/weather.py

import requests
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from src.config import OPENWEATHER_API_KEY

router = Router()

class WeatherStates(StatesGroup):
    waiting_for_city = State()

@router.message(Command("weather"))
async def cmd_weather(message: types.Message, state: FSMContext):
    await message.answer("Please enter the name of the city:")
    await state.set_state(WeatherStates.waiting_for_city)

@router.message(WeatherStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    city_name = message.text
    await state.clear()
    weather_data = get_weather(city_name)
    if weather_data:
        await message.answer(format_weather(weather_data))
    else:
        await message.answer("Sorry, I couldn't fetch the weather for that city. Please try again.")

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def format_weather(weather_data):
    city = weather_data['name']
    temp = weather_data['main']['temp']
    weather = weather_data['weather'][0]['description']
    return f"The current weather in {city}:\nTemperature: {temp}°C\nCondition: {weather}"
