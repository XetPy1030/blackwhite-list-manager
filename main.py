import asyncio
import os.path

from config import bot, dp
from config.logger_config import logger
from config.settings import CACHE_DIR, ADMIN_SECRET
from utils.group_awaiter import group_awaiter


async def init_bot_commands():
    await bot.set_my_commands(
        [
            {'command': 'start', 'description': 'Начать работу с ботом'},
            {'command': 'whitelist', 'description': 'Управление белым списком'},
            {'command': 'blacklist', 'description': 'Управление черным списком'},
            {'command': 'blacklist_with_netmask', 'description': 'Управление черным списком с подсетью'},
        ]
    )


async def main():
    import database  # noqa

    from handlers import router
    dp.include_router(router)

    logger.info('Initializing bot commands...')
    await init_bot_commands()

    logger.info('Starting bot polling...')
    asyncio.ensure_future(group_awaiter())
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info('Starting bot...')

    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    logger.info(f'Admin secret is {ADMIN_SECRET}')
    with open('admin_secret.txt', 'w') as f:
        f.write(ADMIN_SECRET)

    asyncio.run(main())
