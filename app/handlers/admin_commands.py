from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove


from app.database.database import Database
from app.handlers.dialogstate import WaitGrades
from app.keyboards.admin_keyboard import GroupsIdCallbackFactory,  get_give_rating_kb, get_grades_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

router = Router()

# Все группы с локациями
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

# Все группы тьютора
@router.message(Command("show_my_groups"))
async def show_my_groups(message: Message, db:Database):
    groups = await db.get_admins_groups(message.from_user.id)

    response = ["📂Ваши группы и локации: ", ""]
    for group in groups:
        print(f"ПРОВЕРКА {group}")
        response.append(f"Группа: {group[0]} | Локация: {group[1]}")

    await message.answer("\n".join(response))

#Начиcление киберонов 
@router.callback_query(F.data == "give_rating")
async def btn_give_rating(callback: CallbackQuery, db: Database):
    groups = await db.get_admins_groups(callback.from_user.id)
    
    await callback.message.answer(
         "Выберите локацию: ",
         reply_markup=get_give_rating_kb(groups).as_markup()
    )
    await callback.answer()

@router.callback_query(GroupsIdCallbackFactory.filter())
async def process_give_rating(callback: CallbackQuery,
                              callback_data: GroupsIdCallbackFactory,
                              state: FSMContext,
                              db: Database):
    users = await db.get_users_by_group_id(callback_data.id)
    response = [f"📃Список учеников: \n {callback_data.group}", ""]
    for user in users:
        response.append(f"{user.username}: {user.points}")        
    await callback.message.answer("\n".join(response))
    await callback.answer()

    await state.update_data(users=users, current_index=0)
    await state.set_state(WaitGrades.waiting_for_grading)
    
    await ask_for_grade(callback.message, users[0])

 
async def ask_for_grade(message: Message, user):
    await message.answer(
        f"Ученик: {user[0]}\n"
        "Введите количество киберонов:\n"
        "Для отмены введите /cancel\n",
        reply_markup=get_grades_kb().as_markup(resize_keyboard=True)
    )

@router.message(WaitGrades.waiting_for_grading)
async def process_grade(message: Message, state: FSMContext, db: Database):
    if message.text.lower() in ["/cancel", "отмена", "cancel"]:
        await state.clear()
        await message.answer("Оценивание отменено", reply_markup=ReplyKeyboardRemove())
        return
    
    data = await state.get_data()
    users = data["users"]
    current_index = data["current_index"]   
    current_user = users[current_index]
    try:
        points = int(message.text)
        await db.update_user_points(current_user.id, points)
        next_index = current_index + 1
        if next_index < len(users):
            await state.update_data(current_index=next_index)
            await ask_for_grade(message, users[next_index])
        else:
            await message.answer("Все ученики оценены!", reply_markup=ReplyKeyboardRemove())
            await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число:")


#Колбэк показа групп
@router.callback_query(F.data == "show_my_groups")
async def btn_show_groups(callback: CallbackQuery, db: Database):
        groups = await db.get_admins_groups(callback.from_user.id)

        response = ["📂Ваши группы и локации: ", ""]
        for group in groups:
            response.append(f"🏢 Группа: {group[0]} | 📍 Локация: {group[1]}")

        await callback.message.answer("\n".join(response))
        await callback.answer()
