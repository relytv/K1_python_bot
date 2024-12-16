from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_start_menu_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    btn1 = types.InlineKeyboardButton(text="Привет, это я КНОПКА!", callback_data="some_data")
    builder.add(btn1)
    return builder