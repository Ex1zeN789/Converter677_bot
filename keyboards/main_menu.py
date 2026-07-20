from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🖼️ Конвертировать изображение")
        ],
        [
            KeyboardButton(text="🎥 Конвертировать видео")
        ],
        [
            KeyboardButton(text="🎵 Конвертировать аудио"),
        ],
        [
            KeyboardButton(text="🪄 Удалить фон")
        ],
    ],
    resize_keyboard=True
)