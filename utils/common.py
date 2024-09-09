import string
import time
import traceback
from functools import wraps

import requests

from config.logger_config import new_logger
from config.settings import ERROR_CHAT_ID, TOKEN
from utils.group_awaiter import append_coro

printable = set(string.printable)


def scheduler(wait_for_seconds: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                func(*args, **kwargs)
                time.sleep(wait_for_seconds)

        return wrapper

    return decorator


async def send_error(e):
    from config import bot
    detail = filter(lambda x: x in printable, traceback.format_exc())
    detail = ''.join(detail)
    append_coro(ERROR_CHAT_ID, bot.send_message(
        ERROR_CHAT_ID,
        f'Бот: Родительский\n'
        f'Ошибка: {e}\n'
        f'Ошибка в функции {e.__traceback__.tb_frame.f_code.co_name}:\n'
        f'{detail}',
    ))


def send_error_sync(e):
    requests.get(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        params={
            'chat_id': ERROR_CHAT_ID,
            'text': f'Бот: Родительский\n'
                    f'Ошибка: {e}\n'
                    f'Ошибка в функции {e.__traceback__.tb_frame.f_code.co_name}:\n{e} \n{e.__traceback__}'
        }
    )


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger_e = new_logger('error_handler')
            logger_e.exception(e)
            send_error_sync(e)

    return wrapper
