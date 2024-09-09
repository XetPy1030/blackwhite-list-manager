from redis import Redis
from .settings import REDIS_HOST, REDIS_PORT, REDIS_LIST_DB, REDIS_PASSWORD

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_LIST_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)
