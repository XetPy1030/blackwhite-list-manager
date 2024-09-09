import re

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config.settings import IP_REGULAR
from core.middleware import AdminMessageMiddleware, AdminCallbackQueryMiddleware
from markups.admin import black as list_markups
from utils import rds_manager

router = Router()

DB_LIST = rds_manager.BLACKLIST
RUS_LIST_CAPITALIZE = 'Черный'
RUS_LIST = 'черный'
RUS_LIST_PARENT = 'черного'
RUS_LIST_OMIT = 'черном'


router.message.middleware(AdminMessageMiddleware())
router.callback_query.middleware(AdminCallbackQueryMiddleware())


@router.message(Command(DB_LIST))
async def list_handler(message: types.Message, state: FSMContext):
    ips = rds_manager.get_list_ips(db_list=DB_LIST)
    total = rds_manager.get_list_total_pages(db_list=DB_LIST)
    kb = list_markups.get_list_keyboard(ips, total_pages=total)
    await message.answer(
        (
            f'{RUS_LIST_CAPITALIZE} список IP:\n'
            'Выберите IP для удаления или добавьте новый'
        ),
        reply_markup=kb
    )


@router.callback_query(list_markups.RemoveIpListCD.filter())
async def remove_ip_list_handler(callback_query: types.CallbackQuery, state: FSMContext):
    ip = list_markups.RemoveIpListCD.unpack(callback_query.data).ip
    rds_manager.remove_from_list(ip, db_list=DB_LIST)
    await callback_query.answer()
    await callback_query.message.answer(f'IP {ip} удален из {RUS_LIST_PARENT} списка')

    ips = rds_manager.get_list_ips(db_list=DB_LIST)
    total = rds_manager.get_list_total_pages(db_list=DB_LIST)
    kb = list_markups.get_list_keyboard(ips, total_pages=total)
    await callback_query.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(list_markups.PageListCD.filter())
async def page_list_handler(callback_query: types.CallbackQuery, state: FSMContext):
    page = list_markups.PageListCD.unpack(callback_query.data).page
    ips = rds_manager.get_list_ips(db_list=DB_LIST, page=page)
    total = rds_manager.get_list_total_pages(db_list=DB_LIST)
    kb = list_markups.get_list_keyboard(ips, page, total)
    await callback_query.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(list_markups.AddIpListCD.filter())
async def add_ip_list_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(f'Введите IP для добавления в {RUS_LIST} список')
    await state.set_state(list_markups.AddListIPState.ip)


@router.message(StateFilter(list_markups.AddListIPState.ip))
async def add_ip_list_handler(message: types.Message, state: FSMContext):
    ip = message.text
    if not re.match(IP_REGULAR, ip):
        await message.answer('Некорректный IP')
        return

    is_add = rds_manager.add_ip_to_list(ip, db_list=DB_LIST)
    if is_add:
        await message.answer(f'IP {ip} добавлен в {RUS_LIST} список')
    else:
        await message.answer(f'IP {ip} уже есть в {RUS_LIST_OMIT} списке')
    await state.clear()
