from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.database.database import Database
from app.keyboards.default_menu import get_start_menu_kb
from app.keyboards.admin_keyboard import get_start_admin_menu_kb
from app.handlers.dialogstate import LinkAccount
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, db: Database, state: FSMContext):
    
    is_admin = await db.is_admin(tg_id=message.from_user.id)
    if is_admin:
        await message.answer(
            "👑 Добро пожаловать, администратор!\n"
            "Доступные команды!\n",
            reply_markup=get_start_admin_menu_kb().as_markup()
        )
    else:
     
        user = await db.get_user_by_tg_id(message.from_user.id)

        if user:
            await message.answer("Вы уже привязаны в аккаунту! Проверьте свой баланс! /cyberons")   
            return
        
        await state.set_state(LinkAccount.waiting_for_name)
        await message.answer(
        "🔐 Ваш Telegram ID не привязан к учетной записи.\n"
        "Пожалуйста, введите ваше имя и фамилию:"
    
        )


@router.message(LinkAccount.waiting_for_name)
async def process_name(message: Message, db: Database, state: FSMContext):
    # try:
        # Ищем пользователя в БД
        user = await db.get_user_by_name(message.text.strip())
        
        if not user:
            await message.answer("❌ Пользователь не найден. Попробуйте еще раз")
            return
        
        # Обновляем запись в БД
        await db.link_telegram_id(
            user_id=user.id,
            tg_id=message.from_user.id,
        )
        
        await state.clear()
        await message.answer(
            f"✅ Успешно привязано!\n"
            f"Telegram ID: {message.from_user.id}\n"
        )
    
    # except Exception as e:
        
    #     await message.answer("⚠️ Ошибка привязки. Попробуйте позже")