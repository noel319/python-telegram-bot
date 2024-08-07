from aiogram.methods import SetMyCommands
from aiogram.types import BotCommand


async def set_default_commands(bot):
    await bot(
        SetMyCommands(
            commands=[
                BotCommand(command='start', description='Foydalanishni boshlash'),
                BotCommand(command='help', description='Xizmat haqida'),
                BotCommand(command='buy', description='Buyurtma berish'),
                BotCommand(command='terms', description='Foydalanish shartlari'),
                BotCommand(command='support', description='Biz bilan aloqa')
            ]
        )
    )
