from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models

from goods_accounting.models import RoommatesGroup


class User(AbstractUser):
    email = models.EmailField('электронная почта', unique=True)
    roommates_group = models.ForeignKey(RoommatesGroup, on_delete=models.SET_NULL, null=True,
                                        verbose_name='группа человек')

    class Meta:
        ordering = ('id',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._meta.get_field('username').help_text = ''
        self._meta.get_field('is_superuser').help_text = 'Супер пользователь имеет все права без их явного назначения'
        self._meta.get_field('is_staff').help_text = 'Сотрудник может иметь права на изменение определенных ресурсов'
