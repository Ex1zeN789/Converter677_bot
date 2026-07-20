from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_formats_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="🟢 PNG", callback_data="format_png")
    builder.button(text="🔵 JPG", callback_data="format_jpg")
    builder.button(text="🟣 WEBP", callback_data="format_webp")
    builder.button(text="📄 PDF", callback_data="format_pdf")

    builder.adjust(2)

    return builder.as_markup()