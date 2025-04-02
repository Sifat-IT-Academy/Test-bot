from aiogram.types import Message, ContentType, CallbackQuery
from loader import dp, bot, ADMINS, private
from aiogram.fsm.context import FSMContext
from keyboard_buttons.default.button import menu_button
from aiogram import F
import logging
from aiogram import types
from states.help_stt import AdminStates, AdminStates, create_inline_keyboard
# from aiogram.filters import Command
# from states.help_stt import Help


# @dp.message(Command("xabar"), private)
# async def help_commands(message:Message,state:FSMContext):
#     await message.answer("Xabaringizni yozib ✍🏻 \nMurojatingiz 👤 adminga boradi !")
#     await state.set_state(Help.help)

# @dp.message(Help.help)
# async def send_advert(message: Message, state: FSMContext):
#     help_text = message.text
#     from_chat_id = message.from_user.id

#     text = f"📬 ... Botdan murojat keldi!\n\n📜 Xabar: {help_text}"
#     await bot.send_message(chat_id=ADMINS[0], text=text)
#     await bot.copy_message(chat_id=ADMINS[0], from_chat_id=from_chat_id, message_id=message.message_id)
#     await message.answer("Sizning xabaringiz adminga yuborildi ✅")
#     await state.clear()

@dp.message(F.text == "Savol❓ va Takliflar 📝")
async def admin_message(message: Message, state: FSMContext):
    await message.answer("Admin uchun xabar yuboring:",reply_markup=menu_button)
    await state.set_state(AdminStates.waiting_for_admin_message)

@dp.message(AdminStates.waiting_for_admin_message, F.content_type.in_([
    ContentType.TEXT, ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO,
    ContentType.PHOTO, ContentType.ANIMATION, ContentType.STICKER, 
    ContentType.LOCATION, ContentType.DOCUMENT, ContentType.CONTACT,
    ContentType.VIDEO_NOTE
]))

async def handle_admin_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or "" 

    if username:
        user_identifier = f"@{username}"
    else:
        user_identifier = f"{first_name} {last_name}".strip() 

    video_note = message.video_note
    inline_keyboard = create_inline_keyboard(user_id)
    for admin_id in ADMINS:
        try:
            if video_note:
                await bot.send_video_note(
                    admin_id,
                    video_note.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.text:
                await bot.send_message(
                    admin_id,
                    f"Foydalanuvchi: {user_identifier}\nXabar:\n{message.text}",
                    reply_markup=inline_keyboard
                )
            elif message.audio:
                await bot.send_audio(
                    admin_id,
                    message.audio.file_id,
                    caption=f"Foydalanuvchi: {user_identifier}\nAudio xabar",
                    reply_markup=inline_keyboard
                )
            elif message.voice:
                await bot.send_voice(
                    admin_id,
                    message.voice.file_id,
                    caption=f"Foydalanuvchi: {user_identifier}\nVoice xabar",
                    reply_markup=inline_keyboard
                )
            elif message.video:
                await bot.send_video(
                    admin_id,
                    message.video.file_id,
                    caption=f"Foydalanuvchi: {user_identifier}\nVideo xabar",
                    reply_markup=inline_keyboard
                )
            elif message.photo:
                await bot.send_photo(
                    admin_id,
                    message.photo[-1].file_id,  # using the highest resolution photo
                    caption=f"Foydalanuvchi: {user_identifier}\nRasm xabar",
                    reply_markup=inline_keyboard
                )
            elif message.animation:
                await bot.send_animation(
                    admin_id,
                    message.animation.file_id,
                    caption=f"Foydalanuvchi: {user_identifier}\nGIF xabar",
                    reply_markup=inline_keyboard
                )
            elif message.sticker:
                await bot.send_sticker(
                    admin_id,
                    message.sticker.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.location:
                await bot.send_location(
                    admin_id,
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    reply_markup=inline_keyboard
                )
            elif message.document:
                await bot.send_document(
                    admin_id,
                    message.document.file_id,
                    caption=f"Foydalanuvchi: {user_identifier}\nHujjat xabar",

                    reply_markup=inline_keyboard
                )
            elif message.contact:
                await bot.send_contact(
                    admin_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name,
                    last_name=message.contact.last_name or "",
                    reply_markup=inline_keyboard
                )
        except Exception as e:
            logging.error(f"Error sending message to admin {admin_id}: {e}")

    await state.clear()
    await bot.send_message(user_id, "Admin sizga javob berishi mumkin.",reply_markup=menu_button)

# Callback query handler for the reply button
@dp.callback_query(lambda c: c.data.startswith('reply:'))
async def process_reply_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = int(callback_query.data.split(":")[1])
    await callback_query.message.answer("Javobingizni yozing. Sizning javobingiz foydalanuvchiga yuboriladi.")
    await state.update_data(reply_user_id=user_id)
    await state.set_state(AdminStates.waiting_for_reply_message)
    await callback_query.answer()

# Handle admin reply and send it back to the user
@dp.message(AdminStates.waiting_for_reply_message)
async def handle_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    original_user_id = data.get('reply_user_id')

    if original_user_id:
        try:
            if message.text:
                await bot.send_message(original_user_id, f"Admin javobi:\n{message.text}", reply_markup=menu_button)
            
            elif message.voice:
                await bot.send_voice(original_user_id, message.voice.file_id, reply_markup=menu_button)

            elif message.video_note:
                await bot.send_video_note(original_user_id, message.video_note.file_id, reply_markup=menu_button)

            elif message.audio:
                await bot.send_audio(original_user_id, message.audio.file_id, reply_markup=menu_button)
            
            elif message.sticker:
                await bot.send_sticker(original_user_id, message.sticker.file_id, reply_markup=menu_button)
            
            elif message.video:
                await bot.send_video(original_user_id, message.video.file_id, reply_markup=menu_button)

            await state.clear()  # Clear state after sending the reply
        except Exception as e:
            logging.error(f"Error sending reply to user {original_user_id}: {e}")
            await message.reply("Xatolik: Javob yuborishda xato yuz berdi.")
    else:
        await message.reply("Xatolik: Javob yuborish uchun foydalanuvchi ID topilmadi.")
