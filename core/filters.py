from typing import Type, Optional, Any, Dict, Union

from aiogram import Bot
from aiogram.filters import Filter, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, TelegramObject


class QueryFilter(Filter):
    def __init__(self, query: Type[CallbackData]):
        self.query = query

    async def __call__(self, callback_data, **kwargs):
        return self.query().pack() in callback_data.data


class StateTextFilter(Filter):
    def __init__(self, my_text: str, type_state) -> None:
        self.my_text = my_text
        self.type_state = type_state

    async def __call__(self, obj: TelegramObject, raw_state: Optional[str] = None) -> bool:
        if not isinstance(obj, Message):
            return False
        message = obj
        state = raw_state
        one = message.text == self.my_text
        a = StateFilter(self.type_state)
        two = await a(message, state)

        return one and two


class ViaFilter(Filter):
    def __init__(self):
        pass

    async def __call__(
            self, message: Message, bot: Bot
    ) -> Union[bool, Dict[str, Any]]:
        if message.via_bot:
            if message.via_bot.id == bot.id:
                return True

        return False
