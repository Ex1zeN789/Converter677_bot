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
        "🪄 <b>Удаление фона</b>\n\n"
        "📤 Отправьте фотографию.\n\n"
        "Через несколько секунд вы получите изображение "
        "с прозрачным фоном.",
        parse_mode="HTML"
    )


@router.message(BackgroundRemover.waiting_image, F.photo)
async def remove_bg_photo(message: Message, state: FSMContext):

    progress = await message.answer(
        "🖼 <b>Изображение получено!</b>\n\n"
        "████░░░░░░ 40%\n\n"
        "⚙️ Удаляю фон...",
        parse_mode="HTML"
    )

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

    await progress.edit_text(
        "██████████ 100%\n\n"
        "📤 Загружаю результат...",
        parse_mode="HTML"
    )

    await message.answer_document(
        document=FSInputFile(output_path),
        caption=(
            "🎉 <b>Готово!</b>\n\n"
            "🪄 <b>Фон успешно удалён.</b>\n\n"
            "❤️ Спасибо за использование <b>Converter677 Bot</b>!"
        ),
        parse_mode="HTML",
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await progress.edit_text(
        "✅ <b>Удаление фона завершено!</b>",
        parse_mode="HTML"
    )