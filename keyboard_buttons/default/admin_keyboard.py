from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni"),
            KeyboardButton(text="Reklama yuborish"),
            KeyboardButton(text="Savollar bo'limi"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)

admin_qustions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Savol qo'shish"),
            KeyboardButton(text="🗑 Savolni o'chirish"),
        ],
        [
            KeyboardButton(text="Orqaga qaytish 🔙"),
        ]
        
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)