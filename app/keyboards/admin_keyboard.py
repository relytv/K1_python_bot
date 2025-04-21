import uuid
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class GroupsIdCallbackFactory(CallbackData, prefix="id",  sep="|"):

    id: uuid.UUID
    group: str



def get_start_admin_menu_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text="Показать группы", callback_data="show_my_groups")
    btn2 = InlineKeyboardButton(text="Проставить оценки", callback_data="give_rating")
    builder.add(btn1)
    builder.add(btn2)
    return builder


def get_give_rating_kb(buttons_data: list[tuple[str, str, uuid.UUID]]) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()
    for group, location, id in buttons_data:
        builder.button(
            text=f"{group}: {location}", 
            callback_data=GroupsIdCallbackFactory(
               id=id,
               group = group
            )
            )
    builder.adjust(1)
    return builder

def get_grades_kb() -> ReplyKeyboardBuilder:

    builder = ReplyKeyboardBuilder()
    grade = 10
    buttons: list[KeyboardButton] = [KeyboardButton(text=f"{i}") for i in range(10, 31, 5)]
    builder.row(*buttons, width=3)
    return builder
    