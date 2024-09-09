import html

from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.BigIntegerField()
    is_admin = models.BooleanField(default=False)

    t_username = models.CharField(max_length=255, null=True, blank=True, default=None)
    t_first_name = models.CharField(max_length=255, null=True, blank=True, default=None)
    t_last_name = models.CharField(max_length=255, null=True, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    last_activity = models.DateTimeField(default=None, null=True, blank=True)

    @property
    def t_fullname(self):
        last_name = html.escape(self.t_last_name or "")
        first_name = html.escape(self.t_first_name or "")
        return f'{last_name} {first_name}'.strip() or 'Неизвестно'

    @property
    def link(self):
        return (f'<a href="tg://user?id={self.user_id}">'
                f'{self.t_fullname}'
                f'</a>{f" (@{self.t_username})" if self.t_username else ""}')
