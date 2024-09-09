from functools import wraps

from aiogram import types

from database import User


def is_admin(func):
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        if isinstance(event, types.Message):
            message = event
            user_id = event.from_user.id
        elif isinstance(event, types.CallbackQuery):
            message = event.message
            user_id = event.from_user.id
        else:
            return await func(event, *args, **kwargs)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            if isinstance(event, types.CallbackQuery):
                await event.answer('Вы не зарегистрированы')
            return await message.answer('Вы не зарегистрированы')
        if not user.is_admin:
            if isinstance(event, types.CallbackQuery):
                await event.answer('Вы не администратор')
            return await message.answer('Вы не администратор')

        return await func(event, *args, **kwargs)

    return wrapper
