from decouple import config
import secrets

TOKEN = config('TOKEN')

ERROR_CHAT_ID = config('ERROR_CHAT_ID')

CACHE_DIR = 'cache'

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_PASSWORD = config('REDIS_PASSWORD')

REDIS_BOT_DB = config('REDIS_BOT_DB')
REDIS_LIST_DB = config('REDIS_LIST_DB')

IP_REGULAR = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
IP_WITH_MASK_REGULAR = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}\b'
IP_WITH_OPTIONAL_MASK_REGULAR = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:/[0-9]{1,2})?\b'

ADMIN_SECRET = secrets.token_urlsafe(32)
