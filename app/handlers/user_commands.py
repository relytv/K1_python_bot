from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.database.database import Database

router = Router()

@router.message(Command("cyberons"))
async def show_points(message: Message, command: CommandObject, db: Database):
    cyberons = await db.get_cyberons(message.from_user.id)

    await message.answer(
        f"Ваш баланс кибернов: {cyberons}"
    )
