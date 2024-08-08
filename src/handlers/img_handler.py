# handlers/img_handler.py

from aiogram import types, Router
from aiogram.types import ContentType
from aiogram.filters import Command
from PIL import Image
import aiohttp
import io

router = Router()

@router.message(Command(ContentType.PHOTO))
async def handle_image(message: types.Message):
    try:
        photo = message.photo[-1]
        file_info = await message.bot.get_file(photo.file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{message.bot.token}/{file_path}"

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    data = await response.read()
                    image = Image.open(io.BytesIO(data))
                    width, height = image.size
                    await message.answer(f"Image dimensions: {width} x {height} pixels")
                else:
                    await message.answer("Failed to retrieve image")
    except Exception as e:
        await message.answer("An error occurred while processing the image.")
        print(f"Error: {e}") 
