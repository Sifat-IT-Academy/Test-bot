from loader import dp, qb, bot
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram import F
from keyboard_buttons.inline.menu import start_test
from aiogram.fsm.context import FSMContext
import asyncio
from keyboard_buttons.default.button import get_test
from states.all_questions import TestState  # Yangi TestState ishlatiladi

# Testni boshlash menyusi
@dp.message(lambda message: message.text == "Test yechish")
async def test(message: Message):
    await message.answer("Testni tanlang!", reply_markup=get_test())

# Testni tanlash va tayyorgarlik
@dp.message(lambda message: message.text in list(set(row[0] for row in qb.question_names())))
async def test_start(message: Message, state: FSMContext):
    test_name = message.text
    await state.update_data(test_name=test_name, chat_id=message.chat.id)
    question_number = len(qb.get_questions(test_name))
    text = (
        f"Test nomi: <b>{test_name}</b> [<b>{question_number}</b>] \n"
        "Testni boshlash uchun <b>\"Boshlash\"</b> degan tugmani bosing! \n\n"
        "⚠️Eslatma: Har bir savol uchun 30 soniya"
    )
    await message.answer(text, reply_markup=start_test, parse_mode="html")

# Testni boshlash
@dp.callback_query(F.data == "start")
async def start_tests(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    test_name = data.get("test_name")
    questions = qb.get_questions(test_name)
    await state.update_data(questions=questions, current_index=0, correct=0)
    await state.set_state(TestState.testing)


    chat_id = data.get("chat_id")
    msg = await bot.send_message(chat_id, "Testni boshlash uchun 30 soniya ⏳")

    # 30 soniyalik countdown
    for i in range(30, 0, -1):
        await asyncio.sleep(1)
        try:
            await msg.edit_text(f"Testni boshlash ⏳ {i}")
        except:
            pass

    await msg.edit_text("Test boshlandi ✅")
    await send_question(chat_id, state)

# Savol yuborish funksiyasi
async def send_question(chat_id, state: FSMContext):
    data = await state.get_data()
    questions = data.get("questions")
    current_index = data.get("current_index", 0)

    # Agar barcha savollar tugagan bo'lsa, testni yakunlaymiz
    if current_index >= len(questions):
        correct = data.get("correct", 0)
        total = len(questions)
        await bot.send_message(chat_id, f"Test tugadi! To'g'ri javoblar: {correct}/{total}")
        await state.clear() 
        return

    # Joriy savolni olish
    question_data = questions[current_index]
    _, _, types, question, A, B, C, D, answer = question_data
    options = [A, B, C, D]
    correct_option_id = ["A", "B", "C", "D"].index(answer)

    # Savolni yuborish
    if types == "text":
        poll_message = await bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False,
            open_period=30
        )
    elif types == "photo":
        await bot.send_photo(chat_id, photo=question, caption="Quyidagi savolga javob bering:")
        poll_message = await bot.send_poll(
            chat_id=chat_id,
            question="Javobni tanlang",
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False,
            open_period=30
        )

    # Poll ID va timeout taskni saqlash
    poll_id = poll_message.poll.id
    timeout_task = asyncio.create_task(timeout_handler(chat_id, state, current_index))
    await state.update_data(current_poll_id=poll_id, timeout_task=timeout_task)

# Timeout handler (30 soniya o'tganda keyingi savolga o'tish)
async def timeout_handler(chat_id, state: FSMContext, index):
    await asyncio.sleep(30)
    data = await state.get_data()
    if data.get("current_index") == index:  # Agar joriy savol o'zgarmagan bo'lsa
        await state.update_data(current_index=index + 1)
        await send_question(chat_id, state)

# Javobni qayta ishlash
@dp.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    current_poll_id = data.get("current_poll_id")

    if poll_answer.poll_id != current_poll_id:
        return

    timeout_task = data.get("timeout_task")
    if timeout_task and not timeout_task.done():
        timeout_task.cancel()

    questions = data.get("questions")
    current_index = data.get("current_index")
    question_data = questions[current_index]
    _, _, _, _, A, B, C, D, answer = question_data
    options = [A, B, C, D]
    
    # To'g'ri indexni belgilar asosida olish
    correct_option_id = ["A", "B", "C", "D"].index(answer)
    
    selected_option_id = poll_answer.option_ids[0] if poll_answer.option_ids else -1

    if selected_option_id == correct_option_id:
        data["correct"] = data.get("correct", 0) + 1

    data["current_index"] = current_index + 1
    await state.update_data(**data)
    chat_id = data.get("chat_id")
    await send_question(chat_id, state)