from typing import Callable, Dict, Any, Awaitable

import aiogram
from aiogram import BaseMiddleware
from aiogram import types
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import TelegramObject
from django.utils import timezone

from config.logger_config import new_logger
from database import User
from utils.common import send_error
from utils.exceptions import MyException


class ErrorHandlerMiddleware(BaseMiddleware):
    logger_e = new_logger('error_handler')

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        try:
            result = await handler(event, data)
            return result
        except MyException as e:
            self.logger_e.exception(e)
            raise e
        except Exception as e:
            self.logger_e.exception(e)
            await send_error(e)
            raise e


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, types.Message) or isinstance(event, types.CallbackQuery):
            t_user = event.from_user
            user = User.objects.get_or_create(user_id=t_user.id)[0]
        else:
            user = None
            t_user = None

        if user:
            user.t_username = t_user.username
            user.t_first_name = t_user.first_name
            user.t_last_name = t_user.last_name
            user.last_message_date = timezone.now()
            user.save()

        result = await handler(event, data)
        return result


class AdminMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, types.Message):
            user = User.objects.get_or_create(user_id=event.from_user.id)[0]
            if user.is_admin:
                result = await handler(event, data)
                return result
            else:
                await event.answer('Вы не админ')
                return

        result = await handler(event, data)
        return result


class AdminCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, types.CallbackQuery):
            user = User.objects.get_or_create(user_id=event.from_user.id)[0]
            if user.is_admin:
                result = await handler(event, data)
                return result
            else:
                await event.answer('Вы не админ')
                return

        result = await handler(event, data)
        return result


class FuncMessageMiddleware(BaseMiddleware):
    def __init__(self, func):
        self.func = func

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, types.Message):
            user = User.objects.get_or_create(user_id=event.from_user.id)[0]
            chat_id = event.chat.id
            if self.func(user, chat_id, event):
                result = await handler(event, data)
                return result
            else:
                await event.answer('Вы не прошли проверку')
                return

        result = await handler(event, data)
        return result


class FuncCallbackQueryMiddleware(BaseMiddleware):
    def __init__(self, func):
        self.func = func

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, types.CallbackQuery):
            user = User.objects.get_or_create(user_id=event.from_user.id)[0]
            chat_id = event.message.chat.id
            if self.func(user, chat_id, event):
                result = await handler(event, data)
                return result
            else:
                await event.answer('Вы не прошли проверку')
                return

        result = await handler(event, data)
        return result


class WaitableErrorHandlerMiddleware(BaseMiddleware):
    logger_e = new_logger('error_handler')

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        try:
            result = await handler(event, data)
            return result
        except aiogram.exceptions.TelegramRetryAfter as e:
            await event.answer(f'Подождите {e.retry_after} секунд')
            raise e
