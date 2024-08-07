from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from services.weather_service import get_weather
from services.user_service import add_user, list_users
from models.user import setup_db
from PIL import Image
import io

class Form(StatesGroup):
    name = State()
    age = State()

class WeatherState(StatesGroup):
    city = State()

class ReminderState(StatesGroup):
    waiting_for_response = State()

async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Hi! What's your name?")

async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("How old are you?")

async def process_age_invalid(message: types.Message):
    return await message.reply("Age should be a number. Please enter your age.")

async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
        add_user(message.from_user.id, data['name'], data['age'])
    
    async with state.proxy() as data:
        await message.reply(f"Nice to meet you, {data['name']}! You are {data['age']} years old.")
    
    await state.finish()

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.')

async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    photo_file = await photo.download(destination=io.BytesIO())
    photo_file.seek(0)
    image = Image.open(photo_file)
    width, height = image.size
    await message.reply(f"The image size is {width}x{height} pixels.")

async def list_users_command(message: types.Message):
    users = list_users()
    if not users:
        await message.reply("No users found.")
        return
    
    user_list = "\n".join([f"ID: {user}" for user in users])
    await message.reply(f"Users:\n{user_list}")

async def cmd_weather(message: types.Message):
    await WeatherState.city.set()
    await message.reply("Please enter the name of the city.")

async def process_weather_city(message: types.Message, state: FSMContext):
    city = message.text
    weather_data = get_weather(city)
    if weather_data:
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        await message.reply(f"The current weather in {city} is {temp}°C with {description}.")
    else:
        await message.reply("Sorry, I couldn't retrieve the weather for that city. Please check the city name and try again.")
    await state.finish()

async def ask_question(message: types.Message):
    await message.answer(f"Hello, {message.from_user.username}! How are you today?")
    await ReminderState.waiting_for_response.set()
