import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from PIL import Image

from states.converter import ImageConverter
from keyboards.inline_formats import get_formats_keyboard
from keyboards.main_menu import main_keyboard
from services.image_service import convert_image

router = Router()

os.makedirs("temp", exist_ok=True)


# ==========================
# Получение фотографии
# ==========================

@router.message(ImageConverter.waiting_image, F.photo)
async def receive_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]

    file = await message.bot.get_file(photo.file_id)

    uid = str(uuid.uuid4())
    input_path = f"temp/{uid}.jpg"

    await message.bot.download_file(
        file.file_path,
        destination=input_path
    )

    await state.update_data(image=input_path)
    await state.set_state(ImageConverter.waiting_action)

    await message.answer(
        "✅ Фото получено!\n\nВыберите формат:",
        reply_markup=get_formats_keyboard()
    )


# ==========================
# Получение документа
# ==========================

@router.message(ImageConverter.waiting_image, F.document)
async def receive_document(message: Message, state: FSMContext):
    document = message.document

    file = await message.bot.get_file(document.file_id)

    ext = document.file_name.split(".")[-1]

    uid = str(uuid.uuid4())
    input_path = f"temp/{uid}.{ext}"

    await message.bot.download_file(
        file.file_path,
        destination=input_path
    )

    await state.update_data(image=input_path)
    await state.set_state(ImageConverter.waiting_action)

    await message.answer(
        "✅ Изображение получено!\n\nВыберите формат:",
        reply_markup=get_formats_keyboard()
    )


# ==========================
# Конвертация
# ==========================

@router.callback_query(ImageConverter.waiting_action)
async def convert(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    input_path = data["image"]

    formats = {
        "format_png": "PNG",
        "format_jpg": "JPEG",
        "format_webp": "WEBP",
        "format_pdf": "PDF",
    }

    output_format = formats[callback.data]

    uid = str(uuid.uuid4())

    ext = output_format.lower()
    if ext == "jpeg":
        ext = "jpg"

    output_path = f"temp/{uid}.{ext}"

    await callback.message.edit_text("⏳ Конвертирую...")

    if output_format == "PDF":
        image = Image.open(input_path)
        image = image.convert("RGB")
        image.save(output_path, "PDF")
    else:
        convert_image(
            input_path,
            output_path,
            output_format
        )

    await callback.message.edit_text("📤 Отправляю файл...")

    await callback.message.answer_document(
        document=FSInputFile(output_path),
        caption=(
            f"✅ Конвертация завершена!\n\n"
            f"📁 Формат: {output_format}\n\n"
            "Выберите следующее действие 👇"
        ),
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await callback.message.edit_text("✅ Конвертация завершена.")