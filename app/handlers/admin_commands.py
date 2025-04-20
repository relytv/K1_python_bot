from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

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


@router.message(Command("show_my_groups"))
async def show_my_groups(message: Message, db:Database):
    groups = await db.get_admins_groups(message.from_user.id)

    response = ["📂Ваши группы и локации: ", ""]
    for group in groups:
        print(f"ПРОВЕРКА {group}")
        response.append(f"Группа: {group[0]} | Локация: {group[1]}")

    await message.answer("\n".join(response))


@router.callback_query(F.data == "show_my_groups")
async def btn_show_groups(callback: CallbackQuery, db: Database):
        groups = await db.get_admins_groups(callback.from_user.id)

        response = ["📂Ваши группы и локации: ", ""]
        for group in groups:
            print(f"ПРОВЕРКА {group}")
            response.append(f"🏢 Группа: {group[0]} | 📍 Локация: {group[1]}")

        await callback.message.answer("\n".join(response))
        await callback.answer()
