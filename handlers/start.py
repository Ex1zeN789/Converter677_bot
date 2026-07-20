from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🚀 <b>Добро пожаловать в Converter677 Bot!</b>\n\n"

        "🔥 <b>Я умею:</b>\n"
        "🖼️ Конвертировать изображения\n"
        "🎥 Конвертировать видео\n"
        "🎵 Конвертировать аудио\n"
        "🪄 Удалять фон\n\n"

        "⚡ <b>Быстро</b>\n"
        "🔒 <b>Безопасно</b>\n"
        "💯 <b>Бесплатно</b>\n\n"

        "👇 <b>Выберите нужную функцию в меню ниже.</b>",
        reply_markup=main_keyboard,
        parse_mode="HTML"
    )