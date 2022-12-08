from typing import Any, Union

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query import RawQuerySet

from accounts.raw_sql_queries import all_group_purchases_query
from utils import StrMethodMixin


class RoommatesGroupManager(models.Manager):

    def get_all_purchases(self, group: Union[int, 'RoommatesGroup']) -> RawQuerySet:
        """Метод возвращает покупки всех членов комнаты"""

        if isinstance(group, RoommatesGroup):
            group = group.pk
        return self.raw(all_group_purchases_query, (group,))


class RoommatesGroup(StrMethodMixin, models.Model):
    """Модель группы человек, живущих вместе"""

    name = models.CharField('название', max_length=63)
    created_at = models.DateField('дата создания', auto_now_add=True)
    objects = RoommatesGroupManager()

    class Meta:
        verbose_name = 'группа человек'
        verbose_name_plural = 'группы человек'


class User(AbstractUser):
    email = models.EmailField('электронная почта', unique=True)
    roommates_group = models.ForeignKey(RoommatesGroup, on_delete=models.SET_NULL, null=True,
                                        verbose_name='группа человек')

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._meta.get_field('username').help_text = ''
        self._meta.get_field('is_superuser').help_text = 'Супер пользователь имеет все права без их явного назначения'
        self._meta.get_field('is_staff').help_text = 'Сотрудник может иметь права на изменение определенных ресурсов'
