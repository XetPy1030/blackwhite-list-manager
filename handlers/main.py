from aiogram import Router, types
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

import markups
from config.settings import ADMIN_SECRET
from database import User

router = Router()


@router.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer("Добро пожаловать!")


@router.callback_query(markups.common.BlankCD.filter())
async def blank_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer('Здесь ничего нет')


@router.message(Command('superadmin'))
async def superadmin(message: types.Message, command: CommandObject):
    if command.args != ADMIN_SECRET:
        return

    user = User.objects.get(user_id=message.from_user.id)
    user.is_admin = True
    user.save()

    await message.answer('Вы стали супер-админом!')
