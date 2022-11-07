from django.contrib.auth.models import AbstractUser
from django.db import models
from goods_accounting.models import RoommatesGroup


class User(AbstractUser):
    email = models.EmailField('электронная почта', unique=True)
    roommates_group = models.ForeignKey(RoommatesGroup, on_delete=models.SET_NULL, null=True,
                                        verbose_name='группа человек')
