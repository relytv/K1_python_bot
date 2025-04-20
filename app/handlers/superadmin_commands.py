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

@router.message(Command("add_group"))
async def add_group(message: Message, command: CommandObject, db: Database):
    
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    try:
        args = command.args.strip().split()
        group_name = args[0]
        location_name = args[1]
        admin_name = args[2]
        
        group = await db.add_group(group_name=group_name,admin_name=admin_name, location_name=location_name)

        await message.answer(
            "✅ Группа успешно добавлена:\n" 
            f"group_name: {group.name}\n"
            f"location: {group.location}\n"
            f"tutor: {group.admin}" 
        )

    except ValueError:
        await message.answer(
            "Ошибка: неправльный формат команды. Пример:\n"
            "/add_group Среда_10:00 Гольцова Gleb"
        )

@router.message(Command("add_user"))
async def add_user(message: Message, command: CommandObject, db: Database):
    
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    try:
        args = command.args.split(maxsplit=3)

        if len(args) < 3:
            raise ValueError("Недостаточно аргументов")
        fullname = f"{args[0]} {args[1]}"
        group_name = args[2]
        location_name = args[3]
        
        user = await db.add_user(username=fullname, group_name=group_name,location_name=location_name)

        await message.answer(
            "✅ Пользователь успешно добавлен:\n" 
            f"username: {fullname}\n"
            f"group_name: {group_name}\n"
            f"location: {location_name}\n"
            f"points: {user.points}" 
        )

    except ValueError:
        await message.answer(
            "Ошибка: неправльный формат команды. Пример:\n"
            "/add_user Иван Иванов Среда_10:30 Гольцова "
        )
    # except Exception as e:
    #     await message.answer("⚠️ Произошла ошибка при добавлении пользователя")

@router.message(Command("show_groups_with_locations"))
async def show_groups_with_locations(
    message: Message, 
    command: CommandObject, 
    db: Database
    ):
    groups_locations = await db.get_all_group_and_locations()

    response = ["📋 Список групп и локаций:\n"]
    response.extend(
        f"{group_name} -> {location_name}"
        for group_name, location_name in groups_locations
    )

    await message.answer('\n'.join(response))
    

# db.add_admin
