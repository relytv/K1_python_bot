from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Callable, Dict, Any, Awaitable

from app.database.database import Database


class AdminCheckMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user = data.get("event_from_user")
        if not user:
            await event.answer("Доступ запрещен")
            return

        async with self.session() as session:
            db = Database(session=session)

            if not await db.is_admin(user.id):
                if isinstance(event, Message):
                    await event.answer("🚫Только для администратора")
                    return

            return await handler(event, data)
