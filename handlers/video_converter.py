import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from states.video_converter import VideoConverter
from keyboards.video_formats import get_video_keyboard
from keyboards.main_menu import main_keyboard
from services.video_service import video_to_mp3, video_to_gif

router = Router()

os.makedirs("temp", exist_ok=True)


@router.message(F.text == "🎥 Видео")
async def video_menu(message: Message, state: FSMContext):

    await state.set_state(VideoConverter.waiting_video)

    await message.answer(
        "🎥 <b>Конвертация видео</b>\n\n"
        "Доступные действия:\n\n"
        "🎵 Видео → MP3\n"
        "🎬 Видео → GIF\n\n"
        "📤 Отправьте видео.",
        parse_mode="HTML"
    )


@router.message(VideoConverter.waiting_video, F.video)
async def receive_video(message: Message, state: FSMContext):

    video = message.video

    file = await message.bot.get_file(video.file_id)

    uid = str(uuid.uuid4())

    input_path = f"temp/{uid}.mp4"

    await message.bot.download_file(
        file.file_path,
        destination=input_path
    )

    await state.update_data(video=input_path)

    await state.set_state(VideoConverter.waiting_action)

    await message.answer(
        "🎥 <b>Видео успешно загружено!</b>\n\n"
        "👇 <b>Выберите действие:</b>",
        reply_markup=get_video_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(VideoConverter.waiting_action, F.data == "video_mp3")
async def convert_mp3(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()

    input_path = data["video"]

    uid = str(uuid.uuid4())

    output_path = f"temp/{uid}.mp3"

    await callback.message.edit_text(
        "📥 <b>Видео получено!</b>\n\n"
        "████░░░░░░ 40%\n\n"
        "⚙️ Конвертирую в MP3...",
        parse_mode="HTML"
    )

    video_to_mp3(input_path, output_path)

    await callback.message.edit_text(
        "██████████ 100%\n\n"
        "📤 Загружаю результат...",
        parse_mode="HTML"
    )

    await callback.message.answer_document(
        document=FSInputFile(output_path),
        caption=(
            "🎉 <b>Готово!</b>\n\n"
            "🎵 <b>Видео успешно конвертировано в MP3.</b>\n\n"
            "❤️ Спасибо за использование Converter677 Bot!"
        ),
        parse_mode="HTML",
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await callback.message.edit_text(
        "✅ <b>Конвертация завершена!</b>",
        parse_mode="HTML"
    )


@router.callback_query(VideoConverter.waiting_action, F.data == "video_gif")
async def convert_gif(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()

    input_path = data["video"]

    uid = str(uuid.uuid4())

    output_path = f"temp/{uid}.gif"

    await callback.message.edit_text(
        "📥 <b>Видео получено!</b>\n\n"
        "████░░░░░░ 40%\n\n"
        "⚙️ Создаю GIF...",
        parse_mode="HTML"
    )

    video_to_gif(input_path, output_path)

    await callback.message.edit_text(
        "██████████ 100%\n\n"
        "📤 Загружаю результат...",
        parse_mode="HTML"
    )

    await callback.message.answer_document(
        document=FSInputFile(output_path),
        caption=(
            "🎉 <b>Готово!</b>\n\n"
            "🎬 <b>GIF успешно создан.</b>\n\n"
            "❤️ Спасибо за использование Converter677 Bot!"
        ),
        parse_mode="HTML",
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await callback.message.edit_text(
        "✅ <b>Конвертация завершена!</b>",
        parse_mode="HTML"
    )