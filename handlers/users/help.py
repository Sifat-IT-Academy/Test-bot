from aiogram.types import Message
from loader import dp, private
from aiogram.filters import Command

#help commands
@dp.message(Command("help"), private)
async def help_commands(message:Message):
    await message.answer("🔥 Buyruqlar \nBotdan foydalanish uchun ... \n/about - Bot haqida \nAdmin bilan bog'lanish uchun menu dan \"Admin bilan bog'lanish\" tugmasini bosing \nTest ishlash uchun \Test yechish\" tugmasini bosing")
