import asyncio
from aiogram import F
from loader import dp,qb, ADMINS
from filters.admin import IsBotAdminFilter
from states.add_questions import Questions
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery
from keyboard_buttons.default.button import get_buttun
from keyboard_buttons.inline.menu import number, option, ask
from keyboard_buttons.default.admin_keyboard import admin_qustions, admin_button

@dp.message(F.text=="Savollar bo'limi", IsBotAdminFilter(ADMINS))
async def questions_menu(message:Message):
    await message.answer("Savollar bo'limi", reply_markup=admin_qustions)

@dp.message(F.text=="Orqaga qaytish 🔙", IsBotAdminFilter(ADMINS))
async def back(message:Message, state:FSMContext):
    await message.answer("Menu", reply_markup=admin_button)
    await state.clear()

@dp.message(F.text=="➕ Savol qo'shish", IsBotAdminFilter(ADMINS))
async def add_questions(message:Message, state:FSMContext):
    await message.answer("<b>🗂 Yangi savollar to'plamini yaratish uchun nom kiriting \nyoki Tugmalardan birini tanling</b>", parse_mode="html", reply_markup=get_buttun())
    await state.set_state(Questions.test_name)

# Start: Test nomini olish
@dp.message(F.text, Questions.test_name,IsBotAdminFilter(ADMINS))
async def test_name(message:Message, state:FSMContext):
    test_name = message.text
    await state.update_data(test_name=test_name)

    question_number = qb.test_number(test_name)
    question_count = len(qb.get_questions(test_name))
    
    if question_count == question_number[0][0]:
        answer_text = f"Siz ushbu testga {question_number[0][0]} ta test qo'shib bo'lgansiz bundan ko'p qo'sha olmaysiz ❗️"
        await message.answer(answer_text)
        await state.clear()

    elif question_number:
        numbers = question_number[0][0]
        await state.update_data(number_question=numbers)
        data = await state.get_data()
        test_name = data.get("test_name")
        text = f"{question_count + 1} savolni yozing ✍️ yoki rasm kiriting 🖼"
        await message.answer(text)
        await state.set_state(Questions.question)
    else:
        await message.answer(text="Toplamda necha savol bo'ladi ?", reply_markup=number)
        await state.set_state(Questions.number_question)


@dp.message(Questions.test_name)
async def test_name_del(message:Message, state:FSMContext):
    await message.answer(text= "Faqat matn yozing, boshqa fayllar mumkin emas ! ")
    await message.delete()

# Start: Savollar sonini olish
@dp.callback_query(F.data, Questions.number_question,IsBotAdminFilter(ADMINS))
async def numbers_question(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    number_question = call.data
    await state.update_data(number_question=number_question)

    data = await state.get_data()
    test_name = data.get("test_name")
    question_number = len(qb.get_questions(test_name))
    text = f"{question_number + 1} savolni yozing ✍️ yoki rasm kiriting 🖼"
    await call.message.answer(text)
    await state.set_state(Questions.question)

@dp.message(Questions.number_question)
async def numbers_question_del(message:Message, state:FSMContext):
    await message.answer(text= "Tugmadan birini tanlang !")
    await message.delete()

# Start: Savolni olish
@dp.message(F.text | F.photo, Questions.question, IsBotAdminFilter(ADMINS))
async def question(message:Message, state:FSMContext):
    if message.photo:
        photo = message.photo[-1].file_id
        await state.update_data(question=photo)

    elif message.text:
        question = message.text
        await state.update_data(question=question)

    await message.answer(text="A variant javobini yozing !")
    await state.set_state(Questions.a)

@dp.message(Questions.question)
async def question_del(message:Message, state:FSMContext):
    await message.answer(text= "Faqat matn yozing yoki rasm kiriting, boshqa fayllar mumkin emas ! ")
    await message.delete()

# Start: A javobini olish
@dp.message(F.text, Questions.a, IsBotAdminFilter(ADMINS))    
async def a(message:Message, state:FSMContext):
    a = message.text.upper()
    await state.update_data(a=a)
    await message.answer(text="B variant javobini yozing !")
    await state.set_state(Questions.b)

@dp.message(Questions.a)
async def a_del(message:Message, state:FSMContext):
    await message.answer(text= "Faqat matn yozing, boshqa fayllar mumkin emas ! ")
    await message.delete()

# Start: B javobini olish
@dp.message(F.text, Questions.b, IsBotAdminFilter(ADMINS))
async def b(message:Message, state:FSMContext):
    b = message.text.upper()
    await state.update_data(b=b)
    await message.answer(text="C variant javobini yozing !")
    await state.set_state(Questions.c)

@dp.message(Questions.b)
async def b_del(message:Message, state:FSMContext):
    await message.answer(text= "Faqat matn yozing, boshqa fayllar mumkin emas ! ")
    await message.delete()

# Start: C javobini olish
@dp.message(F.text, Questions.c, IsBotAdminFilter(ADMINS))
async def c(message:Message, state:FSMContext):
    c = message.text.upper()
    await state.update_data(c=c)
    await message.answer(text="D variant javobini yozing !")
    await state.set_state(Questions.d)

@dp.message(Questions.c)
async def c_del(message:Message, state:FSMContext):
    await message.answer(text= "Faqat matn yozing, boshqa fayllar mumkin emas ! ")
    await message.delete()

# Start: D javobini olish
@dp.message(F.text, Questions.d, IsBotAdminFilter(ADMINS))
async def d(message: Message, state: FSMContext):    
    d = message.text.upper()
    await state.update_data(d=d)
    await message.answer(text="Javobni tanlang !", reply_markup=option)
    await state.set_state(Questions.answer)

@dp.message(Questions.d)
async def d_del(message:Message, state:FSMContext):
    await message.answer(text= "Faqat matn yozing, boshqa fayllar mumkin emas ! ")
    await message.delete()

# Start: To'g'ri javobni tanlash
@dp.callback_query(F.data, Questions.answer, IsBotAdminFilter(ADMINS))
async def answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    test_name = data.get("test_name")
    number_question = data.get("number_question")
    question = data.get("question")
    a = data.get("a")
    b = data.get("b")
    c = data.get("c")
    d = data.get("d")
    answer = callback.data

    qb.add_questions(
        test_name=test_name, 
        number_question=number_question,
        question=question, 
        a=a, b=b, c=c, d=d, 
        answer=answer
    )
    message_del = await callback.message.answer("Savol qo'shildi 🎉")
    await state.clear()
    await callback.message.answer("Savolni qo'shishni davom etasizmi ?", reply_markup=ask)
    await asyncio.sleep(3)
    await message_del.delete()

@dp.message(Questions.answer)
async def answer_del(message:Message, state:FSMContext):
    await message.answer(text= "Tugmadan birini tanlang ! ")
    await message.delete()

# Start: Yangi savol qo'shish yoki bekor qilish
@dp.callback_query(F.data == "true", IsBotAdminFilter(ADMINS))
async def add_another_question(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("<b>🗂 Yangi savollar to'plamini yaratish uchun nom kiriting \nyoki Tugmalardan birini tanling</b>", parse_mode="html", reply_markup=get_buttun())
    await state.set_state(Questions.test_name)

@dp.callback_query(F.data == "false", IsBotAdminFilter(ADMINS))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Menu", reply_markup=get_buttun())
    await state.clear()
