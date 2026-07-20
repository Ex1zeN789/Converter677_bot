from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import main_keyboard
from states.converter import ImageConverter

router = Router()


@router.message(F.text == "🖼️ Конвертировать изображение")
async def image_menu(message: Message, state: FSMContext):

    await state.set_state(ImageConverter.waiting_image)

    await message.answer(
        "📤 Отправьте изображение (фото или документ).\n\n"
        "После загрузки вы сможете выбрать формат."
    )


@router.message(F.text == "🏠 Главное меню")
async def home(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_keyboard
    )