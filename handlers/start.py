from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в Converter677 Bot!\n\n"
        "Выберите нужное действие 👇",
        reply_markup=main_keyboard
    )