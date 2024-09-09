import math

from config.redis import redis

LIMIT_PAGE = 5

MAX_LIMIT = 1000

WHITELIST = 'whitelist'
BLACKLIST = 'blacklist'


def add_ip_to_list(ip: str, db_list: str) -> bool:
    if redis.get(f'{db_list}:{ip}'):
        return False

    redis.set(f'{db_list}:{ip}', 1)
    return True


def remove_from_list(ip: str, db_list: str):
    redis.delete(f'{db_list}:{ip}')


def get_list_ips(db_list: str, page: int = 0, limit: int = LIMIT_PAGE) -> list[str]:
    start = page * limit
    end = start + limit
    _, keys = redis.scan(0, f'{db_list}:*', count=MAX_LIMIT)
    try:
        filtered_keys = keys[start:end]
    except IndexError:
        filtered_keys = []
    return [key.removeprefix(f'{db_list}:') for key in filtered_keys]


def get_list_total_pages(db_list: str):
    _, keys = redis.scan(0, f'{db_list}:*', count=MAX_LIMIT)
    total = len(keys)
    return math.ceil(total / LIMIT_PAGE)
