import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers.start_menu import router as start_menu_router



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot("6963651623:AAEVd6CKaeP1vJKXT24WoY5DECa_tET6S7g")
    dp = Dispatcher()
    dp.include_router(start_menu_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
