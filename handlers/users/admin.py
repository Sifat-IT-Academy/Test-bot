import time 
from aiogram import F
from aiogram.types import Message
from states.reklama import Adverts
from aiogram.filters import Command
from filters.admin import IsBotAdminFilter
from aiogram.fsm.context import FSMContext
from loader import bot,db,dp,ADMINS, private
from keyboard_buttons.default import admin_keyboard


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS), private)
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)

@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS), private)
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS), private)
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()

