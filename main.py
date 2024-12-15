import asyncio
import logging

from aiogram import Bot, Dispatcher


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot("")
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
