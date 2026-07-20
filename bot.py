import asyncio
import os

from aiohttp import web

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from handlers.start import router
from handlers.menu import router as menu_router
from handlers.image_converter import router as image_router
from handlers.video_converter import router as video_router
from handlers.background import router as background_router
from handlers.audio_converter import router as audio_router


async def health(request):
    return web.Response(text="Converter677 Bot is running!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(f"🌐 Web server started on port {port}")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)
    dp.include_router(menu_router)
    dp.include_router(image_router)
    dp.include_router(video_router)
    dp.include_router(background_router)
    dp.include_router(audio_router)

    await start_web_server()

    print("✅ Converter677 Bot started!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())