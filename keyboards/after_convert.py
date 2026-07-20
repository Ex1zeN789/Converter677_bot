from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

after_convert_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Конвертировать ещё")],
        [KeyboardButton(text="🏠 Главное меню")]
    ],
    resize_keyboard=True
)