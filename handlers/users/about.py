from aiogram.types import Message
from loader import dp, private
from aiogram.filters import Command

#about commands
@dp.message(Command("about"), private)
async def about_commands(message:Message):
    await message.answer("🤖 TestBot — bu bilimlaringizni sinab ko‘rish uchun maxsus yaratilgan bot! \nSizga turli mavzularda test savollari taqdim etiladi. Har bir test natijasida to‘g‘ri va noto‘g‘ri javoblaringizni ko‘rib, o‘zingizni sinab ko‘rishingiz mumkin.")

