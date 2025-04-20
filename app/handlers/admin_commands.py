from aiogram import Router, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message

from app.database.database import Database
from app.keyboards.admin_keyboard import get_start_admin_menu_kb

router = Router()

# @router.message(CommandStart())
# async def start_handler(message: Message, db: Database):
#      await message.answer(
#             "👑 Добро пожаловать, администратор!\n"
#             "Доступные команды!\n",
#             reply_markup=get_start_admin_menu_kb().as_markup()
#         )


@router.message(Command("show_groups_with_locations"))
async def show_groups_with_locations(
    message: Message, 
    db: Database
    ):
    groups_locations = await db.get_all_group_and_locations()

    response = ["📋 Список групп и локаций:\n"]
    response.extend(
        f"{group_name} -> {location_name}"
        for group_name, location_name in groups_locations
    )

    await message.answer('\n'.join(response))

