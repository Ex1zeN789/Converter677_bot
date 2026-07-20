import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from states.ocr import OCR
from services.ocr_service import recognize_text
from keyboards.main_menu import main_keyboard

router = Router()

os.makedirs("temp", exist_ok=True)


@router.message(F.text == "📝 Распознать текст")
async def ocr_menu(message: Message, state: FSMContext):

    await state.set_state(OCR.waiting_image)

    await message.answer(
        "📷 Отправьте фотографию или изображение с текстом."
    )


@router.message(OCR.waiting_image, F.photo)
async def photo_ocr(message: Message, state: FSMContext):

    progress = await message.answer("⏳ Распознаю текст...")

    photo = message.photo[-1]

    file = await message.bot.get_file(photo.file_id)

    uid = str(uuid.uuid4())

    image_path = f"temp/{uid}.jpg"

    await message.bot.download_file(
        file.file_path,
        destination=image_path
    )

    text = recognize_text(image_path)

    os.remove(image_path)

    if not text.strip():

        await progress.edit_text(
            "❌ Текст не найден."
        )

        await state.clear()

        return

    if len(text) < 3500:

        await message.answer(
            f"📝 Распознанный текст:\n\n{text}",
            reply_markup=main_keyboard
        )

    else:

        txt_path = f"temp/{uid}.txt"

        with open(txt_path, "w", encoding="utf-8") as file:

            file.write(text)

        await message.answer_document(
            FSInputFile(txt_path),
            caption="📝 Распознанный текст",
            reply_markup=main_keyboard
        )

        os.remove(txt_path)

    await progress.edit_text("✅ Готово!")

    await state.clear()


@router.message(OCR.waiting_image, F.document)
async def document_ocr(message: Message, state: FSMContext):

    progress = await message.answer("⏳ Распознаю текст...")

    document = message.document

    ext = document.file_name.split(".")[-1].lower()

    if ext not in ["jpg", "jpeg", "png", "webp"]:

        await progress.edit_text(
            "❌ Поддерживаются только изображения."
        )

        return

    uid = str(uuid.uuid4())

    image_path = f"temp/{uid}.{ext}"

    file = await message.bot.get_file(document.file_id)

    await message.bot.download_file(
        file.file_path,
        destination=image_path
    )

    text = recognize_text(image_path)

    os.remove(image_path)

    if not text.strip():

        await progress.edit_text(
            "❌ Текст не найден."
        )

        await state.clear()

        return

    if len(text) < 3500:

        await message.answer(
            f"📝 Распознанный текст:\n\n{text}",
            reply_markup=main_keyboard
        )

    else:

        txt_path = f"temp/{uid}.txt"

        with open(txt_path, "w", encoding="utf-8") as file:

            file.write(text)

        await message.answer_document(
            FSInputFile(txt_path),
            caption="📝 Распознанный текст",
            reply_markup=main_keyboard
        )

        os.remove(txt_path)

    await progress.edit_text("✅ Готово!")

    await state.clear()