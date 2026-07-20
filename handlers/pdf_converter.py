import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from PIL import Image

from states.pdf_converter import PdfConverter
from keyboards.main_menu import main_keyboard
from services.pdf_service import office_to_pdf

router = Router()

os.makedirs("temp", exist_ok=True)


@router.message(F.text == "📄 Конвертировать в PDF")
async def pdf_menu(message: Message, state: FSMContext):

    await state.set_state(PdfConverter.waiting_file)

    await message.answer(
        "📄 Отправьте файл.\n\n"
        "Поддерживаются:\n"
        "• JPG\n"
        "• PNG\n"
        "• WEBP\n"
        "• DOCX\n"
        "• XLSX\n"
        "• PPTX"
    )


@router.message(PdfConverter.waiting_file, F.photo)
async def photo_to_pdf(message: Message, state: FSMContext):

    progress = await message.answer("⏳ Конвертирую...")

    photo = message.photo[-1]

    file = await message.bot.get_file(photo.file_id)

    uid = str(uuid.uuid4())

    input_path = f"temp/{uid}.jpg"
    output_path = f"temp/{uid}.pdf"

    await message.bot.download_file(file.file_path, input_path)

    image = Image.open(input_path).convert("RGB")
    image.save(output_path, "PDF")

    await progress.edit_text("📤 Отправляю PDF...")

    await message.answer_document(
        FSInputFile(output_path),
        caption="✅ PDF готов!",
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await progress.edit_text("✅ Готово!")


@router.message(PdfConverter.waiting_file, F.document)
async def document_to_pdf(message: Message, state: FSMContext):

    progress = await message.answer("⏳ Конвертирую...")

    document = message.document

    ext = document.file_name.split(".")[-1].lower()

    uid = str(uuid.uuid4())

    input_path = f"temp/{uid}.{ext}"

    file = await message.bot.get_file(document.file_id)

    await message.bot.download_file(
        file.file_path,
        input_path
    )

    # Изображения
    if ext in ["jpg", "jpeg", "png", "webp"]:

        output_path = f"temp/{uid}.pdf"

        image = Image.open(input_path).convert("RGB")

        image.save(output_path, "PDF")

    # Microsoft Office
    elif ext in ["doc", "docx", "xls", "xlsx", "ppt", "pptx"]:

        output_path = office_to_pdf(input_path)

    else:

        os.remove(input_path)

        await progress.edit_text(
            "❌ Этот формат пока не поддерживается."
        )

        return

    await progress.edit_text("📤 Отправляю PDF...")

    await message.answer_document(
        FSInputFile(output_path),
        caption="✅ PDF готов!",
        reply_markup=main_keyboard
    )

    if os.path.exists(input_path):
        os.remove(input_path)

    if os.path.exists(output_path):
        os.remove(output_path)

    await state.clear()

    await progress.edit_text("✅ Готово!")