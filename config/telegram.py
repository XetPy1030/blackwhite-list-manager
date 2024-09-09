from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import settings
from core.middleware import UserMiddleware, ErrorHandlerMiddleware, WaitableErrorHandlerMiddleware

storage = RedisStorage(
    redis=Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_BOT_DB,
        password=settings.REDIS_PASSWORD,
    )
)
bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)

dp.callback_query.outer_middleware(UserMiddleware())
dp.message.outer_middleware(UserMiddleware())

dp.message.middleware(ErrorHandlerMiddleware())
dp.callback_query.middleware(ErrorHandlerMiddleware())

dp.message.middleware(WaitableErrorHandlerMiddleware())
dp.callback_query.middleware(WaitableErrorHandlerMiddleware())
