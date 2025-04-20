from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.database.database import Database

router = Router()


@router.message(Command("add_admin"))
async def add_admin(message: Message, command: CommandObject, db: Database):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    try:
        args = command.args.strip().split()
        tg_id = int(args[0])
        username = args[1]
        is_superadmin = args[2].lower() == "true"

        admin = await db.add_admin(tg_id, username, is_superadmin)

        await message.answer(
            "✅ Администратор успешно добавлен:\n"
            f"ID: {admin.tg_id}\n"
            f"Username: @{admin.username}\n"
            f"Супер-админ: {'Да' if admin.is_superadmin else 'Нет'}"
        )

    except ValueError:
        await message.answer(
            "Ошибка: неправльный формат команды. Пример:\n"
            "/add_admin 123456 username true"
        )


@router.message(Command("add_location"))
async def add_location(message: Message, command: CommandObject, db: Database):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    try:
        location_name = command.args.strip()
        location = await db.add_location(location_name)

        await message.answer(
            "✅ Локация успешно добавлена:\n" f"Name: @{location.name}\n" 
        )

    except ValueError:
        await message.answer(
            "Ошибка: неправльный формат команды. Пример:\n"
            "/add_location Гольцова"
        )


# db.add_admin
