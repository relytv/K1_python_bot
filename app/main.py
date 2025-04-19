import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.middlewares.admin import AdminCheckMiddleware
from app.middlewares.db import DatabaseMiddleware
from app.handlers import start_menu, superadmin_commands




async def main():
    logging.basicConfig(level=logging.INFO)
    
    engine = create_async_engine(url= "postgresql+asyncpg://k1_admin:postgres@localhost:9877/postgres", echo=True)
    session = async_sessionmaker(engine, expire_on_commit=False)
    
    bot = Bot("6963651623:AAEVd6CKaeP1vJKXT24WoY5DECa_tET6S7g")
    dp = Dispatcher()
    dp.include_routers(start_menu.router, superadmin_commands.router)
    

    dp.update.middleware(DatabaseMiddleware(session))

    admin_router = superadmin_commands.router
    
    admin_router.message.middleware(AdminCheckMiddleware(session))
    admin_router.callback_query.middleware(AdminCheckMiddleware(session))
    
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
