import datetime
import asyncio
from asyncio import Task, Future
from typing import Coroutine

groups_coros: list[list[int | Coroutine | Future | None]] = []

last_message_dates: dict[int, float] = {}


def append_coro(group_id: int, coro: Coroutine):
    """
    Добавление корутины в список готовых к отправке
    """
    print('append_coro', group_id, coro)
    groups_coros.append([group_id, coro, None])


async def group_awaiter():
    """
    Функция ожидания сообщений в группах
    Не может отправлять сообщения в определенную группу чаще, чем раз в 5 секунд
    """
    while True:
        # Очистить список готовых корутин
        i = 0
        while i < len(groups_coros):
            if groups_coros[i][2] is not None:
                if groups_coros[i][2].done():
                    groups_coros.pop(i)
                    continue

            i += 1

        for i in range(len(groups_coros)):
            group_id, coro, task = groups_coros[i]
            if task is not None:
                continue

            if group_id not in last_message_dates:
                last_message_dates[group_id] = 0

            if (datetime.datetime.now() - datetime.datetime.fromtimestamp(last_message_dates[group_id])).seconds > 4:
                try:
                    groups_coros[i][2] = asyncio.ensure_future(coro)
                except Exception as ex:
                    print(ex)
                last_message_dates[group_id] = datetime.datetime.now().timestamp()

        await asyncio.sleep(1)
