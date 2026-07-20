import os
import uuid

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.audio_formats import audio_keyboard
from keyboards.main_menu import main_keyboard
from services.audio_service import convert_audio
from states.audio_converter import AudioConverter

router = Router()

os.makedirs("temp", exist_ok=True)


@router.message(F.text == "🎵 Конвертировать аудио")
async def audio_menu(message: Message, state: FSMContext):

    await state.set_state(AudioConverter.waiting_format)

    await message.answer(
        "🎵 Выберите формат:",
        reply_markup=audio_keyboard
    )


@router.message(AudioConverter.waiting_format)
async def choose_format(message: Message, state: FSMContext):

    formats = {
        "🟢 MP3": "mp3",
        "🔵 WAV": "wav",
        "🟣 FLAC": "flac",
        "🟠 OGG": "ogg",
        "🟡 M4A": "m4a"
    }

    if message.text not in formats:

        await message.answer("❌ Выберите формат кнопкой.")

        return

    await state.update_data(
        format=formats[message.text]
    )

    await state.set_state(
        AudioConverter.waiting_audio
    )

    await message.answer(
        "🎧 Теперь отправьте аудиофайл."
    )


@router.message(AudioConverter.waiting_audio, F.audio)
async def convert_music(message: Message, state: FSMContext):

    await process_audio(
        message,
        state,
        message.audio.file_id,
        message.audio.file_name.split(".")[-1]
    )


@router.message(AudioConverter.waiting_audio, F.document)
async def convert_document(message: Message, state: FSMContext):

    ext = message.document.file_name.split(".")[-1].lower()

    if ext not in [
        "mp3",
        "wav",
        "ogg",
        "flac",
        "m4a",
        "aac"
    ]:

        await message.answer(
            "❌ Это не аудиофайл."
        )

        return

    await process_audio(
        message,
        state,
        message.document.file_id,
        ext
    )


async def process_audio(
    message: Message,
    state: FSMContext,
    file_id,
    ext
):

    data = await state.get_data()

    output_ext = data["format"]

    progress = await message.answer(
        "⏳ Конвертирую..."
    )

    uid = str(uuid.uuid4())

    input_path = f"temp/{uid}.{ext}"

    output_path = f"temp/{uid}.{output_ext}"

    file = await message.bot.get_file(file_id)

    await message.bot.download_file(
        file.file_path,
        destination=input_path
    )

    convert_audio(
        input_path,
        output_path
    )

    await progress.edit_text(
        "📤 Отправляю..."
    )

    await message.answer_document(
        FSInputFile(output_path),
        caption=f"✅ Готово!\n\nФормат: {output_ext.upper()}",
        reply_markup=main_keyboard
    )

    os.remove(input_path)
    os.remove(output_path)

    await state.clear()

    await progress.edit_text(
        "✅ Конвертация завершена!"
    )