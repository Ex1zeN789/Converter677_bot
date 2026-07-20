from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

format_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🟢 PNG"),
            KeyboardButton(text="🔵 JPG"),
        ],
        [
            KeyboardButton(text="🟣 WEBP"),
        ],
        [
            KeyboardButton(text="🔙 Назад"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите формат"
)