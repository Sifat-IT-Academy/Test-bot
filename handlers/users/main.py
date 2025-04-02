from loader import dp, qb, bot
from aiogram.types import Message, CallbackQuery
from aiogram import F
from keyboard_buttons.inline.menu import start_test
from aiogram.fsm.context import FSMContext
import asyncio
from keyboard_buttons.default.button import get_test
import random


@dp.message(lambda message: message.text == "Test yechish")
async def test(message: Message):
    await message.answer("Testni tanlang !", reply_markup=get_test())

user_answers = {}
user_polls = {}

@dp.message(lambda message: message.text in list(set(row[0] for row in qb.question_names())))
async def test_start(message: Message, state: FSMContext):
    test_name = message.text
    await state.update_data(test_name=test_name)
    question_number = len(qb.get_questions(test_name))
    text = f"Test nomi: <b>{test_name}</b> [<b>{question_number}</b>] \nTestni boshlash uchun <b>\"Boshlash\"</b> degan tugmani bosing ! \n\n⚠️Eslatma. Xar bir test uchun 30 soniya"
    await message.answer(text, parse_mode="html", reply_markup=start_test)

@dp.callback_query(F.data == "start")
async def start(call: CallbackQuery):
    await call.message.delete()
    