# BlackWhite List Manager Bot

Бот для управления черным и белым списком ip адресов из redis.

## Quick start

```bash
docker-compose up -d
pip install -r requirements.txt
python main.py
```

## Env variables

| Variable       | Description                     | Default   |
|----------------|---------------------------------|-----------|
| TOKEN          | Токен бота                      | -         |
| ERROR_CHAT_ID  | ID чата для отправки ошибок     | -         |
| REDIS_HOST     | Хост redis                      | localhost |
| REDIS_PORT     | Порт redis                      | 6379      |
| REDIS_PASSWORD | Пароль redis                    | -         |
| REDIS_BOT_DB   | Номер базы redis для бота       | 1         |
| REDIS_LIST_DB  | Номер базы redis для ip адресов | 0         |

## Commands

Для становления админом бота необходимо отправить боту команду `/superadmin <password>`, где `<password>` - пароль,
указанный в логах бота при запуске или в файле `admin_secret.txt`.

| Command     | Description                       | Access level |
|-------------|-----------------------------------|--------------|
| /start      | Начало работы с ботом             | Все          |
| /whitelist  | Добавить ip адрес в белый список  | Админ        |
| /blacklist  | Добавить ip адрес в черный список | Админ        |
| /superadmin | Стать админом бота                | Все          |

# Redis List Manager Schema

| Key             | Value |
|-----------------|-------|
| black_list:{ip} | 1     |
| white_list:{ip} | 1     |

Для белого списка поддерживается маска подсети с помощью `/{число}`.
Например: `192.0.0.0/2`.
