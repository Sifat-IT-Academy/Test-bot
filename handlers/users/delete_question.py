
from aiogram import F
from loader import dp, qb, ADMINS
from aiogram.fsm.context import FSMContext
from filters.admin import IsBotAdminFilter
from states.all_questions import DeleteQuestions
from aiogram.types import Message, CallbackQuery
from keyboard_buttons.inline.menu import delete_ask
from keyboard_buttons.default.button import get_buttun
from keyboard_buttons.default.admin_keyboard import admin_qustions

@dp.message(F.text=="🗑 Savolni o'chirish", IsBotAdminFilter(ADMINS))
async def delete_questions(message:Message, state:FSMContext):
    await message.answer("O'chirmoqchi bo'lgan savol turini tanlang", parse_mode="html", reply_markup=get_buttun())
    await state.set_state(DeleteQuestions.test_name)

@dp.message(DeleteQuestions.test_name, lambda message: message.text in list(set(row[0] for row in qb.question_names())), IsBotAdminFilter(ADMINS))
async def delete_test_name(message: Message, state: FSMContext):
    test_name = message.text
    await state.update_data(test_name=test_name)
    text = f"{test_name} savollar bo'limi o'chirilsinmi ?"
    await message.answer(text, reply_markup=delete_ask)

@dp.callback_query(F.data == "del_true", IsBotAdminFilter(ADMINS))
async def delete_test(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    test_name = data.get("test_name")
    qb.delete_questions(test_name=test_name)
    await callback.message.answer("Savollar o'chirildi 🎉", reply_markup = admin_qustions)
    await state.clear()

@dp.callback_query(F.data == "del_false", IsBotAdminFilter(ADMINS))
async def undelete_test(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Savollar o'chirilmadi", reply_markup = admin_qustions)
    await state.clear()