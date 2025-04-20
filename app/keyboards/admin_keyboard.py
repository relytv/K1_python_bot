from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_start_admin_menu_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text="Показать группы", callback_data="some_data")
    btn2 = types.InlineKeyboardButton(text="Проставить оценки", callback_data="some_data")
    builder.add(btn1)
    builder.add(btn2)
    return builder