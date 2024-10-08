from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State

from markups.common import BlankCD


class RemoveIpListCD(CallbackData, prefix='remove_ip_bl'):
    ip: str


class AddIpListCD(CallbackData, prefix='add_ip_bl'):
    pass


class RemoveIpCD(CallbackData, prefix='remove_ip_bl_kb'):
    pass


class PageListCD(CallbackData, prefix='page_bl'):
    page: int


def get_list_keyboard(ips: list[str], current_page: int = 0, total_pages: int = 1):
    kb = []
    for ip in ips:
        kb.append(
            [
                types.InlineKeyboardButton(
                    text=ip,
                    callback_data=RemoveIpListCD(ip=ip).pack()
                )
            ]
        )

    kb.append(
        [
            types.InlineKeyboardButton(
                text='Добавить IP в черный список',
                callback_data=AddIpListCD().pack()
            )
        ]
    )
    kb.append(
        [
            types.InlineKeyboardButton(
                text='Удалить IP из черного списка',
                callback_data=RemoveIpCD().pack()
            )
        ]
    )

    sub_lb = []
    if current_page > 0:
        sub_lb.append(
            types.InlineKeyboardButton(
                text='<<',
                callback_data=PageListCD(page=current_page - 1).pack()
            )
        )
    else:
        sub_lb.append(
            types.InlineKeyboardButton(
                text='#',
                callback_data=BlankCD().pack()
            )
        )

    sub_lb.append(
        types.InlineKeyboardButton(
            text=f'{current_page + 1}/{total_pages}',
            callback_data=BlankCD().pack()
        )
    )

    if current_page < total_pages - 1:
        sub_lb.append(
            types.InlineKeyboardButton(
                text='>>',
                callback_data=PageListCD(page=current_page + 1).pack()
            )
        )
    else:
        sub_lb.append(
            types.InlineKeyboardButton(
                text='#',
                callback_data=BlankCD().pack()
            )
        )

    kb.append(sub_lb)

    return types.InlineKeyboardMarkup(inline_keyboard=kb)


class AddListBlackIPState(StatesGroup):
    ip = State()


AddListIPState = AddListBlackIPState


class RemoveListIPState(StatesGroup):
    ip = State()
