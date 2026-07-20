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
        [
            KeyboardButton(text="📄 Конвертировать в PDF")
        ],
        [
            KeyboardButton(text="📝 Распознать текст"),
        ],
    ],
    resize_keyboard=True
)