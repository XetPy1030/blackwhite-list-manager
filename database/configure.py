def configure_app():
    import django
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'database.settings')
    os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')

    django.setup()

    from django.core.management import call_command

    call_command('makemigrations', 'database')
    call_command('migrate')
