from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.default_menu import get_start_menu_kb

router = Router()


@router.message(CommandStart())
async def start_keyboard(message: Message):
    markup = get_start_menu_kb()
    await message.answer(
        "Привет тьютор. Что хочешь сделать?", reply_markup=markup.as_markup()
    )
