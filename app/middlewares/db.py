from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Callable, Dict, Any, Awaitable

from app.database.database import Database


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        async with self.session() as session:
            data["db"] = Database(session=session)
            try:
                return await handler(event, data)
            finally:
                await session.close()
