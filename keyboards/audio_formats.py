from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

audio_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🟢 MP3"),
            KeyboardButton(text="🔵 WAV")
        ],
        [
            KeyboardButton(text="🟣 FLAC"),
            KeyboardButton(text="🟠 OGG")
        ],
        [
            KeyboardButton(text="🟡 M4A")
        ]
    ],
    resize_keyboard=True
)