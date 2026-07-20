import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.background import BackgroundRemover
from services.background_service import remove_background
from keyboards.main_menu import main_keyboard

router = Router()

os.makedirs("temp", exist_ok=True)


@router.message(F.text == "🪄 Удалить фон")
async def background_menu(message: Message, state: FSMContext):

    await state.set_state(BackgroundRemover.waiting_image)

    await message.answer(
        "🖼️ Отправьте изображение, у которого нужно удалить фон."
    )


@router.message(BackgroundRemover.waiting_image, F.photo)
async def remove_bg_photo(message: Message, state: FSMContext):

    progress = await message.answer("⏳ Удаляю фон...")

    photo = message.photo[-1]

    file = await message.bot.get_file(photo.file_id)

    uid = str(uuid.uuid4())

    input_path = f"temp/{uid}.jpg"
    output_path = f"temp/{uid}.png"

    await message.bot.download_file(
        file.file_path,
        destination=input_path
    )

    remove_background(
        input_path,
        output_path
    )

    await progress.edit_text("📤 Отправляю изображение...")

    await message.answer_document(
        FSInputFile(output_path),
        caption="✅ Фон успешно удален!",
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await progress.edit_text("✅ Готово!")