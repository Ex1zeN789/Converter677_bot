import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.start import router
from handlers.menu import router as menu_router
from handlers.image_converter import router as image_router
from handlers.video_converter import router as video_router
from handlers.background import router as background_router
from handlers.pdf_converter import router as pdf_router
from handlers.audio_converter import router as audio_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(menu_router)
    dp.include_router(image_router)
    dp.include_router(video_router)
    dp.include_router(background_router)
    dp.include_router(pdf_router)
    dp.include_router(audio_router)

    print("✅ Бот запускается...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())