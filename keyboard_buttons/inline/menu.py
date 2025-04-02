from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

number = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="10", callback_data="10"),
            InlineKeyboardButton(text="20", callback_data="20"),
            InlineKeyboardButton(text="30", callback_data="30"),
        ]
    ]
)

option = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data="A"), 
            InlineKeyboardButton(text="B", callback_data="B"), 
            InlineKeyboardButton(text="C", callback_data="C"), 
            InlineKeyboardButton(text="D", callback_data="D"), 
        ]
    ]
)

ask = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="true"), 
            InlineKeyboardButton(text="❌", callback_data="false"), 
        ]
    ]
)

start_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Boshlash", callback_data="start"), 
            InlineKeyboardButton(text="Bekor qilish", callback_data="false"), 
        ]
    ]
)
