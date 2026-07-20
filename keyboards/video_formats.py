from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_video_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🎵 MP3",
        callback_data="video_mp3"
    )

    builder.button(
        text="🎬 GIF",
        callback_data="video_gif"
    )

    builder.adjust(2)

    return builder.as_markup()